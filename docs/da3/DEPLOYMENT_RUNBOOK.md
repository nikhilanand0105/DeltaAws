# AWS Cloud Architecture Deployment Runbook (Beginner-Friendly Guide)
**Course**: BCSE355L – Cloud Architecture Design (2026–27)  
**Project**: Algorithmic Trading System Migration & Cloud Deployment  
**Target Platform**: Amazon Web Services (AWS Free Tier / Credit-Eligible)  

---

## 1. Prerequisites & Safety Precautions

Before executing any commands, review these foundational principles:
1. **Never Commit Secrets**: Never paste or hardcode your AWS Access Keys, Secret Keys, or Delta Exchange API credentials in git commits, bash command histories, or chat windows.
2. **Billing Alarm**: Always set an initial AWS CloudWatch Billing Alarm at $1.00 or $5.00 to guarantee immediate alerts against inadvertent chargeable resource provisioning.
3. **Region Selection**: Deploy in `us-east-1` (N. Virginia) or `ap-south-1` (Mumbai) where Free Tier EC2 instance types (`t3.micro` / `t2.micro`) and AWS Systems Manager are fully supported.
4. **Zero-Trust Administrative Access**: This deployment utilizes **AWS Systems Manager (SSM) Session Manager** for terminal access. Port 22 (SSH) is completely closed to the internet in the security group, eliminating brute-force vulnerabilities.

---

## 2. Step-by-Step Deployment Instructions

### STEP 1: AWS Account Setup & Billing Safeguards

* **A. Exact AWS Console Path / CLI Command**:
  * Console Path: **AWS Management Console -> Billing and Cost Management -> Billing Preferences -> Receive CloudWatch Billing Alerts**.
  * CloudWatch Path: **CloudWatch -> Alarms -> Create Alarm -> Select Metric -> Billing -> Total Estimated Charge**.
  * CLI Command:
    ```bash
    aws cloudwatch put-metric-alarm \
      --alarm-name "BudgetSafetyAlarm-5USD" \
      --alarm-description "Triggers notification if estimated charges exceed $5" \
      --metric-name EstimatedCharges \
      --namespace AWS/Billing \
      --statistic Maximum \
      --period 21600 \
      --threshold 5.0 \
      --comparison-operator GreaterThanOrEqualToThreshold \
      --dimensions Name=Currency,Value=USD \
      --evaluation-periods 1
    ```
* **B. What it Does & Why it is Needed**:
  Establishes an automated monitoring boundary that triggers if your monthly bill reaches $5.00. This protects your university credit balance or personal card.
* **C. Required Inputs**:
  Currency code (`USD`), threshold limit (`5.0`).
* **D. Expected Result**:
  CloudWatch returns status 200; alarm appears in the CloudWatch console under `OK` status.
* **E. Common Failures & Fixes**:
  * *Error*: `Billing metrics are not enabled`.
  * *Fix*: Go to AWS Billing Console -> Preferences -> Check "Receive Billing Alerts" and wait 15 minutes.
* **F. Screenshot for DA3 Report**:
  Capture: CloudWatch Alarms dashboard showing `BudgetSafetyAlarm-5USD` in `OK` state.
* **G. Cost & Security Implications**:
  10 CloudWatch alarms are 100% Free Tier eligible. Incurs $0.00 cost.

---

### STEP 2: IAM Role & Security Group Configuration

* **A. Exact AWS Console Path / CLI Command**:
  * Console Path: **IAM -> Roles -> Create Role -> EC2 -> Attach `AmazonSSMManagedInstanceCore` and `CloudWatchAgentServerPolicy`**.
  * CLI Command:
    ```bash
    # Create IAM Role
    aws iam create-role \
      --role-name DeltaTradingBot-InstanceRole \
      --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Principal": {"Service": "ec2.amazonaws.com"}, "Action": "sts:AssumeRole"}]
      }'

    # Attach SSM Policy (Browser Terminal Access)
    aws iam attach-role-policy \
      --role-name DeltaTradingBot-InstanceRole \
      --policy-arn arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore

    # Attach CloudWatch Policy (Metrics and Logs)
    aws iam attach-role-policy \
      --role-name DeltaTradingBot-InstanceRole \
      --policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy

    # Create Instance Profile
    aws iam create-instance-profile --instance-profile-name DeltaTradingBot-Profile
    aws iam add-role-to-instance-profile --instance-profile-name DeltaTradingBot-Profile --role-name DeltaTradingBot-InstanceRole
    ```
