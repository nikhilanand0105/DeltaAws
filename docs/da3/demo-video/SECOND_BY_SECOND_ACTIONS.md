# DA3 5-Minute Video: Second-by-Second Actions Guide
## Course: Cloud Architecture Design (BCSE355L) — Academic Year 2026–27
**Target Duration**: 00:00 to 05:00 (300 Seconds)  
**Resolution**: 1920 × 1080 (16:9 Full HD)  
**Browser Setup**: Google Chrome / Brave with 8 Pre-Opened Tabs  

---

## Tab Index Reference

- **Tab 1**: Trading Application Dashboard (`https://13-203-204-25.sslip.io/dashboard`)
- **Tab 2**: AWS EC2 Instances Console (`ap-south-1` Mumbai)
- **Tab 3**: AWS Systems Manager Session Manager (Terminal Shell)
- **Tab 4**: AWS EBS Volumes Console (`vol-00d3397bf9149f76b`)
- **Tab 5**: AWS Security Groups Console (`sg-05a5e6777dcfe4936`)
- **Tab 6**: AWS CloudWatch Log Groups (`/aws/ec2/delta-bot`)
- **Tab 7**: AWS CloudWatch Alarms (`DeltaBot-HighCPUUtilization`)
- **Tab 8**: AWS IAM Roles Console (`DeltaTradingBot-InstanceRole-ap-south-1`)

---

## Detailed Second-by-Second Action Matrix

