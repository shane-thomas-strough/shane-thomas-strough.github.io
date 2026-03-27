# Siemens Building Automation Systems
## Data Center Commissioning — Field Guide
**Cx Boot Camp Training Series · Session 3**
**Author: Shane Thomas Strough**

---

## SESSION 3 AGENDA

| Left Column | Right Column |
|---|---|
| 01 — Siemens Product Family Overview | 01 — Siemens Fire Alarm Systems |
| 02 — Desigo CC Platform | 02 — Cerberus PRO Deep Dive |
| 03 — APOGEE Platform | 03 — Fire Alarm Commissioning Protocol |
| 04 — Siemens Controllers | 04 — Integration Between BAS and FA |
| 05 — BACnet Implementation | 05 — Common Fault Conditions |
| 06 — Modbus Integration | 06 — Tools and Software |
| 07 — Siemens on the Data Center Floor | 07 — Exercise — Group Discussion |
| 08 — Commissioning Workflow | |

---

## CHAPTER 1 — Siemens Product Family Overview

Siemens Building Technologies is one of the most widely deployed building automation and fire safety platforms in mission-critical facilities worldwide. In data center commissioning you will encounter Siemens products on virtually every large project — understanding their architecture, terminology, and integration methods is non-negotiable field knowledge.

**The Two Primary Platforms You Will Encounter:**

**Desigo CC** — The current-generation integrated building management platform. Desigo CC is Siemens' flagship product for large mission-critical facilities. It integrates HVAC, fire safety, access control, and power monitoring under a single operator interface. Most new data center builds specify Desigo CC.

**APOGEE** — The legacy platform. Many existing data centers and retrofit projects still run APOGEE. You will encounter APOGEE on existing facility upgrades and expansions. Understanding both platforms is required for full-scope commissioning work.

> **Critical field note:** Do not assume a Siemens installation is Desigo CC just because the hardware is new. Verify the platform before you begin. APOGEE and Desigo CC have different commissioning workflows, different software tools, and different integration methods.

---

## CHAPTER 2 — Desigo CC Platform

**What Is Desigo CC?**

Desigo CC (Command and Control) is Siemens' integrated building management platform designed for large, complex facilities. In data center applications it serves as the central operations hub — aggregating data from HVAC controllers, fire alarm panels, electrical systems, and access control into a single operator workstation.

**Core Architecture:**

**Management Station (Server)**
The Desigo CC server runs the core software platform. All data from field controllers and subsystems aggregates here. The server hosts the engineering environment, the operator interface, and the historical data archive. In large data centers there will typically be a primary server and a redundant standby server.

**Operator Workstation**
The client interface where operators monitor and control the facility. Multiple workstations can connect to a single Desigo CC server. The operator workstation displays system graphics, alarm lists, trend logs, and event history.

**Field Controllers**
Desigo CC communicates with field-level controllers via BACnet/IP, BACnet MS/TP, or proprietary Siemens protocols depending on the hardware generation. Controllers handle local control logic and communicate data to the management station.

**Integration Engine**
Desigo CC includes native integration capabilities for BACnet, Modbus, OPC, LON, and SNMP. This is what makes it valuable in data centers — it can aggregate data from chillers, UPS systems, PDUs, and precision cooling units regardless of manufacturer.

---

## Desigo CC — Key Features for Data Center Commissioning

**System Manager**
The engineering environment within Desigo CC. This is where points are configured, graphics are built, and control logic is programmed. During commissioning you will use System Manager to verify point configurations, check engineering unit assignments, and confirm alarm setpoints.

**Trend Logs**
Desigo CC maintains configurable trend logs for all monitored points. During commissioning verify that trend logs are configured for all critical points — supply air temperature, chilled water supply and return, differential pressure, UPS battery temperature. Trend data is the primary tool for performance verification after systems are running.

**Alarm Management**
Desigo CC uses a structured alarm hierarchy. Alarms are categorized by priority — Life Safety, Critical, Major, Minor, Warning. During commissioning verify that every alarm is assigned the correct priority and that routing to the correct operator group is configured. A life safety alarm routed to the wrong group is a commissioning deficiency.

**Graphics and Floor Plans**
Desigo CC supports custom system graphics and floor plan overlays. During acceptance testing the owner will expect to see accurate system graphics that match the installed equipment. Verify all graphics against the as-built equipment layout before acceptance.