* **B. What it Does & Why it is Needed**:
  Grants the EC2 instance least-privilege permission to communicate with AWS Systems Manager (SSM) for encrypted shell access and push system/application metrics to CloudWatch Logs without embedding static access keys on the server.
* **C. Required Inputs**:
  Role name (`DeltaTradingBot-InstanceRole`), policy ARNs.
* **D. Expected Result**:
  IAM role and instance profile created successfully; verified via `aws iam get-role --role-name DeltaTradingBot-InstanceRole`.
* **E. Common Failures & Fixes**:
  * *Error*: `EntityAlreadyExists`.
  * *Fix*: The role already exists from a previous step; proceed directly to attaching policies.
* **F. Screenshot for DA3 Report**:
  Capture: IAM Role Summary page showing attached managed policies `AmazonSSMManagedInstanceCore` and `CloudWatchAgentServerPolicy`.
* **G. Cost & Security Implications**:
  IAM roles and policies are 100% free. Prevents credential leakage.

---

### STEP 3: Security Group Network Boundary Creation

* **A. Exact AWS Console Path / CLI Command**:
  * Console Path: **VPC -> Security Groups -> Create Security Group -> Name: `sg-delta-trading-bot`**.
  * CLI Command:
    ```bash
    VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query "Vpcs[0].VpcId" --output text)

    SG_ID=$(aws ec2 create-security-group \
      --group-name "sg-delta-trading-bot" \
      --description "Security group for Delta Trading Bot (Inbound 80, 443; Egress All)" \
      --vpc-id "$VPC_ID" \
      --query "GroupId" --output text)

    # Inbound HTTP (port 80) for Nginx redirect to HTTPS
    aws ec2 authorize-security-group-ingress \
      --group-id "$SG_ID" \
      --protocol tcp \
      --port 80 \
      --cidr 0.0.0.0/0

    # Inbound HTTPS (port 443) for TradingView Webhook & Admin Dashboard
    aws ec2 authorize-security-group-ingress \
      --group-id "$SG_ID" \
      --protocol tcp \
      --port 443 \
      --cidr 0.0.0.0/0
    ```
* **B. What it Does & Why it is Needed**:
  Implements stateful firewall filtering. Allows inbound web traffic strictly on ports 80 and 443 while keeping administrative port 22 closed to the internet.
* **C. Required Inputs**:
  VPC ID (`VPC_ID`), ports (80, 443), CIDR block (`0.0.0.0/0`).
* **D. Expected Result**:
  Security group ID returned (`sg-xxxxxxxxx`); ingress rules verified via `aws ec2 describe-security-groups --group-ids $SG_ID`.
* **E. Common Failures & Fixes**:
  * *Error*: `InvalidPermission.Duplicate`.
  * *Fix*: Rule already exists; skip or ignore duplicate addition.
* **F. Screenshot for DA3 Report**:
  Capture: EC2 Security Group Inbound Rules tab showing only ports 80 and 443 open.
* **G. Cost & Security Implications**:
  Security Groups incur $0.00 cost. Completely mitigates automated SSH bot attacks.

---

### STEP 4: CloudFormation Automated Stack Provisioning

* **A. Exact AWS Console Path / CLI Command**:
  * Console Path: **CloudFormation -> Stacks -> Create Stack -> With new resources -> Upload template -> `deploy/cloudformation.yaml`**.
  * CLI Command:
    ```bash
    bash deploy/aws_deploy.sh
    ```
* **B. What it Does & Why it is Needed**:
  Deploys the complete AWS Infrastructure as Code (IaC) stack: provisions the `t3.micro` EC2 instance, attaches the 30 GB gp3 volume, configures CloudWatch Log Group `/aws/ec2/delta-bot`, and sets up the CPU alarm.
* **C. Required Inputs**:
  Template path (`deploy/cloudformation.yaml`), target region (`us-east-1`).
* **D. Expected Result**:
  CloudFormation reports `CREATE_COMPLETE`. Stack outputs display:
  * `InstanceId: i-0xxxxxxxxxxxx`
  * `PublicIp: 54.xxx.xxx.xxx`
  * `DashboardURL: https://54.xxx.xxx.xxx/dashboard`
  * `WebhookURL: https://54.xxx.xxx.xxx/webhook`
* **E. Common Failures & Fixes**:
  * *Error*: `No default VPC found`.
  * *Fix*: In the AWS Console, click **VPC -> Actions -> Create default VPC**, then re-run the deployment script.
* **F. Screenshot for DA3 Report**:
  Capture: CloudFormation stack overview showing `CREATE_COMPLETE` status and the **Outputs** tab.