| Time Window | Active Tab / Screen | Action Type | Exact UI Target | Mouse Position | Visible State on Screen | Spoken Cue / Technical Concept |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **00:00 – 00:08** | Tab 1 | Remain Still | Top Header / URL Bar | Center Top | Browser shows `https://13-203-204-25.sslip.io/dashboard` with valid lock icon. | "Good morning, respected faculty. I am Nikhil Anand..." |
| **00:08 – 00:16** | Tab 1 | Slow Hover | Lock icon in URL bar | URL bar left | SSL Certificate details tooltip ("Connection is secure"). | Let's Encrypt CA certificate verification without self-signed warnings. |
| **00:16 – 00:25** | Tab 1 | Move Cursor | Header Navigation Bar | Nav links area | View of "Accounts", "Trades & PnL", "Performance Analytics". | Introduction of BCSE355L DA3 project title & objectives. |
| **00:25 – 00:35** | Tab 1 | Hover | Account Card #1 | Center-left card | "Alpha Momentum Fund (Paper)" card details: Leverage 50x, Buffer 80%. | Multi-tenant portfolio risk segregation. |
| **00:35 – 00:45** | Tab 1 | Click Button | Button: `Check Balance` | Account #1 Button | Button shows loading spinner, then pops toast "Balance: $25.40 USD". | Live async API call to Flask backend (`/api/accounts/1/balance`). |
| **00:45 – 00:55** | Tab 1 | Slow Scroll | Account Cards 2, 3, 4 | Center Screen | Cards for "Delta Grid & Arbitrage", "Institutional Swing Pool", "Retail Vault". | Diverse position sizing rules (Percentage vs Fixed Margin). |
| **00:55 – 01:05** | Tab 1 | Click Tab | Nav: `Alert Playground` | Top Nav (6th item) | Screen switches to `#playground` tab; Alert form and payload box appear. | Switching to external webhook simulation. |
| **01:05 – 01:15** | Tab 1 | Hover / Select | Select: `play-ticker` | Ticker Dropdown | `ETHUSD.P (Ether Perpetual)` selected, Action set to `BUY`. | Ingestion of TradingView synthetic alerts. |
| **01:15 – 01:25** | Tab 1 | Click Button | Button: `Run Simulation` (`#trigger-sandbox-btn`) | Blue Primary Button | Button turns disabled ("Running simulation..."), `#sandbox-console` clears. | Safe sandboxed execution trigger via `/api/simulate-webhook`. |
| **01:25 – 01:38** | Tab 1 | Highlight Text | `#sandbox-console` | Inside black console | Console displays green success marks: "Simulated successfully: BUY 86266 lots...". | Deterministic multi-account position sizing calculation. |
| **01:38 – 01:45** | Tab 1 | Click Tab | Nav: `Performance Analytics` | Top Nav (3rd item) | `#analytics` panel displays KPI cards (Win Rate 75%, Sharpe 3.30). | Empirical strategy metrics derived from historical trades. |
| **01:45 – 01:50** | Tab 1 | Smooth Scroll | `#chart-equity` | Mid-page | Interactive ApexCharts cumulative equity curve and drawdown graph. | Quantitative portfolio risk visualization. |
| **01:50 – 02:02** | Tab 1 | Click Tab | Nav: `Global Settings` | Top Nav (7th item) | Webhook URL and rate-limiting configuration visible. | Transitioning to cloud architecture explanation. |
| **02:02 – 02:15** | Tab 1 | Hover | Webhook URL Input Field | Center Form | Displaying `https://13-203-204-25.sslip.io/webhook`. | Architectural overview: Nginx reverse proxy + Gunicorn WSGI. |
| **02:15 – 02:22** | Switch to Tab 2 | Click Tab Header | Chrome Tab 2 (EC2) | Browser Tab Bar | AWS EC2 Instances list in `ap-south-1` appears. | Switching to AWS Management Console. |
| **02:22 – 02:35** | Tab 2 | Click Row | Row `i-0affed362f3927281` | Table Checkbox / ID | Row is highlighted; bottom detail pane opens. | Demonstrating EC2 compute resource ID and running state. |
| **02:35 – 02:45** | Tab 2 | Hover | Instance Type `t3.micro` | Bottom Details Tab | Highlighting 1 vCPU, 1 GiB memory, Status Checks `2/2 passed`. | Free Tier compute selection (750 hours/month). |
| **02:45 – 02:50** | Tab 2 | Hover | Public IPv4 `13.203.204.25` | Bottom Details Tab | Highlighting matching IP address to the live application. | Direct elastic ingress without expensive ALB. |
| **02:50 – 02:56** | Switch to Tab 3 | Click Tab Header | Chrome Tab 3 (SSM) | Browser Tab Bar | AWS Systems Manager Session Manager terminal prompt appears. | Secure host administration without port 22 SSH. |
| **02:56 – 03:08** | Tab 3 | Type Command | Terminal Prompt | Console Input | Type: `docker compose ps` and press `Enter`. | Querying Docker container runtime on EC2 host. |
| **03:08 – 03:20** | Tab 3 | Highlight Output | Terminal Output Area | Console Output | Highlight `delta-bot-nginx (Up)` and `delta-bot-app (Up)`. | Verifying multi-container microservice isolation. |
| **03:20 – 03:26** | Switch to Tab 4 | Click Tab Header | Chrome Tab 4 (EBS) | Browser Tab Bar | Amazon EBS Volumes Console appears. | Transition to cloud persistence. |
| **03:26 – 03:35** | Tab 4 | Click Row | Volume `vol-00d3397bf9149f76b` | Table Row | Details pane shows 30 GiB, Type `gp3`, Encrypted `True`. | 30 GiB Free Tier EBS storage & AES-256 KMS encryption. |
| **03:35 – 03:40** | Switch to Tab 5 | Click Tab Header | Chrome Tab 5 (SG) | Browser Tab Bar | Security Groups console for `sg-05a5e6777dcfe4936`. | Network perimeter security. |
| **03:40 – 03:50** | Tab 5 | Hover / Scroll | Inbound Rules Table | Center Table | Show Port 80 (HTTP) and Port 443 (HTTPS). Show NO Port 22 rule. | Least-privilege ingress hardening against brute-force attacks. |
| **03:50 – 03:56** | Switch to Tab 6 | Click Tab Header | Chrome Tab 6 (CW Logs) | Browser Tab Bar | CloudWatch Log Group `/aws/ec2/delta-bot`. | Observability and monitoring. |
| **03:56 – 04:08** | Tab 6 | Click Stream | Stream `i-0affed362f3927281-app`| Table Link | Log viewer opens showing real-time Gunicorn request logs and GET /health. | Real-time application log ingestion via CloudWatch Agent. |
| **04:08 – 04:14** | Switch to Tab 7 | Click Tab Header | Chrome Tab 7 (CW Alarm) | Browser Tab Bar | CloudWatch Alarm `DeltaBot-HighCPUUtilization`. | Proactive health monitoring. |
| **04:14 – 04:20** | Tab 7 | Hover | Status Badge `OK` | Alarm Details | Show metric CPUUtilization > 80% with green `OK` status badge. | Automated threshold alarms for compute resource limits. |
| **04:20 – 04:26** | Switch to Tab 8 | Click Tab Header | Chrome Tab 8 (IAM) | Browser Tab Bar | IAM Role `DeltaTradingBot-InstanceRole-ap-south-1`. | Identity and access management. |
| **04:26 – 04:34** | Tab 8 | Scroll Down | Permissions Policies Table | Center Page | Policies: `AmazonSSMManagedInstanceCore` & `CloudWatchAgentServerPolicy`. | Least-privilege instance profile; zero long-term static credentials. |
| **04:34 – 04:40** | Tab 8 | Remain Still | Role Summary Card | Center Page | Point out lack of administrative privileges or root access. | Free Tier cost efficiency (~₹4.20 total demo expense). |
| **04:40 – 04:46** | Switch to Tab 1 | Click Tab Header | Chrome Tab 1 (Dashboard) | Browser Tab Bar | Return to trading dashboard home screen. | Seamless narrative transition back to working application. |
| **04:46 – 04:54** | Tab 1 | Click Tab | Nav: `Trades & PnL` | Top Nav (2nd item) | Closed Position History table displays completed trades and PnL. | Empirical results and academic deliverable validation. |
| **04:54 – 05:00** | Tab 1 | Scroll to Top | Header / Brand Title | Center Screen | Final clean view of live application; mouse cursor stationary. | "Thank you for your time, and I welcome any questions." |

---

## Cursor Movement & Screen Hygiene Best Practices
1. **Never Fidget with the Mouse**: When speaking without performing an action, park the mouse pointer in a neutral area (e.g. upper right corner or margin) so it does not distract the viewer.
2. **Smooth Linear Trajectories**: Move the mouse in straight, deliberate lines directly toward target buttons. Avoid rapid circular motions.
3. **Respect Tab Switch Pauses**: Allow 0.5 to 1 second after switching tabs before starting the next narration sentence so the audience visually registers the new AWS console page.
4. **Clean Address Bar**: Keep the browser address bar clean and bookmark bar minimal.
