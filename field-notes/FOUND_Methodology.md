# Accelerating the Workforce: Deploying the FOUND Methodology in Enterprise L&D

**Author: Shane Thomas Strough**
**Field Notes Series — [shanestrough.com](https://shanestrough.com)**

---

## The Thesis

Learning and development is an engineering problem. It has inputs, outputs, measurable throughput, and quantifiable waste. Treating it as an HR function — soft, unmeasured, disconnected from operational metrics — is why most enterprise L&D programs fail to move the needle on the metrics that actually matter: time-to-productivity, retention, and revenue per employee.

I designed the FOUND methodology — Framework for Opportunities, Upskilling, and Next-level Development — while leading workforce development integration at M.C. Dean, a $2B+ electrical and technology integration enterprise with approximately 5,000 employees. The problem I was solving was concrete: new commissioning technicians took 8 weeks to reach baseline productivity. The company was hemorrhaging institutional knowledge through attrition. Static training catalogs were not keeping pace with the technical complexity of the work.

FOUND is the system I built to fix it. This article lays out the methodology, the technology stack, the deployment strategy, and the projected ROI.

---

## The Problem: Why Traditional L&D Fails in Technical Enterprises

M.C. Dean executes mission-critical electrical and technology infrastructure across DoD, federal, data center, and commercial sectors. The work is technically complex: commissioning building automation systems, integrating SCADA and EPMS platforms, performing zero-downtime cutovers on live power distribution systems, and testing fire alarm integrations in occupied facilities.

The workforce development challenge is specific to this type of organization:

**8-week ramp time for new technicians.** A newly hired commissioning technician — even one with an electrical license and field experience — takes approximately 8 weeks before they contribute meaningfully to project execution. They need to learn company-specific procedures, project-specific systems (Siemens, Schneider, Honeywell), site-specific safety protocols, and the commissioning methodology. During those 8 weeks, they consume senior technician time for mentoring, they slow down the crew, and they represent negative productivity.

**Institutional knowledge loss.** When a senior superintendent with 20 years of commissioning experience leaves the company, their knowledge goes with them. It is not captured in a document repository. It is not encoded in a training program. It exists only in their head. The next person in that role starts from a lower baseline, and the organization has permanently lost capability.

**Static training catalogs.** The existing L&D infrastructure was built around static course catalogs — a list of available training classes organized by trade or discipline. The catalog did not account for individual career trajectories, project-specific requirements, or the gap between a technician's current skill set and their target role. A technician looking to advance from field installer to commissioning lead had no structured pathway. They had a list of classes and a hope that someone would mentor them.

**Disconnection from operational metrics.** The L&D department tracked course completions and training hours. Operations tracked project performance, rework rates, and schedule adherence. There was no connection between the two. Nobody could answer the question: "Does our training investment actually improve field execution?"

These are not unique problems. They are endemic across technical enterprises — construction, utilities, manufacturing, defense contracting. The scale at M.C. Dean made the impact visible, but the pattern is universal.

---

## The FOUND Framework

FOUND is a five-component methodology that replaces static training catalogs with a dynamic, AI-powered career development system. Each component addresses a specific failure mode of traditional L&D.

### F — Framework

The structural foundation. Before you build career pathways, you need an accurate model of the organization's roles, competencies, and technical requirements.

**Role Taxonomy.** Every role in the organization is defined with a specific set of required competencies, organized by level (entry, intermediate, senior, lead, superintendent). Each competency has measurable proficiency criteria — not subjective assessments, but observable, testable capabilities.

For commissioning roles, the competency framework looks like this:

| Level | Example Competencies |
|---|---|
| Entry (Installer) | Wire termination, conduit installation, LOTO compliance, basic multimeter use |
| Intermediate (Technician) | Loop testing, point-to-point verification, BACnet device configuration, submittal review |
| Senior (Cx Tech) | Sequence of operation testing, integrated systems testing, relay event log analysis, SBAR reporting |
| Lead (Cx Lead) | MOP development, test plan authoring, subcontractor coordination, owner interface |
| Superintendent | Program-level scheduling, risk management, multi-trade SIMOPS, P&L accountability |

This taxonomy is not a job description. It is an engineering specification for what a person at each level must be able to do. It is testable and auditable.

**Gap Analysis.** For every employee, the system compares their current verified competencies against their target role. The delta is their development plan. This is not a subjective manager assessment — it is a structured comparison of demonstrated capabilities against role requirements.

### O — Opportunities

The identification and matching of development opportunities to individual gaps.

Traditional L&D says: "Here is a catalog of 200 courses. Find the ones relevant to you." FOUND inverts this: "Here are the 6 specific competencies you need to develop to reach your target role, and here are the opportunities that will develop each one."

Opportunities are not limited to classroom training. They include:

- **Project assignments.** Placing a technician on a Siemens Desigo CC commissioning project when their gap analysis shows BAS integration as a development need. The project itself is the training.
- **Structured mentoring.** Pairing a senior superintendent with a commissioning lead who is developing program management competencies. The mentoring has specific objectives, a defined timeline, and measurable outcomes.
- **Digital courses.** Targeted e-learning modules developed from the company's own commissioning methodology. Not generic vendor training — company-specific procedures taught by the company's own subject matter experts.
- **Bootcamps.** Intensive, multi-day training events that combine classroom instruction with hands-on lab exercises. I designed the commissioning bootcamp series at M.C. Dean — the Siemens Data Center Commissioning Guide is one session from that series.
- **Certifications.** External certifications (NETA, NICET, CxA) mapped to specific role levels so employees know exactly which certifications they need and when.

### U — Upskilling

The execution engine. This is where the development plan becomes actionable.

**Personalized Learning Paths.** Based on the gap analysis, each employee receives a sequenced development plan with specific milestones, deadlines, and verification checkpoints. The path is not generic — it is tailored to their starting point, their target role, and the opportunities available on their current or upcoming projects.

**AI-Powered Content Delivery.** This is where GPT Enterprise enters the architecture. The system ingests the company's proprietary training materials, procedures, standards, and commissioning guides. When a technician has a question about BACnet MS/TP configuration on a Siemens PXC controller, they do not search a document repository and hope to find the right PDF. They query the AI, which retrieves the relevant content from the ingested corpus and delivers a contextual answer with source citations.

This is not chatbot novelty. This is the difference between a technician spending 45 minutes searching for information and getting an accurate, sourced answer in 30 seconds. Multiply that by 5,000 employees and thousands of queries per week, and the productivity impact is measurable.

**Progress Tracking.** Every completed module, every passed assessment, every verified competency is recorded. The employee's competency profile updates in real time. Managers see a dashboard of their team's development progress against project requirements. The L&D department sees aggregate metrics tied to operational outcomes.

### N — Next-Level Development

The forward-looking component. FOUND does not just close current gaps — it prepares the workforce for where the organization is going.

**Technology Roadmap Alignment.** If the organization is expanding into hyperscale data center commissioning, the development system proactively identifies employees who have the foundational competencies to upskill into that domain and begins building their pathway before the projects are awarded.

**Leadership Pipeline.** Superintendent and program management roles are not filled by hoping the right person emerges organically. They are filled by systematically developing candidates through the competency framework over a 2-3 year horizon. When a superintendent role opens, there are three qualified internal candidates ready to step in.

**Emerging Technology Integration.** As new systems enter the commissioning scope — Small Modular Reactors, advanced battery energy storage systems, AI-powered building management — the competency framework updates and the development system generates new pathways for the affected roles.

### D — Development (Continuous)

The feedback loop. FOUND is not a one-time implementation. It is a continuously improving system.

**Outcome Measurement.** The L&D metrics are tied directly to operational metrics:
- Time-to-productivity for new hires (target: 8 weeks reduced to 2 weeks)
- Rework rates on projects staffed by employees on active development plans
- Retention rate among employees with active career pathways vs. those without
- Internal promotion rate vs. external hiring rate for senior roles

**Content Refresh.** Training content is updated based on field feedback. When a commissioning lead identifies a recurring knowledge gap in the field — for example, technicians consistently misconfiguring BACnet BBMD settings — that gap is flagged, new content is developed, and the relevant learning paths are updated within weeks, not quarters.

---

## The Technology Stack: GPT Enterprise Integration

The AI layer is what makes FOUND scalable. Without it, personalized career pathway delivery for 5,000 employees is a staffing problem that requires dozens of dedicated L&D specialists. With it, the system is largely self-service.

**GPT Enterprise** was selected for three reasons:

1. **Data privacy.** GPT Enterprise does not train on customer data. The proprietary training materials ingested into the system remain within the organization's data boundary. This was a non-negotiable requirement — M.C. Dean handles DoD and federal program information that cannot be used for model training.

2. **Document ingestion.** The system ingests the company's existing document corpus: commissioning procedures, safety manuals, equipment-specific guides, project-specific specifications. This corpus becomes the retrieval source for AI-assisted queries.

3. **Natural language interface.** Technicians interact with the system in plain language. "What is the BACnet MS/TP baud rate for Siemens PXC controllers on the AWS Dataville project?" returns a precise answer with a citation to the project-specific specification. No search syntax. No document management skills required.

**Offline Capability for Secure Environments**

For DoD and classified programs where GPT Enterprise's cloud infrastructure is not acceptable, the FOUND methodology deploys with a local inference alternative. The same RAG pipeline architecture described in my air-gapped AI article applies here: local model weights, local vector database, local inference. The career pathway logic and competency framework are application-layer functions that run on any inference backend.

This dual-deployment capability — cloud for standard environments, local for secure environments — means FOUND scales across the full spectrum of an organization's portfolio without creating data sovereignty exceptions.

---

## Commissioning Bootcamps: The Accelerator

The bootcamp program is the highest-intensity component of FOUND. It is designed to compress months of on-the-job learning into days of structured, hands-on training.

**Format:** 3-5 day intensive sessions. Classroom instruction in the morning. Hands-on lab exercises in the afternoon. Assessments at the end of each day.

**Content development methodology:** Every bootcamp session is developed by extracting knowledge from the company's senior subject matter experts and converting it into structured, teachable material. The Siemens Data Center Commissioning Guide is an example of this process — it captures the field knowledge of experienced commissioning agents in a format that can be taught, tested, and referenced.

**Bootcamp series I designed at M.C. Dean:**

| Session | Topic | Duration |
|---|---|---|
| Session 1 | Commissioning Fundamentals — process, documentation, tools | 3 days |
| Session 2 | Electrical Commissioning — MV/LV switchgear, protection relays, power distribution | 5 days |
| Session 3 | Siemens BAS and Fire Alarm Commissioning | 3 days |
| Session 4 | Schneider Electric BAS and Power Monitoring | 3 days |
| Session 5 | Integrated Systems Testing — methodology and execution | 3 days |
| Session 6 | Commissioning Leadership — MOPs, test plans, owner interface | 2 days |

**Impact on ramp time:** Technicians who completed Sessions 1-3 before their first project assignment reached baseline productivity in 2 weeks instead of 8. That is a 75% reduction in ramp time. For an organization deploying 50-100 new technicians per year, the cumulative productivity gain is measured in thousands of labor-hours recovered.

---

## ROI Model: The Business Case

The FOUND ROI model is built on three quantifiable value drivers.

**1. Turnover Reduction**

Industry average turnover for skilled electrical trades is approximately 20-25% annually. M.C. Dean's rate was consistent with industry averages. Each departure costs the organization approximately $30,000-$50,000 in recruiting, onboarding, and lost productivity (conservative estimate for technical roles).

FOUND targets a 10% reduction in turnover — from 25% to 22.5% — by providing visible career pathways, personalized development plans, and demonstrated organizational investment in employee growth. Research consistently shows that career development opportunities are the primary driver of retention for technical professionals, outranking compensation in most surveys.

**The math:**
- 5,000 employees at 25% turnover = 1,250 departures/year
- 10% reduction = 125 fewer departures
- Average cost per departure: $35,000
- Annual savings: $4.375 million

Even at a conservative realization rate of 35% (accounting for the fact that not all retained employees would have left for L&D-related reasons), the turnover savings exceed **$1.5 million annually at the SBU level**.

**2. Productivity Acceleration**

The ramp time reduction from 8 weeks to 2 weeks for new commissioning technicians recovers 6 weeks of productive capacity per new hire.

**The math:**
- 100 new commissioning technicians per year
- 6 weeks recovered per technician
- Average fully-loaded labor cost: $85/hour
- 6 weeks x 40 hours = 240 hours recovered per technician
- 100 technicians x 240 hours x $85/hour = **$2.04 million in recovered productivity annually**

**3. Reduced External Training Spend**

By developing internal bootcamp content and AI-powered self-service learning, the organization reduces its dependency on external vendor training programs.

**The math:**
- Average external training cost per technician per year: $3,000-$5,000
- 50% reduction through internal content development: $1,500-$2,500 savings per technician
- Applied to 1,000 technicians in the commissioning workforce: **$1.5M-$2.5M in reduced external training spend**

**Total projected annual ROI: $5M-$9M** across the three value drivers. The FOUND system investment — platform development, content creation, and first-year operating costs — is recoverable within 6-9 months.

---

## Why L&D Is an Engineering Problem

I came to workforce development from the field, not from HR. My background is commissioning infrastructure — designing test plans, executing procedures, verifying that systems perform as specified. When I looked at the L&D function through that lens, I saw the same deficiencies I would flag on a commissioning project:

**No specification.** There was no clear definition of what "trained" meant for each role. In commissioning, we would never accept "the system works" without a specification to test against. But that is exactly what L&D was doing — declaring people trained without a competency specification to verify against.

**No test plan.** Training completion was tracked by attendance and course completion, not by demonstrated competency. In commissioning terms, this is like signing off on a system because the contractor said they installed it, without performing any functional testing.

**No feedback loop.** There was no mechanism to connect training outcomes to field performance. In commissioning, we trend data after startup to verify the system performs as designed under real conditions. L&D had no equivalent — once a technician completed a course, there was no verification that the training improved their field execution.

**No continuous improvement.** The training content was updated on a multi-year cycle, if at all. In commissioning, we update procedures after every project based on lessons learned. L&D was operating on static content that was years behind the current state of the technology.

FOUND applies commissioning discipline to workforce development. Define the specification (competency framework). Build the test plan (assessments). Execute the test (training delivery). Verify the outcome (operational metrics). Feed back the results (continuous content improvement).

The methodology works because it treats human capability development with the same rigor we apply to system commissioning. People are not less complex than building automation systems. If anything, they are more complex. They deserve at least the same level of engineering discipline.

---

## Deployment Roadmap

For organizations looking to implement FOUND or a similar methodology, here is the phased approach I recommend:

**Phase 1: Foundation (Months 1-3)**
- Build the role taxonomy and competency framework for your highest-priority workforce segment
- Conduct gap analysis on the target population
- Identify and prioritize the top 10 competency gaps by frequency and operational impact
- Select and configure the AI platform (GPT Enterprise or local inference)

**Phase 2: Content Development (Months 3-6)**
- Develop bootcamp curriculum for the top-priority competencies
- Ingest existing training materials and procedures into the AI system
- Build the first set of personalized learning paths based on gap analysis
- Deploy to a pilot group of 50-100 employees

**Phase 3: Scale (Months 6-12)**
- Expand to additional workforce segments
- Integrate competency data with HR and project management systems
- Establish the operational metric linkage (ramp time, rework rates, retention)
- Publish the first ROI report based on pilot group data

**Phase 4: Continuous Improvement (Ongoing)**
- Quarterly content refresh based on field feedback and lessons learned
- Annual competency framework review aligned to organizational strategy
- Expand AI capabilities (automated assessment generation, predictive gap analysis)
- Extend to subcontractor workforce development

---

## The Takeaway

The skilled trades workforce crisis is not a future problem. It is a current reality. The organizations that will thrive are the ones that treat workforce development as a core engineering function — measured, optimized, and continuously improved with the same discipline they apply to their technical infrastructure.

FOUND provides the framework. The AI provides the scale. The commissioning mindset provides the rigor.

Stop treating L&D as overhead. Start treating it as infrastructure. The ROI is there. The methodology is proven. The workforce is waiting.

---

*Shane Thomas Strough is an Integration and Commissioning Leader with 15+ years across DoD, federal, aerospace, hyperscale data center, and industrial infrastructure. He designed the FOUND methodology while leading workforce development integration at M.C. Dean, Inc. Founder of Elevare Edge LLC.*

*Connect at [shanestrough.com](https://shanestrough.com) · [LinkedIn](https://www.linkedin.com/in/shane-thomas-strough/) · [Field Notes & Insights](https://shanestrough.com/insights.html)*
