# DA3 Video Demonstration: AWS Console Navigation Guide
## Course: Cloud Architecture Design (BCSE355L) — Academic Year 2026–27
**Target Region**: `ap-south-1` (Asia Pacific - Mumbai)  
**AWS Account ID**: Mask or blur if feasible, or ensure no root credentials / secret keys are displayed  
**CloudFormation Stack**: `delta-trading-bot-stack`  

---

## Direct Deep Links & Quick Reference Table

| Service / Resource | Resource Identifier | Console Direct URL |
| :--- | :--- | :--- |
| **Amazon EC2 Instances** | `i-0affed362f3927281` | [EC2 Instance Details](https://ap-south-1.console.aws.amazon.com/ec2/home?region=ap-south-1#InstanceDetails:instanceId=i-0affed362f3927281) |
| **AWS Systems Manager** | Fleet Manager / Session Manager | [SSM Managed Instances](https://ap-south-1.console.aws.amazon.com/systems-manager/managed-instances/i-0affed362f3927281/overview?region=ap-south-1) |
| **Amazon EBS Storage** | `vol-00d3397bf9149f76b` | [EBS Volume Details](https://ap-south-1.console.aws.amazon.com/ec2/home?region=ap-south-1#VolumeDetails:volumeId=vol-00d3397bf9149f76b) |
| **Security Groups** | `sg-05a5e6777dcfe4936` | [Security Group Details](https://ap-south-1.console.aws.amazon.com/ec2/home?region=ap-south-1#SecurityGroup:groupId=sg-05a5e6777dcfe4936) |
| **CloudWatch Log Group** | `/aws/ec2/delta-bot` | [CloudWatch Log Group](https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1#logsV2:log-groups/log-group/$252Faws$252Fec2$252Fdelta-bot) |
| **CloudWatch Alarms** | `DeltaBot-HighCPUUtilization` | [CloudWatch Alarm](https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1#alarmsV2:alarm/DeltaBot-HighCPUUtilization) |
| **AWS IAM Instance Role** | `DeltaTradingBot-InstanceRole-ap-south-1` | [IAM Role Console](https://console.aws.amazon.com/iam/home#/roles/details/DeltaTradingBot-InstanceRole-ap-south-1) |

---

## Detailed Step-by-Step Navigation & On-Screen Explanations

### 1. Amazon EC2 Compute Infrastructure (Tab 2)
- **Direct Link**: `https://ap-south-1.console.aws.amazon.com/ec2/home?region=ap-south-1#InstanceDetails:instanceId=i-0affed362f3927281`
- **Navigation Path in Console**:
  1. Open the search bar in the AWS header and type `EC2`.
  2. Select **Instances** in the left sidebar menu under the "Instances" section.
  3. Verify that the region selector in the top right is set to **Mumbai (ap-south-1)**.
  4. In the instances table, select the row named `delta-trading-bot-stack-TradingBotInstance-...` with ID `i-0affed362f3927281`.
- **What to Highlight on Screen**:
  - **Instance State**: `Running` (Green badge).
  - **Status Checks**: `2/2 checks passed` (System check and Instance check operational).
  - **Instance Type**: `t3.micro` (1 vCPU, 1 GiB memory, burstable CPU architecture).
  - **Public IPv4 Address**: `13.203.204.25`.
- **Key Narration Points**:
  - The `t3.micro` qualifies for the **750 hours/month Free Tier** allowance.
  - The single-instance deployment avoids unnecessary Application Load Balancers (saving ~$18/month) and NAT Gateways (saving ~$32/month).

---

### 2. AWS Systems Manager (SSM) Session Manager (Tab 3)
- **Direct Link**: `https://ap-south-1.console.aws.amazon.com/systems-manager/managed-instances/i-0affed362f3927281/overview?region=ap-south-1`
- **Navigation Path in Console**:
  1. Search for `Systems Manager` in the top search bar.
  2. In the left navigation, click **Session Manager** (under *Node Management*).
  3. Click the orange button: **Start session**.
  4. Select instance `i-0affed362f3927281` and click **Start session**. A browser-based Linux terminal shell opens.
- **Safe Commands to Execute on Video**:
  ```bash
  cd /opt/delta-bot
  docker compose ps
  ```
- **What Appears on Screen**:
  ```
  NAME              IMAGE          COMMAND                  SERVICE   CREATED          STATUS          PORTS
  delta-bot-app     delta-bot-app  "gunicorn --bind 0.0…"   app       40 minutes ago   Up 40 minutes   5000/tcp
  delta-bot-nginx   nginx:alpine   "/docker-entrypoint.…"   nginx     40 minutes ago   Up 40 minutes   0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
  ```
- **Optional Quick Health Probe**:
  ```bash
  curl -s http://localhost:5000/health
  ```
  Output: `{"service":"delta-webhook-bot","status":"healthy"}`
- **Key Narration Points**:
  - **Zero Open Inbound Ports for Admin**: Host management is achieved entirely over an outbound TLS tunnel via AWS SSM. Port 22 SSH is completely unnecessary and blocked.
  - **Container Isolation**: Docker Compose encapsulates the Gunicorn WSGI server and Nginx reverse proxy, ensuring seamless reproducibility and clean process isolation.

---

### 3. Amazon EBS Persistent Storage (Tab 4)
- **Direct Link**: `https://ap-south-1.console.aws.amazon.com/ec2/home?region=ap-south-1#VolumeDetails:volumeId=vol-00d3397bf9149f76b`
- **Navigation Path in Console**:
  1. Return to the EC2 dashboard.
  2. In the left sidebar, click **Volumes** (under *Elastic Block Store*).
  3. Select volume `vol-00d3397bf9149f76b`.
- **What to Highlight on Screen**:
  - **Volume State**: `In-use` (attached to `i-0affed362f3927281` as `/dev/xvda`).
  - **Size**: `30 GiB`.
  - **Volume Type**: `gp3` (General Purpose SSD with 3,000 baseline IOPS and 125 MB/s throughput).
  - **Encryption**: `Encrypted` (using AWS KMS default managed key `aws/ebs`).
- **Key Narration Points**:
  - 30 GiB is 100% covered under the AWS Free Tier storage quota (30 GiB-months free).
  - The volume persistently stores the application's SQLite database (`local.db`), container state, logs, and a 2.0 GiB swapfile that expands total virtual memory to 3.0 GiB on `t3.micro`.

---

### 4. AWS Security Groups & Network Perimeter (Tab 5)
- **Direct Link**: `https://ap-south-1.console.aws.amazon.com/ec2/home?region=ap-south-1#SecurityGroup:groupId=sg-05a5e6777dcfe4936`
- **Navigation Path in Console**:
  1. In the EC2 left sidebar, click **Security Groups** (under *Network & Security*).
  2. Select `sg-05a5e6777dcfe4936` (`delta-trading-bot-stack-TradingBotSecurityGroup-...`).
  3. Click the **Inbound rules** tab in the bottom details panel.
- **What to Highlight on Screen**:
  - **Inbound Rule 1**: Type `HTTP`, Protocol `TCP`, Port `80`, Source `0.0.0.0/0` (Used for ACME Let's Encrypt validation and HTTP-to-HTTPS 301 redirection).
  - **Inbound Rule 2**: Type `HTTPS`, Protocol `TCP`, Port `443`, Source `0.0.0.0/0` (Encrypted production web and webhook traffic).
  - **Crucial Security Observation**: Point out to the faculty that **Port 22 (SSH) is completely absent from the rules list**.
- **Key Narration Points**:
  - By relying on SSM Session Manager for host management, the SSH port is permanently closed to the public internet, eliminating automated botnet dictionary attacks and brute-force intrusion risks.

---

### 5. Amazon CloudWatch Logs & Alarms (Tabs 6 & 7)
- **Direct Links**:
  - **Log Group**: `https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1#logsV2:log-groups/log-group/$252Faws$252Fec2$252Fdelta-bot`
  - **Alarm**: `https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1#alarmsV2:alarm/DeltaBot-HighCPUUtilization`
- **Navigation Path in Console**:
  1. Search for `CloudWatch` in the header search bar.
  2. In the left navigation, open **Logs** -> **Log groups**.
  3. Click on the log group name: `/aws/ec2/delta-bot`.
  4. Click on the active log stream: `i-0affed362f3927281-app`.
  5. The log viewer displays live timestamps and Gunicorn application log entries:
     ```
     2026-10-24 17:18:06 - INFO - Fetching products list from Delta Exchange...
     127.0.0.1 - - [24/Oct/2026:17:18:06 +0000] "GET /health HTTP/1.1" 200 51
     ```
  6. In the left navigation under **Alarms**, click **In alarm / All alarms**.
  7. Show alarm `DeltaBot-HighCPUUtilization`:
     - **Status**: `OK` (Green badge).
     - **Condition**: `CPUUtilization > 80% for 2 datapoints within 10 minutes`.
- **Key Narration Points**:
  - The Amazon CloudWatch Unified Agent streams both application and system logs directly from the EC2 host.
  - Automated threshold alarms monitor CPU consumption, alerting administrators before memory or compute saturation occurs.

---

### 6. AWS IAM Least-Privilege Instance Profile (Tab 8)
- **Direct Link**: `https://console.aws.amazon.com/iam/home#/roles/details/DeltaTradingBot-InstanceRole-ap-south-1`
- **Navigation Path in Console**:
  1. Search for `IAM` in the header search bar.
  2. In the left navigation, click **Roles**.
  3. Click on the role name: `DeltaTradingBot-InstanceRole-ap-south-1`.
  4. In the **Permissions** tab, highlight the attached AWS managed policies:
     - `AmazonSSMManagedInstanceCore` (Allows secure Session Manager connectivity).
     - `CloudWatchAgentServerPolicy` (Allows pushing metrics and logs to CloudWatch).
     - `AmazonS3ReadOnlyAccess` (Allows downloading build artifacts during provisioning).
- **Key Narration Points**:
  - In accordance with AWS Well-Architected Security principles, no long-term AWS access keys (`AKIA...`) are stored on the EC2 instance or in environment files.
  - The instance authenticates securely via temporary STS credentials rotated automatically by AWS.

---

## 7. Security Best Practices During Recording
- **Hide Account ID**: In the top right corner of the AWS header, the account ID `704475327110` is displayed. If possible, click on the username dropdown and keep it collapsed, or avoid lingering on the top-right corner.
- **Never Open .env in Terminal**: During the SSM terminal demonstration, only run `docker compose ps` and `curl localhost:5000/health`. Do not run `cat .env` or expose API keys on screen.
