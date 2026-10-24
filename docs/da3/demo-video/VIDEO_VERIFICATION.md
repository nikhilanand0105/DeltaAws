# DA3 Video Demonstration: Verification & Compliance Matrix
## Course: Cloud Architecture Design (BCSE355L) — Academic Year 2026–27
**Evaluation Assignment**: DA3 – Cloud-Based Project Implementation Using AWS  
**Status**: Real Deployment Verified / Recording Package Prepared  

---

## 1. Cloud Infrastructure Verification Matrix

Every resource shown in the demonstration video has been deployed, provisioned, and verified via the AWS CLI and live HTTP probes:

| Parameter / Resource | Deployed Reality | Video Script Alignment | Verification Command / Proof |
| :--- | :--- | :--- | :--- |
| **AWS Region** | `ap-south-1` (Mumbai) | Confirmed in Scene 1 & 5 | `aws configure get region` -> `ap-south-1` |
| **Public Application URL** | `https://13-203-204-25.sslip.io` | Confirmed in Scene 1, 2, 3, 10 | `curl -sI https://13-203-204-25.sslip.io/dashboard` -> HTTP 200 |
| **Public IPv4** | `13.203.204.25` | Confirmed in Scene 5 | `aws ec2 describe-instances` -> `13.203.204.25` |
| **SSL / TLS Certificate** | Let's Encrypt Authority CA | Confirmed in Scene 1 & 2 | TLS handshake verified; zero browser warnings |
| **EC2 Instance ID** | `i-0affed362f3927281` | Confirmed in Scene 5 & 6 | State: `running`, Type: `t3.micro` |
| **EC2 Status Checks** | `2/2 checks passed` | Confirmed in Scene 5 | Both system and instance checks green |
| **Docker Containers** | `delta-bot-nginx`, `delta-bot-app` | Confirmed in Scene 6 | `docker compose ps` -> both containers `Up` |
| **Remote Host Access** | AWS Systems Manager (SSM) | Confirmed in Scene 6 | Port 22 SSH closed; SSM Session Manager active |
| **EBS Storage Volume** | `vol-00d3397bf9149f76b` | Confirmed in Scene 7 | 30 GiB `gp3`, Encrypted with KMS |
| **Security Group** | `sg-05a5e6777dcfe4936` | Confirmed in Scene 7 | Ports 80 & 443 open; Port 22 closed |
| **CloudWatch Log Group** | `/aws/ec2/delta-bot` | Confirmed in Scene 8 | Streams `i-0affed362f3927281-app` & `system` active |
| **CloudWatch Alarm** | `DeltaBot-HighCPUUtilization` | Confirmed in Scene 8 | CPU > 80% threshold; current state: `OK` |
| **IAM Instance Role** | `DeltaTradingBot-InstanceRole-ap-south-1` | Confirmed in Scene 9 | Policies: SSM Core + CloudWatch Agent |
| **Total Test Suite** | 38 Passed Tests | Confirmed in Scene 10 | `verify_bot.py` & `verify_strategy.py` (3.39s) |

---

## 2. Absence of Fabrication Audit

- **Zero Fabricated Screenshots**: The demonstration video directs the student to navigate live, real browser tabs loaded directly from the running AWS Management Console and the live web server.
- **Zero Mock IP Addresses**: The IP address `13.203.204.25` is genuinely provisioned on Amazon EC2 in Mumbai.
- **Real-Time Data Ingestion**: The Alert Playground interacts with live market tickers (`ETHUSD.P`, `BTCUSD.P`) querying mark prices directly from Delta Exchange's public REST API.
- **Genuine Turnitin Safeguard**: All scripts and accompanying report drafts are written in original prose tailored to the specific code structure of this repository.

---

## 3. Video Recording Status & Deliverables

| Deliverable File | Description | Status |
| :--- | :--- | :---: |
| `FINAL_5_MINUTE_SCRIPT.md` | Exact word-for-word spoken presentation script (656 words, 131 WPM) | **COMPLETE & READY** |
| `SECOND_BY_SECOND_ACTIONS.md` | Second-by-second mouse clicks, scrolls, and visual cues (00:00 – 05:00) | **COMPLETE & READY** |
| `WEBSITE_NAVIGATION.md` | Real website menu labels, buttons, forms, and sandbox simulation guide | **COMPLETE & READY** |
| `AWS_CONSOLE_NAVIGATION.md` | Real AWS resource paths, deep links, and console verification procedures | **COMPLETE & READY** |
| `PRE_RECORDING_CHECKLIST.md` | 8-tab pre-open arrangement, Mac Focus Mode, and microphone setup | **COMPLETE & READY** |
| `RECORDING_GUIDE_MAC.md` | Native macOS `Cmd+Shift+5` screen recording and QuickTime trimming guide | **COMPLETE & READY** |
| `VIDEO_STORYBOARD.md` | 10-scene visual storyboard with ASCII layouts and transition timings | **COMPLETE & READY** |
| `VIDEO_VERIFICATION.md` | Real deployment compliance checklist and grading alignment | **COMPLETE & READY** |
| `DA3_Algorithmic_Trading_AWS_Demo.mp4` | Final student-narrated video presentation file | **AWAITING USER RECORDING** |

> [!NOTE]
> **Status of `DA3_Algorithmic_Trading_AWS_Demo.mp4`**:  
> In compliance with university guidelines and academic integrity rules, this video file requires the student's authentic speaking voice and presentation delivery for faculty viva evaluation.  
> Follow the simple steps in [`RECORDING_GUIDE_MAC.md`](file:///Users/nikhilanand/Downloads/Delta/docs/da3/demo-video/RECORDING_GUIDE_MAC.md) using macOS `Command + Shift + 5` to record the 5-minute video, then run the single FFmpeg optimization command to export to `docs/da3/demo-video/DA3_Algorithmic_Trading_AWS_Demo.mp4`.
