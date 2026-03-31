# Bridging the Gap: Aligning E&I Field Execution with OT/IT Network Integration

**Author: Shane Thomas Strough**
**Field Notes Series — [shanestrough.com](https://shanestrough.com)**

---

## The Thesis

The most expensive failures in mission-critical infrastructure do not happen inside the electrical distribution system or inside the network architecture. They happen at the boundary between the two — the handoff point where operational technology meets information technology, where the E&I field team meets the network engineering team, and where everyone assumes someone else has it covered.

I call it the OT/IT ambush. It is the moment during a live-environment cutover when the network team discovers the electrical team changed the power feed to a fiber switch without coordinating the VLAN configuration, or the controls integrator learns that the new BAS controller they just racked was never added to the OT network's whitelist. Nobody planned for the collision. Everyone assumed their scope was independent. The result is downtime, finger-pointing, and a punch list that just became a re-engineering effort.

I have spent 15+ years working both sides of this boundary — commissioning medium-voltage switchgear, programming SEL relays, pulling fiber backbones, configuring SCADA RTUs, and tying remote facilities into self-healing ring networks. The lesson is always the same: the OT/IT handoff is where most programs fail, and the only defense is treating integration as a discipline, not an afterthought.

This article is the field-tested playbook for aligning E&I execution with OT/IT network integration across data centers, DoD facilities, industrial plants, and distributed infrastructure.

---

## The OT/IT Ambush: How It Happens

The ambush does not announce itself. It builds quietly across weeks of parallel execution until it detonates during the integrated systems test or, worse, during a live cutover.

Here is the anatomy. The electrical team is commissioned and tested on their scope — switchgear, MCCs, VFDs, protection relays. They have completed their point-to-point testing. Their megger results are clean. Their relay settings match the coordination study. From their perspective, the system is ready.

Simultaneously, the OT/IT team has been building their network infrastructure — switches, firewalls, fiber backbone, RTAC gateways, SCADA head-end. They have verified their VLANs, their routing tables, their firewall rules. Their pings come back. From their perspective, the system is ready.

The ambush happens when you try to make both systems work together. The protection relay that the electrical team commissioned on a test bench has Ethernet ports that need to land on the OT network — but nobody coordinated the IP addressing scheme between the relay settings and the network DHCP reservations. The BAS controller that the controls team programmed in the shop needs to communicate with the EPMS server — but the firewall rule set does not include the BACnet/IP port because the network team was never given the communication matrix.

I have seen this exact pattern on data center programs, DoD installations, industrial plants, and distributed oil and gas SCADA systems. The technology changes. The failure mode does not.

The root cause is organizational, not technical. Electrical teams, controls teams, and network teams typically report through different supervisory chains. Their scopes of work are written by different engineers. Their submittals are reviewed by different disciplines. Their commissioning procedures are developed independently. At no point in the process is anyone required to verify that all three systems will function as an integrated whole — until the IST, when it is too late to fix it cheaply.

---

## Self-Healing Fiber Rings and SEL RTAC Interfaces

Let me get specific about the technology, because the integration challenges live in the details.

**Self-healing fiber rings** are the backbone architecture for distributed SCADA and protection systems. The concept is straightforward: fiber optic cable connects every node in a ring topology, and if any single segment fails — a cut cable, a failed switch — traffic automatically reroutes in the opposite direction around the ring. Recovery time is measured in milliseconds. The system self-heals without human intervention.

I have deployed self-healing rings on remote well site SCADA networks, DoD campus distribution systems, and data center BMS networks. The architecture is elegant and proven. The integration challenges are entirely practical.

**Challenge 1: Fiber termination timing.** The fiber backbone is typically installed by the electrical contractor, but the switches that terminate the ring are procured and configured by the OT/IT integrator. If the electrical contractor completes their fiber pulls and terminations before the switches are on site, you have untested fiber sitting in conduit for weeks. When the switches finally arrive and the OT team begins commissioning, they discover that three of the 24 fusion splices have loss values above the threshold because the fiber was stressed during a cable tray installation that happened after the initial pull. Now the fiber contractor has to re-mobilize.

**The fix:** Fiber acceptance testing — OTDR and insertion loss testing — must be a joint hold point between the electrical contractor and the OT integrator. Neither party proceeds until both have verified the physical medium. I build this into every MOP as a mandatory sign-off gate.

**Challenge 2: Ring convergence time vs. protection relay requirements.** SEL (Schweitzer Engineering Laboratories) RTAC units — Real-Time Automation Controllers — are the workhorses of modern substation and industrial SCADA integration. They aggregate data from protection relays, meters, I/O modules, and other IEDs (Intelligent Electronic Devices) via protocols like DNP3, Modbus, and IEC 61850. The RTAC then communicates upstream to the SCADA head-end.

The problem is that protection relays have communication timing requirements that are tighter than generic IT network SLAs. An SEL-351 overcurrent relay sending a trip signal via GOOSE messaging under IEC 61850 expects sub-4ms delivery. If the self-healing ring is in the middle of a convergence event when that message needs to transit, and the ring protocol takes 50ms to reroute, you have a protection gap.

**The fix:** Protection-critical messaging must be architecturally separated from monitoring and data collection traffic. I use dedicated VLANs with strict QoS policies for protection traffic on rings that also carry SCADA polling. On critical installations, I specify dual-homed relay connections — the relay has two Ethernet ports on two separate paths — so there is no single point of failure in the communication path.

**Challenge 3: RTAC configuration vs. relay settings.** The RTAC needs to know the address, protocol, and register map of every device it polls. The protection relay needs to know the IP address and communication parameters of the RTAC. These configurations are developed by different teams — the relay settings by the protection engineer, the RTAC configuration by the SCADA integrator. If either side changes a parameter without notifying the other, communication fails silently. The RTAC shows "device offline" and the control room operator has no visibility into a critical relay.

**The fix:** A single, version-controlled communication matrix that is jointly owned by the protection engineer and the SCADA integrator. Every IP address, every DNP3 address, every register map, every polling interval — all in one document. Any change requires both parties to sign off before implementation. This document is the Rosetta Stone of OT/IT integration, and I treat it with the same rigor as a relay coordination study.

---

## Change-Freeze Protocols Before and During Cutovers

The most dangerous period in any OT/IT integration is the 48 hours before and during a live-environment cutover. This is when last-minute changes — "quick fixes" — create cascading failures that nobody can diagnose under time pressure.

I enforce a **hard change freeze** that follows this timeline:

**T-48 hours:** All configuration changes to OT/IT systems stop. No firmware updates. No VLAN changes. No firewall rule modifications. No relay setting adjustments. The system state is documented — every switch port configuration, every firewall rule set, every relay setting file — and that documentation becomes the baseline for the cutover.

**T-24 hours:** Pre-cutover verification. Every communication path in the system is tested. Every SCADA point is verified end-to-end: field device to RTAC to head-end. Every alarm is confirmed. Every trend is logging. If anything fails pre-cutover verification, the cutover is postponed until the issue is resolved and the verification is repeated from the beginning. Not from the point of failure — from the beginning.

**T-0 (cutover execution):** The only changes permitted are the planned cutover steps documented in the MOP. Any deviation requires the Commissioning Lead (me) and the OT/IT Lead to jointly authorize. Verbal agreements do not count. The authorization is documented on the MOP in real time.

**T+24 hours (post-cutover monitoring):** The change freeze remains in effect for 24 hours after the cutover completes. The system is monitored for any anomalies. Trend data is compared to pre-cutover baselines. If the system is stable at T+24, the change freeze is lifted and normal operations resume.

I have had field engineers push back on the 48-hour freeze. "It's just a minor change." "It won't affect the cutover." I have heard it all. My answer is the same every time: if it is minor enough that it will not affect the cutover, it is minor enough that it can wait until T+24. The change freeze exists because every "minor change" I have ever seen cause a cutover failure was described as minor before it caused the failure.

---

## FAT/SAT Coordination Between Vendors

Factory Acceptance Testing and Site Acceptance Testing are where integration either gets verified or gets discovered to be broken. The difference depends entirely on how the tests are structured.

**The problem with vendor FATs in isolation:** Each vendor FATs their own equipment against their own specification. The BAS vendor tests their controllers against BACnet communications. The EPMS vendor tests their power meters against Modbus registers. The SCADA vendor tests their RTAC against simulated field devices. Every vendor passes their FAT. Nobody has tested whether the BAS controller can talk to the EPMS meter through the SCADA network using the actual firewall rules that will exist on site.

**The integrated FAT:** On programs where I have the authority to structure the commissioning plan, I require an integrated FAT before any equipment ships. The BAS vendor, the EPMS vendor, and the SCADA integrator set up their equipment in the same room, connected to the same network architecture that will be deployed on site — including firewalls, VLANs, and the actual switch configurations. Then we test the integrated system.

This is more expensive than isolated FATs. It requires vendors to coordinate schedules. It requires the OT/IT integrator to provide network equipment for the test. It adds two to four weeks to the equipment delivery schedule.

It is also the single most effective risk mitigation in the entire commissioning plan. I have seen integrated FATs catch firewall rule conflicts, protocol version mismatches, register map errors, and timing issues that would have taken weeks to diagnose in the field. Two days in a vendor's shop saves two weeks on site. The math is not complicated.

**SAT as verification, not discovery:** If the integrated FAT was done correctly, the SAT should confirm what was already proven — not discover new problems. The SAT verifies that the equipment survived shipping, that the field wiring is correct, that the site network infrastructure matches the FAT configuration, and that the end-to-end system performs in the actual environment.

When the SAT becomes a discovery process — "oh, this doesn't work with the site firewall" — it means the FAT was incomplete. That is a planning failure, not a field failure. I track it accordingly.

---

## BAS/EPMS/SCADA Integration Challenges in Data Centers

Data centers are the most demanding OT/IT integration environment I work in, because every system must be integrated and every system is live. There is no "we'll fix it during the next outage" in a facility that has contractual uptime SLAs of 99.999%.

**BAS (Building Automation System):** Controls HVAC, lighting, fire alarm monitoring, leak detection, access control — everything that keeps the building operational. In a hyperscale data center, the BAS is managing thousands of points: CRAHs, chillers, AHUs, humidifiers, UPS environmental monitoring, generator building ventilation. The protocol is typically BACnet/IP on the OT network.

**EPMS (Electrical Power Monitoring System):** Monitors every electrical distribution component — utility switchgear, generators, ATSs, UPSs, PDUs, RPPs. The EPMS provides real-time power, voltage, current, power factor, and harmonic data. The protocol is typically Modbus TCP or DNP3, again on the OT network.

**SCADA:** The supervisory layer that aggregates BAS, EPMS, and other subsystem data into a unified operator interface. The SCADA head-end provides alarm management, trending, historical data logging, and the single-pane-of-glass view that the facility operations team uses to manage the building.

The integration challenge is that these three systems are typically provided by three different vendors, installed by three different subcontractors, and commissioned by three different teams. The BAS vendor has never seen the EPMS vendor's equipment. The SCADA integrator has a specification that describes what data they need from both systems, but the specification was written by an engineer who may or may not have verified the actual register maps of the actual equipment that was procured.

**The most common failures I see:**

1. **Point name mismatches.** The SCADA specification says the point name for UPS-1 output voltage is "UPS1_Vout." The EPMS meter exposes the register as "UPS-01_OutputVoltage_PhA." The SCADA integrator's database mapping fails. Multiply this by 3,000 points across the facility and you have a weeks-long debugging effort.

2. **Scaling factor errors.** The power meter sends a raw register value of 4,801. The SCADA database expects this to represent 480.1V with a scaling factor of 0.1. But the meter was configured with a scaling factor of 1.0, so the value is actually 4,801V, which triggers every high-voltage alarm in the system. I have seen this happen on a live data center where the false alarms caused a cascade of automated responses that nearly took a cooling system offline.

3. **Polling rate conflicts.** The SCADA system polls the BAS at 5-second intervals. The BAS gateway can handle 50 simultaneous connections. But the EPMS system also needs to be polled through the same gateway because of a network architecture decision made six months ago, and now the gateway is overloaded and dropping packets. Communications become intermittent. The control room sees devices flashing between online and offline status. Nobody trusts the data.

4. **Firewall rule gaps.** The network team implemented the firewall rules from the design document, which was written before the BAS vendor changed their controller model. The new controller uses a different port for BACnet/IP discovery (port 47808 instead of the default 47808 — same port, but the new controller also requires port 47809 for a proprietary management interface that was not in the original design). The controller cannot be managed remotely. The BAS tech has to walk to every controller on a 400,000 square foot campus to make configuration changes.

**My approach:** I require a complete point-to-point communication verification matrix before the integrated systems test. Every SCADA point is traced from the field device through the network to the head-end. The verification includes point name, scaling factor, engineering units, alarm limits, and update rate. This matrix is the acceptance document. If a point is not on the matrix, it is not in scope. If a point is on the matrix and it does not work, it is a deficiency that blocks IST completion.

---

## Camp Lejeune: BAS/Controls Upgrades Across 200+ Buildings

Let me ground this in a real program that illustrates every integration challenge I have described.

Marine Corps Base Camp Lejeune — a DoD installation with over 200 buildings requiring BAS and controls modernization. The scope included removing legacy pneumatic and DDC controls and replacing them with modern BACnet-based BAS controllers, installing new fiber backbone infrastructure, deploying new control racks, and integrating everything into a campus-wide facility management system.

**The scale challenge.** Two hundred buildings is not one project — it is two hundred individual integrations. Every building has different mechanical equipment, different vintages of existing controls, different wiring conditions, and different occupancy requirements. The temptation is to create a single standard template and deploy it across every building. The reality is that every building requires a customized point mapping, customized programming, and customized commissioning.

**The network backbone.** We deployed new fiber backbone infrastructure tying the buildings into self-healing ring networks. This meant coordinating fiber installation with the base's existing IT infrastructure — because the OT network for the BAS had to be logically and physically separated from the base's IT network per DoD cybersecurity requirements, but both networks used portions of the same physical cable pathway infrastructure.

The coordination required joint planning sessions between our controls team, the base's IT department, and the base's cybersecurity office. Every fiber route was documented. Every patch panel was labeled. Every cross-connect was approved before installation. The cybersecurity office had to verify that the OT network could not be reached from the IT network at any point in the topology.

**The control rack deployments.** New control racks in 200+ buildings means 200+ individual commissioning events. Each rack contains BAS controllers, network switches, power supplies, I/O modules, and fiber terminations. Each rack must be individually commissioned: power verified, network connectivity confirmed, controller programmed and tested, I/O points verified against the wiring diagrams, and end-to-end communication to the head-end confirmed.

We developed a standardized commissioning procedure for the racks, but — critically — we included building-specific sections for the unique equipment in each facility. The standardized section covered the common elements (power, network, controller boot-up). The building-specific section covered the equipment-specific I/O testing and functional performance verification.

**The integration sequencing.** You cannot commission 200 buildings simultaneously. You commission them in a sequence that respects the network topology — because each building connects to the ring, and you need the upstream portions of the ring to be operational before you can verify end-to-end communication for downstream buildings.

We divided the campus into ring segments and commissioned building-by-building along each ring. When a ring segment was complete, we ran an integrated test of the entire segment — verifying that every building on the ring could communicate with the head-end, that failover scenarios (simulated fiber breaks) were handled correctly, and that the head-end could see all points from all buildings on the segment.

**The lesson.** The OT/IT integration on a program like Camp Lejeune is not a single event — it is a sustained discipline applied consistently across hundreds of individual integrations. The standard procedures, the communication matrix, the change-freeze protocols, the joint verification gates — all of them scale. You just have to be disciplined enough to apply them every single time, regardless of whether it is building number 3 or building number 187.

---

## Remote Well Sites and Distributed SCADA Integration

The OT/IT integration challenge takes a different form on distributed infrastructure — oil and gas well sites, remote pump stations, water treatment outfalls, and similar facilities spread across large geographic areas.

On these programs, the field devices are miles apart, connected by fiber, cellular, or radio links to a central SCADA host. The self-healing ring architecture is still the backbone, but now the ring spans miles instead of meters. Latency matters. Bandwidth is constrained. And when something fails at a remote site, you are not walking down the hall to check a switch — you are driving 45 minutes or dispatching a technician who may not arrive until the next day.

I have tied remote well sites into self-healing rings where the fiber run between adjacent nodes was eight miles. The ring convergence time on a fiber cut was under 50ms — the remote site never lost communication with the SCADA host. But achieving that performance required meticulous attention to the switch configurations, the spanning tree protocol settings, and the fiber link budget calculations.

**The integration discipline for remote sites:**

**Pre-deployment factory staging.** Every remote site's equipment — RTU, switch, I/O modules, radio or cellular modem — is staged in the shop and connected to the SCADA host before it ships to the field. The entire communication path is tested end-to-end. Every point is verified. Every alarm is confirmed. When the equipment arrives at the remote site, the field technician's job is mechanical installation and wiring — the integration is already proven.

**Site-specific communication surveys.** Before deploying any radio or cellular link, we conduct an RF survey at the site to verify signal quality, interference, and available bandwidth. I have seen programs skip this step and discover on commissioning day that the cellular modem cannot maintain a reliable connection because the site is in a coverage dead zone. That is a mobilization wasted and a schedule slip created by skipping a half-day survey.

**Redundant communication paths.** For critical remote sites, I specify dual communication paths — primary fiber and backup cellular, or primary radio and backup satellite. The SCADA host automatically fails over if the primary path drops. The operator sees an alarm, not a data gap.

**Remote firmware management.** This is where OT/IT discipline is non-negotiable. Firmware updates to remote RTUs must be tested in the shop on identical hardware before they are pushed to the field. I have seen a single firmware update brick 12 remote RTUs simultaneously because the update was pushed to the production network without shop testing. Twelve sites went dark. Twelve technicians had to mobilize. The cost of not testing in the shop was 12x the cost of testing.

---

## Keeping Every System State Known

The overarching discipline — the one that connects all of these specific practices — is **state awareness**. From the first isolation to the final re-energization, every system state must be known, documented, and verified.

This means:

**Before you touch anything, you document the current state.** Every switch port configuration is backed up. Every relay setting file is archived. Every BAS controller program is exported. Every firewall rule set is saved. If the integration goes wrong, you have a known-good state to restore to. This is your rollback plan, and it is non-negotiable.

**During execution, every change is logged in real time.** Changed a VLAN assignment? Logged. Updated a firewall rule? Logged. Modified a relay setting? Logged. Added a BAS point? Logged. The log includes the timestamp, the person who made the change, the system affected, the specific parameter changed, the old value, and the new value. This is not overhead — this is the diagnostic trail that lets you find the root cause when something breaks at 2 AM during a cutover.

**After completion, the final state is documented and verified.** The as-built documentation reflects the actual configuration of every system, not the design intent. The as-built is verified by the person who made the changes and a second party who independently confirms the configuration. Discrepancies between the as-built and the actual configuration are deficiencies that must be resolved before turnover.

I carry this discipline from the nuclear power world. In a reactor plant, the position of every valve, the status of every breaker, the setting of every controller is known at all times. The operator can tell you the plant state in any given moment, because the documentation system requires real-time status tracking. That level of rigor may seem excessive for a BAS upgrade or a SCADA deployment. It is not. The difference between a program that delivers on time and a program that spirals into months of troubleshooting is almost always traceable to a moment where someone changed something and did not document it.

---

## Why the OT/IT Handoff Is Where Most Programs Fail

I want to be explicit about why this particular boundary creates so many failures, because understanding the root cause is the only way to prevent it.

**Organizational silos.** The electrical team, the controls team, and the IT team report through different chains. They have different project managers, different superintendents, and different QA/QC processes. Integration requires all three to operate as a single team, but the project structure treats them as independent scopes.

**Specification gaps.** The design engineer specifies the electrical system. A different engineer specifies the controls system. A different engineer specifies the network system. Each specification is internally consistent. None of them are verified against each other for interface compatibility. The integration requirements fall in the gaps between specifications.

**Schedule pressure.** Integration testing takes time. When the schedule compresses — and it always compresses — integration testing is the first activity that gets cut. "We'll figure it out during startup." That is the most expensive sentence in the construction industry.

**Competency gaps.** The electrician who can terminate 15kV cable in their sleep has never configured a managed switch. The network engineer who can design a zero-trust VLAN architecture has never touched a protection relay. The controls technician who can program a BAS controller has never read a relay coordination study. Integration requires people who can work across all three domains, or at minimum, who can communicate effectively across the boundaries. Those people are rare.

**My role on every program is to be the bridge.** I speak electrical. I speak controls. I speak network. I have pulled cable, programmed relays, configured switches, and troubleshot SCADA communications. When the electrical team says "the relay is working" and the network team says "the network is working" and the system is not working, I can diagnose which side of the boundary the problem lives on — because I have worked on both sides.

That cross-domain competency is the single most valuable skill in mission-critical infrastructure today. The systems are converging. The electrical distribution, the building automation, the power monitoring, the SCADA, and the enterprise IT network are all becoming a single integrated system. The industry needs people who can integrate them, not just install them.

---

## The Playbook: Preventing the OT/IT Ambush

Here is the distilled version — the actions that prevent integration failures on every program.

1. **Joint integration planning from day one.** The electrical, controls, and OT/IT teams must participate in a joint kick-off meeting where the integration requirements are defined, the interface points are identified, and the communication matrix is started. This happens before mobilization, not during commissioning.

2. **Single communication matrix.** One document. All IP addresses, all protocol parameters, all register maps, all polling intervals. Jointly owned by all disciplines. Version-controlled. Updated in real time. This is the single most important document in any OT/IT integration.

3. **Integrated FAT.** Test the systems together in the shop before they ship to the field. Two days in a vendor's shop saves two weeks on site.

4. **Joint hold points in the commissioning plan.** Fiber acceptance testing, network infrastructure verification, end-to-end communication testing — all of these are joint activities that require sign-off from both the E&I team and the OT/IT team.

5. **Change-freeze protocol.** Forty-eight hours before any cutover, all configurations are frozen and documented. No exceptions.

6. **State documentation at every phase.** Before, during, and after every integration activity, the system state is documented. Current state, changes made, final state.

7. **Cross-domain competency.** If you cannot find one person who speaks all three languages (electrical, controls, network), then establish a standing integration meeting where all three disciplines are represented and integration issues are resolved in real time. Do not let integration issues sit in email chains between discipline leads. They will die there.

8. **Post-integration monitoring.** Twenty-four hours of monitored operation after every integration milestone. Compare live data to expected baselines. Verify alarm integrity. Confirm trend logging. Do not declare victory until the data confirms it.

---

## The Takeaway

The OT/IT handoff is not a technical problem. It is an organizational discipline problem. The technology works — self-healing rings, SEL RTACs, BACnet/IP, Modbus TCP, IEC 61850 — all of it is proven and reliable when properly deployed.

What fails is the coordination between the people deploying it. The electrician who does not tell the network engineer about a power feed change. The controls tech who does not update the communication matrix after a controller swap. The network engineer who pushes a firmware update without testing it in the shop first. The project manager who cuts integration testing from the schedule to save two days.

Every one of those failures is preventable. Every one of them comes down to the same principle: treat integration as a discipline, not an afterthought.

From Camp Lejeune's 200-building BAS modernization to remote well site SCADA rings spanning miles of fiber — the playbook is the same. Joint planning. Shared documentation. Change control. State awareness. Cross-domain competency. Relentless verification.

Bridge the gap, or the gap will swallow your schedule, your budget, and your reputation.

---

*Shane Thomas Strough is an Integration and Commissioning Leader with 15+ years across DoD, federal, aerospace, hyperscale data center, and industrial infrastructure. Founder of Elevare Edge LLC. Builder of systems — electrical, digital, and human.*

*Connect at [shanestrough.com](https://shanestrough.com) · [LinkedIn](https://www.linkedin.com/in/shane-thomas-strough/) · [Podcast](https://shanestrough.com/podcast.html)*