---

## CHAPTER 3 — APOGEE Platform

**What Is APOGEE?**

APOGEE is Siemens' legacy building automation platform. It remains widely deployed in existing facilities and will be encountered on data center retrofits, expansions, and upgrade projects. APOGEE uses a hierarchical architecture with three distinct levels.

**APOGEE Architecture — Three Levels:**

**Level 3 — Insight Workstation**
The operator interface and engineering workstation for APOGEE systems. Insight software runs on Windows and provides system monitoring, alarm management, trending, and programming access. This is your primary tool for APOGEE commissioning.

**Level 2 — Field Panel Controllers**
APOGEE field panels handle local control for HVAC and mechanical systems. Common APOGEE field panels encountered in data centers:

| Panel | Description |
|---|---|
| MEC (Modular Equipment Controller) | Controls individual mechanical equipment — air handlers, chillers, cooling towers |
| REC (Remote Equipment Controller) | Smaller controller for terminal equipment |
| TEC (Terminal Equipment Controller) | Zone-level control for VAVs, FCUs |
| PXCM (PXC Modular) | Newer generation BACnet native controller |
| PXC36 / PXC64 / PXC128 | PXC series — number indicates IO point capacity |

**Level 1 — Field Devices**
Sensors, actuators, valves, and dampers that connect directly to field panel IO. Same device types as discussed in Session 2 — temperature sensors, pressure transmitters, flow meters, differential pressure sensors.

---

## APOGEE — Commissioning Workflow

**Step 1: Establish Communication with Insight**
Connect laptop to the APOGEE network. Launch Insight software. Verify communication to all field panels — a panel shown offline in Insight is the first item to resolve before any other commissioning activity.

**Step 2: Verify Point Database**
Every physical IO point must have a corresponding point in the Insight database. Verify:
- Point name matches MEPiL tag
- Engineering units are correct
- Range calibration matches instrument submittal
- Alarm setpoints match design documents

**Step 3: Verify Field Wiring**
Cross-reference each point in Insight against the field installation using loop drawings. Force outputs and verify field response. Read inputs and verify correct engineering unit display.

**Step 4: Verify Control Logic**
Review APOGEE programming against the Sequence of Operation. Every control sequence must be tested and documented. Do not rely on the programmer's word that the logic is correct — test every sequence under real conditions.

**Step 5: Trend Verification**
Enable trend logs for critical points. Allow the system to run for a minimum of 24 hours before acceptance. Review trend data to verify stable operation within design parameters.

---

## CHAPTER 4 — Siemens Controllers

**Current Generation — PXC Series (BACnet Native)**

The PXC (Process Controller) series is Siemens' current-generation BACnet native controller family. PXC controllers are the most commonly specified Siemens controllers on new data center projects.

| Controller | IO Capacity | Typical Application |
|---|---|---|
| PXC36-E.D | 36 IO points | Terminal equipment, small AHUs |
| PXC64-E.D | 64 IO points | Medium AHUs, pump skids |
| PXC128-E.D | 128 IO points | Large AHUs, chiller plants |
| PXC200-E.D | 200 IO points | Central plant controllers |

**PXC Communication Ports:**
- Ethernet port — BACnet/IP communication to management station
- RS-485 port — BACnet MS/TP communication to field bus devices
- USB port — local programming and diagnostics

**PXC LED Indicators — Know These:**

| LED | Color/State | Meaning |
|---|---|---|
| RUN | Green solid | Controller operating normally |
| RUN | Green flashing | Controller in startup or download mode |
| ERR | Red solid | Hardware fault — requires service |
| ERR | Red flashing | Application fault — check programming |
| COM | Yellow flashing | Active communication on BACnet port |
| COM | Yellow solid | Communication fault |

> **Field tip:** When you approach a Siemens PXC controller the first thing you check is the LED status. A red ERR LED stops all other commissioning activity on that controller until resolved.

---

## PXC Controller — BACnet Object Types

Every point on a PXC controller is represented as a BACnet object. During commissioning you will read and write BACnet objects to verify correct operation.

**Core BACnet Object Types on PXC Controllers:**