* **G. Cost & Security Implications**:
  EC2 `t3.micro` and 30 GB EBS gp3 are covered under the 750-hour AWS Free Tier. The attached public IPv4 address bills at $0.005/hr (~$3.65/mo), which is deducted from your promotional credits.

---

### STEP 5: Connect Securely via AWS Systems Manager Session Manager

* **A. Exact AWS Console Path / CLI Command**:
  * Console Path: **EC2 -> Instances -> Select Instance -> Click "Connect" -> Select "Session Manager" -> Click "Connect"**.
  * CLI Command:
    ```bash
    aws ssm start-session --target <INSTANCE_ID>
    ```
* **B. What it Does & Why it is Needed**:
  Opens an encrypted, authenticated browser terminal session directly on the EC2 instance without requiring SSH keys or public port 22 access.
* **C. Required Inputs**:
  EC2 Instance ID (`i-xxxxxxxx`).
* **D. Expected Result**:
  Bash prompt opens: `sh-5.2$ ` or `ec2-user@...`.
* **E. Common Failures & Fixes**:
  * *Error*: `TargetNotConnected`.
  * *Fix*: The EC2 instance takes 60–90 seconds after boot to register with SSM. Wait 1 minute and re-try. Ensure the IAM role `AmazonSSMManagedInstanceCore` is attached.
* **F. Screenshot for DA3 Report**:
  Capture: Browser terminal open via AWS SSM Session Manager displaying `uname -a` and `docker --version`.
* **G. Cost & Security Implications**:
  100% Free. All session traffic is encrypted with TLS 1.3 and logged in AWS CloudTrail for university audit compliance.

---

### STEP 6: Application Code Deployment & Container Launch

* **A. Exact AWS Console Path / CLI Command**:
  Run inside the SSM Session Manager terminal:
  ```bash
  # 1. Switch to root/admin
  sudo -i

  # 2. Clone repository branch
  git clone -b aws-deployment-da3 https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>.git /opt/delta-bot
  cd /opt/delta-bot

  # 3. Execute setup script
  bash deploy/setup_ec2.sh
  ```
* **B. What it Does & Why it is Needed**:
  Downloads the application, generates self-signed TLS certificates for Nginx, configures systemd, seeds the SQLite database with paper trading accounts, and launches the Docker Compose stack (Flask WSGI + Nginx).
* **C. Required Inputs**:
  Git repository URL.
* **D. Expected Result**:
  Command output confirms:
  ```
  [INFO] Launching Docker Compose stack...
  ✔ Network delta-bot_delta-net   Created
  ✔ Container delta-bot-app       Started
  ✔ Container delta-bot-nginx     Started
  [SUCCESS] Delta Trading Bot Deployment Complete!
  ```
* **E. Common Failures & Fixes**:
  * *Error*: `docker: command not found`.
  * *Fix*: Run `dnf install -y docker` or `systemctl start docker`.
* **F. Screenshot for DA3 Report**:
  Capture: Terminal output showing Docker Compose containers `delta-bot-app` and `delta-bot-nginx` in `Up (healthy)` state.
* **G. Cost & Security Implications**:
  Containers run locally on the EC2 host. Persistent database data is stored in `/opt/delta-bot/instance/local.db` on the 30 GB EBS volume.

---

### STEP 7: Application Health & Webhook Verification

* **A. Exact AWS Console Path / CLI Command**:
  From your local machine terminal:
  ```bash
  PUBLIC_IP="<YOUR_EC2_PUBLIC_IP>"

  # 1. Verify Health Endpoint
  curl -k -i "https://$PUBLIC_IP/health"

  # 2. Test Webhook Authentication (Negative test - should fail 401)
  curl -k -i -X POST "https://$PUBLIC_IP/webhook" \
    -H "Content-Type: application/json" \
    -d '{"passphrase":"wrong_passphrase","ticker":"ETHUSD.P","action":"buy"}'

  # 3. Test Webhook Order Execution (Positive test - should succeed 200)
  curl -k -i -X POST "https://$PUBLIC_IP/webhook" \
    -H "Content-Type: application/json" \
    -d '{"passphrase":"my_secure_trading_passphrase_123","ticker":"ETHUSD.P","action":"buy"}'
  ```
* **B. What it Does & Why it is Needed**:
  Validates that Nginx is properly terminating TLS, proxying requests to Flask, enforcing rate limits, authenticating webhooks, and executing orders statefully.
* **C. Required Inputs**:
  EC2 Public IP, Passphrase (`my_secure_trading_passphrase_123`).
