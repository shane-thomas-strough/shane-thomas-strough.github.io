# Architecting Air-Gapped AI: Deploying Local Enterprise Models for Secure Infrastructure

**Author: Shane Thomas Strough**
**Field Notes Series — [shanestrough.com](https://shanestrough.com)**

---

## The Thesis

If your data leaves your building, you do not control it. In classified, federal, medical, legal, and critical infrastructure environments, that is not a philosophical position — it is a regulatory requirement, a contractual obligation, and an operational reality. Cloud AI is not an option. The model must live inside the wire.

I built a bare-metal AI workstation specifically to solve this problem: sovereign local inference with zero external API dependency. This article walks through the why, the how, and the economics of deploying air-gapped AI infrastructure for organizations that cannot afford to send their data to someone else's server.

---

## Why Cloud AI Is Unacceptable

Let me be direct about the environments where cloud-based AI services are a non-starter.

**DoD and Classified Facilities.** Any facility operating under NIST 800-171, CMMC, or handling CUI (Controlled Unclassified Information) has strict data handling requirements that prohibit sending sensitive content to third-party cloud APIs. It does not matter that OpenAI or Anthropic have enterprise agreements. It does not matter that the API connection is encrypted in transit. The data leaves the controlled environment. For classified and CUI-adjacent workflows, that is a disqualifying condition.

**Federal Facilities with FISMA Requirements.** Federal Information Security Management Act compliance mandates that agencies maintain control over information systems processing federal data. A cloud API is an external information system. The authorization boundary extends to every system that touches the data. Adding a cloud AI provider to your authorization boundary adds their entire infrastructure to your risk assessment. Most federal security officers will reject that on sight.

**Medical and HIPAA Environments.** Protected Health Information has specific handling, storage, and access requirements under HIPAA. While some cloud AI providers offer BAA (Business Associate Agreement) coverage, the practical reality is that PHI flowing through an external API creates audit exposure, breach notification obligations, and patient consent complications that most healthcare organizations are not equipped to manage.

**Legal and Privileged Communications.** Attorney-client privilege requires that privileged communications remain within the control of the legal entity. Running privileged documents through a cloud AI for summarization, analysis, or discovery preparation creates a third-party exposure that could be challenged as a waiver of privilege. No competent general counsel will accept that risk.

**Critical Infrastructure and ICS/SCADA.** Operational technology environments — power plants, water treatment, manufacturing, data centers — operate on air-gapped or segmented networks specifically to prevent external data exfiltration. Introducing a cloud API dependency into an OT environment defeats the purpose of the air gap.

These are not edge cases. These are entire sectors of the economy that need AI capabilities but cannot use the delivery model that the market has standardized on.

---

## Data Sovereignty as a Non-Negotiable

Data sovereignty is not a feature request. It is a constraint that the architecture must satisfy before any other requirement is considered.

Sovereignty means three things:

**1. The data never leaves the physical premises.** Not encrypted. Not anonymized. Not tokenized. Never leaves. The inference happens on hardware that you own, in a room that you control, on a network that has no path to the public internet.

**2. The model weights are stored locally.** You do not download model weights on demand from a remote repository every time you run inference. The weights are on local storage. The machine can operate with the network cable unplugged. If the internet goes down globally, your AI still works.

**3. No telemetry, no usage reporting, no external callbacks.** The software stack must be auditable to confirm that no component is phoning home. Open-source models with published weights and open-source inference frameworks satisfy this requirement. Proprietary runtimes with opaque binaries do not.

When I say air-gapped, I mean air-gapped. The workstation I built can run in a SCIF. It can run in a hospital server room. It can run in a law firm's document review center. It does not need the internet to function, and it does not communicate with any external service during operation.

---

## The Build: RTX 5090 Bare-Metal Workstation

I will walk through the actual hardware I specified and assembled, because the theoretical discussion of air-gapped AI means nothing without a concrete reference architecture.

**Processor: AMD Ryzen 9 9950X**
16 cores, 32 threads. This is not the inference bottleneck — the GPU handles inference — but the CPU manages data preprocessing, tokenization, document ingestion, and orchestration. The 9950X provides enough headroom to run the full software stack (inference server, API layer, document processing pipeline) simultaneously without contention.

**GPU: NVIDIA RTX 5090 (32GB GDDR7)**
This is the inference engine. The RTX 5090 delivers the VRAM capacity to run 70B-parameter models quantized to 4-bit, or 13B-parameter models at full precision. For most enterprise use cases — document analysis, summarization, Q&A over proprietary corpora, code review — a well-tuned 13B or 30B model running locally on a 5090 matches or exceeds the quality of cloud API calls for domain-specific tasks.

The key metric is VRAM, not FLOPS. Model inference is memory-bandwidth bound. The 32GB of GDDR7 on the 5090 with 1,792 GB/s bandwidth means tokens generate fast enough for real-time interactive use. I consistently see 40-60 tokens per second on 13B models and 15-25 tokens per second on 70B quantized models. That is faster than most cloud API response times once you factor in network latency.

**Memory: 96GB DDR5-6000**
The system RAM handles document ingestion, embedding generation, vector database operations, and the operating system. 96GB is sufficient to load large document corpora into memory for processing while the GPU handles inference. For organizations processing thousands of documents, this is the minimum I would specify.

**Storage: 2x Samsung 990 PRO 4TB NVMe (Gen5)**
8TB total local storage. Gen5 NVMe provides sequential read speeds exceeding 14 GB/s, which matters when loading model weights from disk to VRAM. A 70B model at 4-bit quantization is approximately 35GB — it loads from NVMe to VRAM in under 3 seconds. The second drive provides storage for document corpora, vector databases, and model weight archives.

**Operating System: Ubuntu 24.04 LTS**
Bare metal. No hypervisor. No container orchestration layer unless the deployment requires it. Ubuntu LTS provides the CUDA toolkit, PyTorch compatibility, and long-term security updates. The system runs headless — all interaction is via SSH or a local terminal.

**Total hardware cost: approximately $8,000.**

---

## The Software Stack: From Power-On to Inference

Here is the deployment sequence from first power-on to running local inference, written for an engineer who has never set up an AI workstation.

**Step 1: Base OS Installation**
Install Ubuntu 24.04 LTS from USB. Configure disk partitioning: 500GB for OS and software on drive 1, remaining space on drive 1 plus all of drive 2 for data. Set a strong root password. Create a service account for the inference workload. Disable automatic updates if the machine will be air-gapped — you will manage updates manually via sneakernet.

**Step 2: NVIDIA Driver and CUDA Toolkit**
Install the NVIDIA proprietary driver (currently 570.x series for the 5090). Install CUDA Toolkit 12.8. Verify with `nvidia-smi` — you should see the RTX 5090 with 32GB VRAM reported. If you are deploying to an air-gapped environment, download the driver and CUDA packages on a connected machine and transfer via encrypted USB.

**Step 3: Python Environment**
Install Python 3.12 via pyenv. Create a virtual environment for the inference stack. Install PyTorch 2.9+ with CUDA 12.8 support. Verify GPU detection: `torch.cuda.is_available()` must return `True` and `torch.cuda.get_device_name(0)` must report the RTX 5090.

**Step 4: Model Download and Storage**
On a connected machine, download model weights from Hugging Face. For enterprise document analysis, I recommend starting with Llama 3.1 70B (4-bit GPTQ quantization) or Mistral Large. Transfer weights to the workstation via encrypted USB or a secure internal network share. Store weights on the NVMe data partition.

**Step 5: Inference Server**
Deploy vLLM or llama.cpp as the inference backend. vLLM provides an OpenAI-compatible API endpoint, which means any application built for the OpenAI API can be pointed at your local server with a configuration change — no code modification required. Start the server bound to localhost only (127.0.0.1) so it is not accessible from the network unless you explicitly configure access.

**Step 6: RAG Pipeline (Optional but Recommended)**
For document analysis use cases, deploy a Retrieval-Augmented Generation pipeline:
- **Document ingestion:** LangChain or LlamaIndex for parsing PDFs, Word docs, and text files
- **Embedding model:** A local embedding model (e.g., BGE-large or E5-large) running on the same GPU
- **Vector database:** pgVector (PostgreSQL extension) or ChromaDB for local vector storage
- **Retrieval:** Query the vector database, retrieve relevant chunks, inject into the LLM prompt as context

This gives you a system that can answer questions about your proprietary documents using your local model, with zero data leaving the machine.

**Step 7: Hardening**
- Disable all unnecessary network services
- Configure the host firewall (ufw) to block all inbound connections except SSH from authorized IPs
- If truly air-gapped, disable the network interface entirely after setup is complete
- Enable disk encryption (LUKS) on the data partition
- Configure audit logging for all access to the inference service
- Set up unattended security monitoring via local syslog

---

## Cost Analysis: Own vs. Rent

The economics are straightforward once you run the numbers at enterprise scale.

**Cloud API Costs (OpenAI GPT-4 class, as of early 2026):**
- Input tokens: ~$2.50 per million tokens
- Output tokens: ~$10.00 per million tokens
- A single legal document review workflow processing 1,000 documents per month generates approximately 500 million input tokens and 50 million output tokens
- Monthly cost: ~$1,750
- Annual cost: ~$21,000 for a single workflow

Scale that to an organization with multiple departments — legal, compliance, HR, engineering — each running document analysis workflows, and you are looking at $50,000 to $150,000 per year in API costs. And that cost scales linearly with usage. More documents, more cost. More users, more cost. Every token is metered.

**Local Infrastructure Costs:**
- Hardware (one-time): ~$8,000
- Electricity (estimated 500W average draw, 24/7): ~$525/year
- Maintenance and model updates: ~$500/year in labor
- Total first-year cost: ~$9,025
- Total year-two-plus cost: ~$1,025/year

**Break-even: approximately 5-6 months** against a moderate enterprise API workload.

After break-even, you are running inference at effectively the cost of electricity. The marginal cost of an additional query is zero. There is no per-token charge. There is no usage tier. You own the hardware. You own the models. You own the output.

For organizations processing sensitive data, the cost comparison is actually irrelevant — they cannot use the cloud option at any price. But it is useful to know that the local option is not just more secure, it is also cheaper at scale.

---

## Use Cases: Where This Architecture Deploys

**Legal Document Analysis**
Law firms processing discovery documents, contract review, and regulatory filings. A local RAG pipeline ingests the document corpus and enables attorneys to query their own files with natural language. Privileged material never leaves the firm's infrastructure. I have seen firms reduce document review time by 60-70% using this architecture.

**Medical Records and Clinical Decision Support**
Healthcare organizations running clinical note summarization, diagnostic support queries, and patient record analysis. PHI stays within the facility's physical and logical boundary. No BAA required with a third party because there is no third party.

**DoD-Adjacent Facilities and Defense Contractors**
Organizations handling CUI that need AI-assisted analysis of technical documents, proposals, and compliance artifacts. The air-gapped workstation can operate in a controlled space that satisfies NIST 800-171 requirements without extending the authorization boundary to a cloud provider.

**Critical Infrastructure Operations**
Power utilities, water treatment facilities, and data center operators that need AI-assisted analysis of SCADA data, maintenance records, and operational procedures. The inference engine runs on the OT network or in a DMZ without any path to the public internet.

**Financial Services and Proprietary Trading**
Quantitative analysis, strategy backtesting, and proprietary research where the intellectual property is the data itself. Sending trading signals, market analysis, or strategy parameters through a cloud API is an unacceptable information leakage risk. Local inference keeps the alpha inside the wire.

---

## The Model Quality Question

The most common objection I hear: "Local models cannot match GPT-4 or Claude quality."

This was true in 2023. It is not true in 2026. The open-weight model ecosystem has closed the gap dramatically for domain-specific tasks. The key insight is that enterprise AI use cases are not general-purpose — they are narrowly scoped. You are not asking the model to write poetry, pass a bar exam, and debug Rust code in the same session. You are asking it to analyze contracts, summarize medical records, or extract entities from technical documents.

For those narrow, well-defined tasks, a 70B-parameter model fine-tuned or prompted with domain-specific context performs at parity with — and in some cases exceeds — cloud API models. The RAG architecture amplifies this: the model does not need to know everything. It needs to reason well over the context you provide. Open-weight models with good reasoning capabilities and a well-constructed retrieval pipeline deliver production-grade results.

I run blind comparison tests regularly. I submit the same document analysis query to my local Llama 3.1 70B with RAG and to a cloud API. For my specific use cases — technical document analysis, specification review, compliance checking — the local model produces equivalent or superior output approximately 85% of the time. The 15% delta is typically on highly nuanced multi-step reasoning tasks where the frontier cloud models still hold an advantage. For those tasks, you adjust the pipeline: break the query into steps, retrieve more context, or use a chain-of-thought prompt structure.

The models are good enough. The architecture matters more than the model.

---

## The Case for Keeping the Model Inside the Wire

The cloud AI model works for many use cases. If you are a marketing team generating social media content, use the cloud. If you are a software team using Copilot for code completion on open-source projects, use the cloud. The convenience, the managed infrastructure, and the automatic model updates are genuine advantages for non-sensitive workloads.

But if your data has regulatory, contractual, or competitive sensitivity — and you are honest with yourself about what that means — then the cloud model is a liability disguised as convenience.

The air-gapped architecture I have described is not theoretical. It is running in my office right now. The RTX 5090 workstation processes documents, generates analysis, runs inference on proprietary data, and does all of it without a single packet leaving my network. I built it, I deployed it, and I use it daily.

The barrier to entry is lower than most organizations assume. $8,000 in hardware. Open-source models that match cloud API quality for domain-specific tasks. A deployment process that a competent systems administrator can execute in a day.

The question is not whether you can afford to build this. The question is whether you can afford not to — when the alternative is sending your most sensitive data to someone else's server and hoping their security practices are as rigorous as yours.

Keep the model inside the wire. Own your inference. Own your data.

---

## Getting Started

If your organization needs AI capabilities but operates under data sovereignty constraints, here is the action plan:

1. **Define your use case.** What documents, data, or workflows will the AI support? This determines the model size and the RAG architecture requirements.

2. **Specify the hardware.** Use the build in this article as a reference. Adjust VRAM and storage based on your model size and corpus volume.

3. **Select your model.** For general document analysis, start with Llama 3.1 70B (4-bit quantized). For code analysis, use CodeLlama or DeepSeek Coder. For multilingual requirements, use Mistral Large. All open-weight, all auditable.

4. **Deploy and test.** Follow the deployment sequence in this article. Test with a representative sample of your actual data before rolling out to users.

5. **Document and harden.** Treat the AI workstation like any other piece of critical infrastructure. Document the configuration. Harden the OS. Restrict access. Audit usage.

The infrastructure the future runs on will not all live in the cloud. Some of it must stay inside the wire. Build accordingly.

---

*Shane Thomas Strough is an Integration and Commissioning Leader with 15+ years across DoD, federal, aerospace, hyperscale data center, and industrial infrastructure. Founder of Elevare Edge LLC, specializing in air-gapped AI infrastructure and secure enterprise deployments.*

*Connect at [shanestrough.com](https://shanestrough.com) · [LinkedIn](https://www.linkedin.com/in/shane-thomas-strough/) · [AI Infrastructure Consulting](https://shanestrough.com/about.html)*