| Object Type | Abbreviation | Use |
|---|---|---|
| Analog Input | AI | Physical analog input — 4-20mA, 0-10VDC, RTD |
| Analog Output | AO | Physical analog output — valve command, VFD speed |
| Analog Value | AV | Software calculated value — setpoints, calculated temperatures |
| Binary Input | BI | Physical binary input — run status, alarm contact |
| Binary Output | BO | Physical binary output — start/stop command |
| Binary Value | BV | Software binary value — enable/disable flags |
| Multi-State Value | MSV | Multi-position status — system operating mode |
| Schedule | SCH | Time-based scheduling object |
| Calendar | CAL | Holiday and special day scheduling |
| Trend Log | TL | Historical data collection object |
| Notification Class | NC | Alarm routing configuration |

---

## Legacy Controllers — APOGEE MEC/REC/TEC

**MEC — Modular Equipment Controller**
The MEC is the primary APOGEE field controller for mechanical equipment. MECs use proprietary Siemens P1 or P2 bus communication to the Insight workstation. Key things to know during commissioning:

- MEC address must match the address configured in Insight — address switches are physically set on the controller board
- MEC programming is stored in battery-backed SRAM — a dead battery means lost programming
- Always verify battery condition on legacy MECs before commissioning — a dead battery during testing is a project delay
- MEC IO expansion modules extend the point count — verify all expansion modules are communicating before point verification begins

**REC — Remote Equipment Controller**
Smaller version of the MEC for terminal equipment. Same communication protocol. Same battery consideration.

**TEC — Terminal Equipment Controller**
Zone-level controller for VAVs and fan coil units. TECs typically communicate via MS/TP bus back to a MEC or directly to an APOGEE network controller.

---

## CHAPTER 5 — BACnet Implementation on Siemens Systems

**BACnet on Siemens — What You Need to Know**

Siemens implements BACnet/IP and BACnet MS/TP in accordance with ASHRAE Standard 135. However, Siemens also implements proprietary extensions and features that affect commissioning. Understanding the difference between standard BACnet behavior and Siemens-specific behavior prevents troubleshooting dead-ends.

**Siemens BACnet Device IDs**
Every BACnet device requires a unique Device Instance (Device ID) on the network. On Siemens PXC controllers the Device ID is configured in the programming tool. During commissioning verify:
- No duplicate Device IDs on the network — duplicates will cause one or both devices to go offline
- Device ID matches the project documentation
- Device ID range falls within the owner's defined numbering scheme

**BACnet/IP — Network Configuration**
PXC controllers communicate BACnet/IP over standard Ethernet. Required configuration:
- Static IP address assigned — DHCP is not recommended for controllers in mission-critical environments
- Subnet mask matches the BAS network segment
- UDP port 47808 (0xBAC0) must be open on any network equipment between controllers and the management station
- BACnet/IP Broadcast Management Device (BBMD) configured if controllers and servers are on different IP subnets

**BACnet MS/TP — Field Bus Configuration**
MS/TP is a serial RS-485 bus used for field-level devices. Key parameters:
- Baud rate — 9600, 19200, 38400, or 76800 bps — must match all devices on the same MS/TP segment
- MAC address — unique address for each device on the MS/TP segment, range 0-127 for masters
- Max Master — sets the highest MAC address the token will be passed to — set this correctly or the bus wastes time polling nonexistent addresses
- Max Info Frames — number of data frames a device can send when it holds the token

> **Common MS/TP commissioning fault:** Baud rate mismatch between devices on the same segment. One device at 38400 and another at 19200 will prevent communication. Verify baud rate on every device before troubleshooting anything else.

---

## BACnet Discovery and Verification Tools

During Siemens BACnet commissioning you will need tools to verify device communication and object values independent of the Siemens software. These tools are your independent verification layer.

**YABE — Yet Another BACnet Explorer**
Free open-source BACnet browser. Run on your laptop to discover all BACnet devices on the network, read object values, and write to writeable objects. Essential for:
- Verifying a PXC controller is online before opening Desigo CC or Insight
- Reading point values independently of the Siemens management software
- Confirming BACnet object names match project documentation

**BACnet Stack Tools**
Siemens provides BACnet diagnostic tools within the engineering software. Use these for advanced diagnostics but always verify independently with YABE first.