* **D. Expected Result**:
  * Health returns: `HTTP/1.1 200 OK` with `{"service":"delta-webhook-bot","status":"healthy"}`.
  * Negative test returns: `HTTP/1.1 401 UNAUTHORIZED`.
  * Positive test returns: `HTTP/1.1 200 OK` with `{"status":"success"}` in < 200ms.
* **E. Common Failures & Fixes**:
  * *Error*: `Connection timed out`.
  * *Fix*: Verify the EC2 Security Group has inbound rules for port 443 from `0.0.0.0/0`.
* **F. Screenshot for DA3 Report**:
  Capture: Terminal window showing curl command responses with HTTP 200 OK status codes.
* **G. Cost & Security Implications**:
  Validates API security and prevents unauthorized order placement.

---

### STEP 8: Web Dashboard Inspection & Video Demonstration

* **A. Exact AWS Console Path / CLI Command**:
  Open in your web browser:
  ```
  https://<YOUR_EC2_PUBLIC_IP>/dashboard
  ```
  *(Note: Since self-signed SSL is used, your browser will display an "Advanced -> Proceed to site" warning. Click Proceed).*
* **B. What it Does & Why it is Needed**:
  Demonstrates the live web interface to faculty reviewers, displaying real-time wallet equity, active long/short positions, dynamic risk calculators, trade logs, and ApexCharts PnL curves.
* **C. Required Inputs**:
  EC2 Public IP.
* **D. Expected Result**:
  Dark-mode dashboard loads with live balances, active positions for ETHUSD, BTCUSD, and SOLUSD, and cumulative PnL graphs.
* **E. Common Failures & Fixes**:
  * *Issue*: Dashboard shows blank cards.
  * *Fix*: Run `docker compose exec app python seed_mock_data.py` inside the EC2 instance to repopulate demonstration records.
* **F. Screenshot for DA3 Report**:
  Capture: Full browser screenshot of the **Accounts & Risk Management** tab and **PnL Analytics** tab showing live cloud metrics.
* **G. Cost & Security Implications**:
  No ongoing charges. Demonstrates full stack operation.

---

### STEP 9: CloudWatch Monitoring & Alarm Verification

* **A. Exact AWS Console Path / CLI Command**:
  * Console Path: **CloudWatch -> Log Groups -> `/aws/ec2/delta-bot` -> View Log Streams**.
  * Console Path: **CloudWatch -> Metrics -> All Metrics -> DeltaTradingBot / AWS/EC2**.
* **B. What it Does & Why it is Needed**:
  Verifies that cloud-native observability is active. Demonstrates to faculty that logs and CPU/memory metrics are ingested into AWS managed services.
* **C. Required Inputs**:
  Log group name (`/aws/ec2/delta-bot`).
* **D. Expected Result**:
  Real-time application logs visible in CloudWatch showing the 10-second strategy runner polling cycles and trade execution events.
* **E. Common Failures & Fixes**:
  * *Issue*: Log streams are empty.
  * *Fix*: Verify the EC2 instance has IAM role `DeltaTradingBot-InstanceRole` attached with `CloudWatchAgentServerPolicy`.
* **F. Screenshot for DA3 Report**:
  Capture: CloudWatch Log Streams table displaying live `[INFO]` trade events and CloudWatch metric graphs for `CPUUtilization`.
* **G. Cost & Security Implications**:
  Log ingestion under 5 GB/month is 100% Free Tier eligible.

---

### STEP 10: AWS Resource Teardown (Post-Grading Cleanup)

* **A. Exact AWS Console Path / CLI Command**:
  From your local machine:
  ```bash
  bash deploy/aws_teardown.sh
  ```
* **B. What it Does & Why it is Needed**:
  Permanently deletes the CloudFormation stack, terminates the EC2 instance, releases the public IPv4 address, and removes the EBS volume, guaranteeing zero recurring billing.
* **C. Required Inputs**:
  Confirmation prompt (`y`).
* **D. Expected Result**:
  `DELETE_COMPLETE` status returned. All resources removed from AWS account.
* **E. Common Failures & Fixes**:
  * *Error*: `Stack deletion failed`.
  * *Fix*: Check CloudFormation console events for the blocking resource (e.g. non-empty S3 bucket or detached network interface) and delete manually.
* **F. Screenshot for DA3 Report**:
  Capture: CloudFormation stack status showing `DELETE_COMPLETE`.
* **G. Cost & Security Implications**:
  Prevents unwanted billing after course assignment completion.
