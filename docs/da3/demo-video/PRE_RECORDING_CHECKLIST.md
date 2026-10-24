# DA3 Video Demonstration: Pre-Recording Checklist
## Course: Cloud Architecture Design (BCSE355L) — Academic Year 2026–27
**Target Video Duration**: Exactly 5:00 (300 seconds ± 2 seconds)  
**Target Video Format**: MP4 (H.264 / AAC), 1080p (1920 × 1080), 30 fps  
**Hardware & OS**: Apple Mac (macOS Sonoma / Sequoia / Ventura)  

---

## 1. Browser & Display Environment Setup

- [ ] **Browser Choice**: Use Google Chrome or Brave (clean profile with zero third-party visual extension badges).
- [ ] **Display Resolution**: Set Mac display scaling to **1920 × 1080** (or record a 1920×1080 fixed window) to guarantee razor-sharp 1080p rendering without blurry downsampling.
- [ ] **Browser Zoom Level**: Reset browser zoom to exactly **100%** (`Command + 0`) on all tabs.
- [ ] **Hide Bookmarks Bar**: Press `Command + Shift + B` to hide the bookmarks bar, maximizing clean vertical viewport space.
- [ ] **Hide Downloads Bar**: Ensure no download shelves or extension popups are visible at the bottom of the window.

---

## 2. Notification & Privacy Safeguards (Mac Focus Mode)

- [ ] **Enable Mac "Do Not Disturb"**:
  - Open Mac **Control Center** (top-right menu bar) -> Click **Focus** -> Select **Do Not Disturb** -> Set to **On**.
  - This prevents iMessage, WhatsApp, Slack, or email notifications from sliding onto the screen during recording.
- [ ] **Close Background Apps**: Quit Mail, Telegram, WhatsApp, Discord, and Spotify to avoid unexpected sound effects or notification chimes.
- [ ] **Clean Desktop**: If recording the full screen, ensure desktop icons and personal folders are hidden or moved off the main display.

---

## 3. Audio & Microphone Verification

- [ ] **Microphone Selection**:
  - Open **System Settings** -> **Sound** -> **Input**.
  - Select your preferred microphone (e.g. MacBook Pro Built-in Mic or external USB headset).
  - Speak a few sentences at your normal presentation volume. Ensure the input level meter consistently registers between 60% and 75% (solid green without hitting red clipping distortion).
- [ ] **Room Acoustics**: Record in a quiet room with doors and windows closed. Turn off loud fans or air conditioners to eliminate background hiss.
- [ ] **Microphone Distance**: Position your microphone approximately 6 to 8 inches from your mouth, slightly off-axis to avoid plosive breath pops ("p" and "b" sounds).

---

## 4. Pre-Open the 8 Browser Tabs in Exact Order

To eliminate loading delays and navigation errors, open these 8 tabs in a single browser window **before pressing record**:

| Tab # | Page / Service | Exact Pre-Loaded URL | Desired State Before Recording |
| :---: | :--- | :--- | :--- |
| **1** | **Trading Dashboard** | `https://13-203-204-25.sslip.io/dashboard` | Loaded on `Accounts` tab. Scrolled to top header. |
| **2** | **Amazon EC2** | [EC2 Instance Details](https://ap-south-1.console.aws.amazon.com/ec2/home?region=ap-south-1#InstanceDetails:instanceId=i-0affed362f3927281) | Row `i-0affed362f3927281` selected. Bottom details panel open. |
| **3** | **AWS SSM Terminal** | [Session Manager](https://ap-south-1.console.aws.amazon.com/systems-manager/managed-instances/i-0affed362f3927281/overview?region=ap-south-1) | Active shell open. Run `cd /opt/delta-bot` so terminal is ready. |
| **4** | **Amazon EBS** | [EBS Volume Details](https://ap-south-1.console.aws.amazon.com/ec2/home?region=ap-south-1#VolumeDetails:volumeId=vol-00d3397bf9149f76b) | Row `vol-00d3397bf9149f76b` selected. Details showing 30 GiB Encrypted. |
| **5** | **Security Groups** | [Security Group Details](https://ap-south-1.console.aws.amazon.com/ec2/home?region=ap-south-1#SecurityGroup:groupId=sg-05a5e6777dcfe4936) | `sg-05a5e6777dcfe4936` selected. **Inbound rules** tab visible. |
| **6** | **CloudWatch Logs** | [Log Stream Viewer](https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1#logsV2:log-groups/log-group/$252Faws$252Fec2$252Fdelta-bot) | Log group open. Click into stream `i-0affed362f3927281-app`. |
| **7** | **CloudWatch Alarms** | [Alarm Details](https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1#alarmsV2:alarm/DeltaBot-HighCPUUtilization) | Alarm `DeltaBot-HighCPUUtilization` open showing green `OK` status. |
| **8** | **AWS IAM Roles** | [IAM Role Console](https://console.aws.amazon.com/iam/home#/roles/details/DeltaTradingBot-InstanceRole-ap-south-1) | Role details open. **Permissions** tab visible showing managed policies. |

---

## 5. Live Application State Check

- [ ] Open a separate terminal or test tab to verify that the application returns HTTP 200:
  ```bash
  curl -sI https://13-203-204-25.sslip.io/health
  ```
  Should return: `HTTP/2 200`
- [ ] On Tab 1 (`Trading Dashboard`):
  - Click `Check Balance` once to warm up the mock balance cache.
  - Switch to `Alert Playground`, verify dropdowns default to `ETHUSD.P` and `BUY`.
  - Switch to `Performance Analytics`, verify the ApexCharts equity curve renders cleanly.
  - Return to the `Accounts` tab and scroll back to the very top.

---

## 6. Rehearsal & Pacing Benchmarks

Before the final recording take, do a complete dry run with a stopwatch or phone timer. Use these cumulative milestone checkpoints:

| Target Timestamp | Milestone Script Checkpoint | Acceptable Range |
| :---: | :--- | :---: |
| **00:25** | Finishing introductory title & objectives | 00:23 – 00:27 |
| **01:05** | Finishing "Check Balance" and account explanations | 01:00 – 01:08 |
| **01:50** | Finishing "Run Simulation" and Performance Analytics | 01:45 – 01:52 |
| **02:15** | Finishing Cloud Architecture summary (transitioning to AWS) | 02:10 – 02:18 |
| **02:50** | Finishing EC2 Console demonstration (`t3.micro`, 2/2 checks) | 02:45 – 02:53 |
| **03:20** | Finishing SSM terminal output (`docker compose ps`) | 03:15 – 03:23 |
| **03:50** | Finishing EBS (30 GiB gp3) and Security Group (port 22 closed) | 03:45 – 03:53 |
| **04:20** | Finishing CloudWatch Logs (`app` stream) & Alarm (`OK`) | 04:15 – 04:23 |
| **04:40** | Finishing IAM role & Free Tier cost breakdown | 04:35 – 04:42 |
| **05:00** | Final closing statement on the live trading dashboard | **04:56 – 05:02** |

---

## 7. Post-Recording Verification Steps

- [ ] Play back the recorded video immediately with headphones.
- [ ] Confirm your voice is crisp, audible, and synchronized with screen actions.
- [ ] Confirm video duration is between **04:55 and 05:05**.
- [ ] Confirm that no passwords, API keys, or unwanted personal notifications were captured.