**Wireshark with BACnet Dissector**
For network-level BACnet troubleshooting. Captures BACnet/IP packets on the Ethernet network. Use when a device appears offline in software but the physical connection is verified — the packet capture will show whether BACnet traffic is reaching the management station.

---

## CHAPTER 6 — Modbus Integration on Siemens Systems

**When You Will Encounter Modbus on Siemens Projects**

Siemens controllers natively speak BACnet. Modbus appears in data center BAS projects when integrating third-party equipment that does not support BACnet:
- Older chiller models
- UPS systems and battery monitoring
- Power distribution units (PDUs)
- Generator controls
- Chemical feed systems
- Some precision cooling units

Siemens PXC controllers support Modbus RTU (RS-485 serial) and Modbus TCP (Ethernet) as integration protocols. The PXC acts as the Modbus Master — it polls the third-party device (Modbus Slave) for data.

---

## Modbus Integration — Commissioning Checklist

**Before Connecting:**
- Obtain the Modbus register map from the equipment manufacturer — this document defines every available data point, its register address, data type, and scaling factor
- Verify the communication parameters — baud rate, parity, stop bits, slave address (RTU) or IP address and port (TCP)
- Verify the Siemens controller has the correct Modbus driver loaded in its programming

**Verifying Modbus Communication:**
Use Modbus Poll software on your laptop to independently verify communication with the Modbus slave device before attempting integration through the Siemens controller. If Modbus Poll cannot read the device, the Siemens controller will not be able to either — resolve the communication issue at the device level first.

**Common Modbus Register Types:**

| Register Type | Address Range | Access | Data Type |
|---|---|---|---|
| Coil | 00001-09999 | Read/Write | Boolean (0/1) |
| Discrete Input | 10001-19999 | Read Only | Boolean (0/1) |
| Input Register | 30001-39999 | Read Only | 16-bit integer |
| Holding Register | 40001-49999 | Read/Write | 16-bit integer |

**Scaling and Engineering Units:**
Modbus registers contain raw integer values. The register map will define the scaling factor required to convert the raw value to engineering units. Example: a chiller leaving water temperature register returns a value of 445. The register map states the scaling factor is 0.1°F. Actual temperature = 44.5°F.

Verify every scaled engineering unit value during commissioning — a wrong scaling factor produces plausible-looking data that is factually incorrect and will cause the control system to operate incorrectly.

---

## CHAPTER 7 — Siemens on the Data Center Floor

**Typical Siemens Scope on a Hyperscale Data Center Build**

On a large data center project you will encounter Siemens equipment across multiple system types. Understanding the full scope prevents gaps during commissioning planning.

**Cooling Plant Integration**
- Chiller plant — supply/return water temperatures, flow, differential pressure, chiller status and alarms
- Cooling tower — fan status, basin temperature, conductivity, blowdown valve
- Primary/secondary pump skids — VFD speed, run status, differential pressure, flow
- Heat exchangers — approach temperature monitoring, isolation valve status

**Precision Cooling**
- CRAHs and CRACs — supply/return air temperature, humidity, fan speed, cooling capacity, alarm status
- Most precision cooling units communicate via BACnet or Modbus — verify protocol with submittal before commissioning begins
- In-row cooling units — same integration approach as CRAHs

**Environmental Monitoring**
- Temperature and humidity sensors in data halls — typically hardwired AI points to Siemens IO modules
- Leak detection panels — binary input to BAS indicating leak alarm
- Airflow stations — analog input for CFM measurement

**Electrical System Integration**
- Generator status and fuel level — Modbus or hardwired binary inputs
- UPS status and battery parameters — typically Modbus TCP
- Automatic Transfer Switch (ATS) position — hardwired binary inputs
- Power Distribution Units (PDUs) — SNMP or Modbus

**Life Safety**
- Fire alarm system interface — hardwired dry contact or network integration (covered in detail in Chapter 9)
- Access control — typically separate Siemens platform (Siemens SiPass or equivalent)

---

## Data Center Commissioning Sequence — Siemens Systems

**Phase 1 — Pre-Functional Checks**
Before any functional testing begins:
- Verify Desigo CC or Insight server is online and communicating with all field controllers
- Verify all field controllers show online and error-free in the management software
- Verify all IO points are reading in the management software
- Verify all trend logs are configured and recording
- Verify all alarm setpoints are configured per design documents
- Verify all graphics are accurate to the as-built installation

**Phase 2 — Point-by-Point Verification**
Working from the MEPiL:
- For every analog input: verify correct engineering unit value at a known condition
- For every analog output: command output and verify field device responds correctly
- For every binary input: verify correct on/off status at field device
- For every binary output: command on/off and verify field device responds correctly
- Document every verified point in the commissioning log

**Phase 3 — Sequence of Operation Testing**
- Test every control sequence defined in the Sequence of Operation
- Test normal operating sequences under actual load conditions
- Test all failure scenarios — simulate equipment failures and verify failover behavior
- Test all alarm conditions — verify alarms appear in correct priority in management software and route to correct operator group
- Document every tested sequence with pass/fail result

**Phase 4 — Integrated Systems Testing**
- Verify communication between Siemens BAS and all integrated third-party systems
- Simulate fire alarm conditions and verify BAS response (fan shutdown, damper positions, door releases)
- Verify power failure response — test UPS transfer and verify BAS continues to operate
- Verify generator start sequence and BAS response

**Phase 5 — Trend and Performance Verification**
- Allow systems to operate for minimum 24-72 hours under design conditions
- Review trend data for all critical points — temperature stability, pressure stability, humidity control
- Document any deviations from design parameters
- Verify all trend logs are archiving correctly to the management station

---

## CHAPTER 8 — Common Siemens Fault Conditions

**Know these before you go to the field. Most commissioning delays come from one of these.**

---

**Fault 1: Controller Offline in Management Software**

Possible causes:
- Network connectivity issue — check Ethernet cable, switch port, IP configuration
- Duplicate Device ID on network — use YABE to scan for duplicates
- Controller in fault state — check ERR LED on controller
- Firewall blocking UDP port 47808 — verify with network team
- Controller IP address conflict — verify no other device has same IP

Troubleshooting sequence:
1. Ping the controller IP from your laptop — if no response, network issue
2. If ping succeeds, open YABE — if controller appears, software configuration issue
3. If controller appears in YABE but not in Desigo CC, check Device ID and network routing configuration

---

**Fault 2: Point Reading Incorrect Value**

Possible causes:
- Wrong input type configured — AI configured as 4-20mA receiving 0-10VDC signal
- Wrong range configured — transmitter range set to 0-100 PSI but device is 0-200 PSI
- Wiring error — signal wired to wrong terminal
- Bad sensor — sensor failed or out of calibration
- Scaling error — engineering unit conversion factor incorrect

Troubleshooting sequence:
1. Verify input type in controller programming matches loop drawing
2. Verify range in controller programming matches equipment submittal
3. Use multimeter to measure raw signal at controller terminal
4. Compare raw signal to expected value at known condition
5. If raw signal is correct but engineering unit value is wrong — programming error
6. If raw signal is wrong — field wiring or sensor issue

---

**Fault 3: Output Not Responding**

Possible causes:
- Output commanded but field device not wired correctly
- Overridden output — Siemens controllers allow manual overrides that prevent normal control
- Output in wrong mode — manual vs automatic
- Interlock preventing operation — safety interlock holding output off
- Actuator or valve issue — mechanical failure in field device

Troubleshooting sequence:
1. Verify output value in controller programming — is it being commanded?
2. Check for active overrides in Desigo CC or Insight — release any manual overrides
3. Measure output signal at controller terminal with multimeter
4. If signal is correct at controller terminal, trace wiring to field device
5. Verify field device receives signal and responds mechanically

---

**Fault 4: MS/TP Bus Communication Failure**

Possible causes:
- Baud rate mismatch between devices
- Duplicate MAC addresses on bus segment
- Incorrect termination — RS-485 bus requires 120-ohm termination resistors at each end
- Wiring fault — polarity reversal on RS-485 A/B conductors
- Bus too long — RS-485 maximum recommended length is 4000 feet

Troubleshooting sequence:
1. Verify baud rate on all devices on the segment
2. Verify MAC addresses — no duplicates
3. Verify termination resistors are installed at both physical ends of the bus
4. Check A/B polarity — swap if reversed
5. Use Wireshark to capture MS/TP traffic and verify token passing

---

**Fault 5: Alarm Not Appearing in Management Software**

Possible causes:
- Alarm not configured — point exists but no alarm object created
- Wrong Notification Class assigned — alarm routes to wrong operator group
- Alarm suppressed — inhibit flag active on the point
- Setpoint not configured — alarm threshold set to wrong value
- Communication gap — controller offline when alarm occurred

Troubleshooting sequence:
1. Verify alarm object exists for the point in the programming
2. Verify Notification Class assignment routes to correct operator group
3. Check for active alarm inhibits on the point
4. Verify alarm setpoint matches design documents
5. Force the condition to trigger the alarm and trace its path through the system

---

## CHAPTER 9 — Siemens Fire Alarm Systems

**Product Families — What You Will Encounter**

Siemens has two primary fire alarm product families deployed in data center applications:

**Cerberus PRO**
Siemens' current-generation intelligent fire alarm platform. Cerberus PRO is the most commonly specified Siemens fire alarm system on new data center construction. It supports addressable detection, aspirating smoke detection (ASD), suppression system monitoring, and integration with the BAS.

**Sinteso (European market designation)**
Equivalent to Cerberus PRO for international projects. You will encounter Sinteso on global data center builds. Same commissioning approach as Cerberus PRO with minor regional differences.

**FireFinder XLS**
Legacy Siemens fire alarm platform. Still widely deployed in existing facilities and retrofit projects. If you are commissioning a fire alarm system on an existing data center, verify which platform is installed before proceeding.

> **Critical note:** Fire alarm commissioning requires licensed fire alarm technicians in most jurisdictions. As a BAS integrator your role is typically limited to verifying the integration between the fire alarm system and the BAS — not commissioning the fire alarm system itself. Always verify scope of work and licensing requirements before touching fire alarm equipment.

---

## Cerberus PRO — System Architecture

**Central Controller — FC722 / FC724**
The Cerberus PRO central controller is the brain of the fire alarm system. It processes detector data, manages alarm conditions, controls output devices, and communicates with the BAS. In large data centers multiple FC controllers may be networked together in a peer-to-peer ring topology for redundancy.

**Loop Controllers**
Cerberus PRO uses addressable detection loops. Each loop controller manages a circuit of addressable devices — smoke detectors, heat detectors, manual call points, and modules. Each device on the loop has a unique address.

**Addressable Devices**
Every detector and module on a Cerberus PRO system has a unique address set during installation. The address determines:
- Where the device appears on the system graphics
- What zone and area it belongs to
- What outputs activate when it alarms

**Network Communication**
Cerberus PRO communicates to the BAS via:
- Hardwired dry contact outputs — the most reliable and most common method
- BACnet/IP — available on newer Cerberus PRO versions via network interface module
- OPC — available via Siemens integration module
- Desigo CC native integration — when both systems are Siemens, native integration provides the richest data exchange

---

## Cerberus PRO — Detector Types in Data Centers

**Standard Addressable Smoke Detectors**
Photo-electric and ionization detectors mounted in ceiling spaces. Standard detection for general areas — corridors, offices, electrical rooms.

**Aspirating Smoke Detection (ASD) — Very Early Warning**
ASD systems (also called VESDA — Very Early Smoke Detection Apparatus) are the primary detection technology in data hall spaces. ASD systems actively draw air samples through a pipe network to a detection chamber. They detect smoke at concentrations far below what standard detectors respond to.

In data centers the ASD pipe network typically runs through the ceiling space and under the raised floor. Commissioning ASD systems involves:
- Verifying all sampling ports are open and unobstructed
- Verifying correct airflow through the system (measured in liters per minute)
- Verifying alarm threshold settings — Alert, Action, Fire 1, Fire 2
- Performing smoke sensitivity testing at the sampling ports
- Verifying integration to fire alarm panel and BAS

**Linear Heat Detection**
Heat-sensitive cable deployed in cable trays and under raised floors. When the cable reaches its rated temperature it creates a short circuit that the panel detects as an alarm.

**Flame Detectors**
UV/IR flame detectors in areas with high fire risk — generator rooms, diesel storage, battery rooms. Verify field of view covers the target area and that no obstructions block the detector.

---

## Fire Alarm Commissioning Protocol — Data Centers

**Pre-Commissioning Requirements**
- Verify all detection devices are installed and addressed per the fire alarm drawing package
- Verify all output devices — bells, strobes, door holders, suppression system interface — are installed
- Verify fire alarm panel programming is loaded and matches the design documents
- Verify all notification appliance circuits are wired and balanced
- Obtain copies of the fire alarm drawing package, device address list, and sequence of operations

**Point-by-Point Testing**
Every addressable device must be individually tested. For each device:
- Verify the device address matches the drawing
- Activate the device (introduce smoke, heat, or use test magnet per device type)
- Verify the correct device identification appears at the panel
- Verify the correct zone and area designation
- Verify correct output activation per the Sequence of Operations
- Document the test result

**ASD System Testing**
- Verify airflow readings at sampling ports against design specifications
- Introduce aerosol test smoke at the sampling port furthest from the detection unit — this is the worst-case scenario for detection sensitivity
- Verify the system detects at the correct alarm threshold
- Verify integration to fire alarm panel triggers at correct threshold

**Integrated Systems Testing**
This is where BAS commissioning and fire alarm commissioning intersect. Verify:
- Fire alarm signal reaches BAS correctly — hardwired contact or network integration
- BAS responds correctly to fire alarm signal — fan shutdown sequence, damper positions, elevator recall
- HVAC smoke control sequences activate correctly
- All smoke dampers go to correct position on alarm
- Suppression system pre-action sequence operates correctly — verify with suppression contractor

**Documentation Requirements**
- Completed point-by-point test forms for every device
- ASD system flow test results
- Integrated systems test results
- Any deficiencies noted and resolved
- Certificate of completion signed by licensed fire alarm technician

---

## CHAPTER 10 — BAS and Fire Alarm Integration

**This is the most critical integration point on any data center project.**

The interface between the Building Automation System and the Fire Alarm System must be verified completely before any occupied testing or owner acceptance.

**Integration Methods — Ranked by Reliability:**

**1. Hardwired Dry Contact (Most Reliable)**
The fire alarm panel provides dry contact outputs that signal the BAS. The BAS monitors these contacts as binary inputs. When the fire alarm activates, the contact closes, the BAS detects the change, and executes the smoke control sequence.

This method is the most reliable because it is the simplest. No network dependency. No software handshake. Just a contact open or closed.

During commissioning verify:
- Contact status reads correctly in the BAS under normal conditions
- Contact status changes correctly when fire alarm activates
- BAS executes correct sequence within required time when contact changes

**2. BACnet Integration (Richest Data)**
When both systems are capable, BACnet integration provides more detailed alarm information — specific zone, specific device, alarm type. The fire alarm panel exposes BACnet objects that the BAS reads via BACnet/IP.

This method provides more data but adds network dependency. Always verify that hardwired backup contacts exist for critical functions — never rely solely on network integration for life safety functions.

**3. OPC Integration**
OPC server on the fire alarm system communicates with OPC client on the BAS. Provides good data exchange but adds software dependency. Use hardwired contacts for critical outputs.

---

## Smoke Control Sequences — What the BAS Must Do

When a fire alarm activates in a data center, the BAS must execute specific smoke control sequences. These sequences are defined in the life safety section of the design documents and must be tested completely before owner acceptance.

**Typical Data Center Smoke Control Requirements:**

**General Alarm — Full Building**
- All supply fans — verify response per design (typically shutdown or switch to smoke purge mode)
- All return and exhaust fans — verify response per design
- All smoke dampers — verify drive to correct position (open or closed per design intent)
- All stairwell pressurization fans — verify activation
- Elevator recall — verify coordination with elevator contractor
- Emergency lighting — verify activation

**Data Hall Specific Alarm**
- Precision cooling units — verify response per design (some designs require CRACs to continue operating during fire alarm to prevent equipment overheating)
- Raised floor supply dampers — verify position
- Pre-action suppression system interface — verify sequence with suppression contractor
- Data hall exhaust — verify activation for smoke purge if designed

**Suppression System Pre-Discharge Warning**
- Audible/visual warning devices — verify activation
- Time delay — verify correct delay period before suppression discharge
- Abort switch function — verify abort capability works correctly
- Personnel egress verification — coordinate with fire alarm contractor

> **Critical note:** The smoke control sequence in a data center is more complex than a standard commercial building because the equipment being protected (servers and storage) generates significant heat that must be managed even during a fire event. Some precision cooling units are designed to continue operating during a fire alarm. Verify the design intent for every piece of equipment before accepting the smoke control sequence as correct.

---

## CHAPTER 11 — Tools and Software

**Required Software for Siemens Commissioning:**

**Desigo CC Engineering Software**
The Siemens engineering environment for Desigo CC. Used for all programming, configuration, and diagnostics on Desigo CC systems. Requires Siemens training and authorization. Obtain credentials and software access before arriving on site.

**Insight Workstation Software**
The engineering and operator interface for APOGEE systems. Windows-based. Obtain installation media and license before commissioning begins.

**XWP — Extended Workstation Programming**
The programming tool for APOGEE field panel controllers (MEC, REC, TEC). Used to load and verify controller programming. Required for any APOGEE field panel troubleshooting.

**Cerberus PRO Engineering Tool (FS720)**
The programming and diagnostic software for Cerberus PRO fire alarm systems. Used by licensed fire alarm technicians. As a BAS integrator you will use this in a read-only capacity to verify integration point status.

**Field Diagnostics Tools:**

| Tool | Use |
|---|---|
| YABE (BACnet Explorer) | Independent BACnet device discovery and point verification |
| Modbus Poll | Independent Modbus register reading and verification |
| Wireshark | Network packet capture for BACnet/IP and Modbus TCP diagnostics |
| PuTTY | Serial terminal for RS-485 diagnostics |
| Siemens Service Tool (handheld) | Local controller diagnostics without laptop |

**Test Equipment:**

| Equipment | Use |
|---|---|
| Multimeter | Signal verification, continuity testing, voltage measurement |
| 4-20mA Loop Calibrator | Simulate and verify analog input signals |
| RS-485 Line Analyzer | MS/TP bus diagnostics, signal quality measurement |
| Network Cable Tester | Ethernet wiring verification |
| Laptop with USB-to-RS485 adapter | Serial communication with legacy controllers |

---

## CHAPTER 12 — Exercise — Group Discussion

Using the Siemens system documentation provided for your project, work through the following:

**1 — Platform Identification**
Identify which Siemens platform is installed on your project — Desigo CC or APOGEE. What evidence tells you which platform you have? What are the first three things you verify before beginning commissioning on that platform?

**2 — Controller Verification**
Identify all Siemens PXC controllers on the project. For each controller:
- What is the Device ID?
- What is the IP address?
- How many IO points does it have?
- What equipment does it control?
- What is the current LED status?

**3 — BACnet Point Verification**
Using YABE, discover all BACnet devices on the BAS network. For each device:
- Does it appear in YABE?
- Does the Device ID match the project documentation?
- Select three points on each controller and verify the value matches field conditions

**4 — Fire Alarm Integration**
Identify the fire alarm to BAS interface on your project:
- What integration method is used — hardwired or network?
- Where are the hardwired contacts terminated in the BAS?
- What BAS sequence activates on general fire alarm?
- What BAS sequence activates on data hall alarm?
- Have the sequences been tested?

**5 — Discussion Questions**
- You discover a PXC controller with a red ERR LED. What are your first three diagnostic steps?
- A Modbus-integrated UPS is not showing data in Desigo CC. What is your troubleshooting sequence?
- The fire alarm triggers but the precision cooling units do not respond as designed. Who do you call first?

---

## CORE PRINCIPLE — Siemens Is the Platform. You Are the Commissioning Agent.

Siemens provides the tools, the controllers, the software, and the integration capability. Your job is to verify that what was designed is what was installed, and that what was installed actually works.

The Siemens platform does not commission itself. The programming does not verify itself. The integration does not test itself.

You do that.

With the drawings. With the tools. With the methodical process covered in this session and every session before it.

When you sign off on a Siemens-controlled system in a data center, you are making a statement that the cooling plant, the environmental monitoring, the fire alarm integration, and the smoke control sequences will perform as designed when the facility is running at full capacity and something goes wrong.

**Something will always go wrong eventually.**

Your commissioning work is the reason it doesn't become a catastrophe when it does.

---

## You are not just here to check systems.
## You are here to make them work — and make them last.

**Siemens Building Automation Systems**
**Data Center Commissioning Field Guide**
**Shane Thomas Strough**
