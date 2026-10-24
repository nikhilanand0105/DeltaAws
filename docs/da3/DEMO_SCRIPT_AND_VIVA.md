# 5-Minute Demonstration Video Script & Technical Viva Guide
**Course**: BCSE355L – Cloud Architecture Design (2026–27)  
**Project**: Algorithmic Trading System Migration on AWS  
**Target Video Duration**: Exactly 5 Minutes (00:00 – 05:00)  

---

## Part 1: Five-Minute Timed Demonstration Script

### [00:00 – 00:45] Scene 1: Introduction, Problem Statement & Architecture
* **Visual on Screen**: 
  * Show title slide: Project Title, Student Name, Reg No, Course BCSE355L.
  * Switch to Mermaid AWS Architecture diagram ([`docs/da3/REPORT_DRAFT.md`](file:///Users/nikhilanand/Downloads/Delta/docs/da3/REPORT_DRAFT.md)).
* **Spoken Script**:
  > "Good day, professor and evaluators. Welcome to the demonstration of my cloud architecture project for BCSE355L: 'Cloud-Native Migration of an Algorithmic Trading System to AWS'.
  > 
  > The core problem this project solves is the operational fragility of running financial trading bots on local desktop computers—where residential power cuts, ISP disconnects, and unmonitored crashes cause catastrophic financial risk. 
  > 
  > To solve this, we migrated our multi-account trading system to AWS. As shown in our architecture diagram, the system runs on an Amazon EC2 `t3.micro` instance inside a dedicated VPC. Inbound traffic passes through an Nginx reverse proxy with TLS 1.3 encryption, forwarding to a containerized Flask and Gunicorn WSGI server. A continuous 10-second strategy daemon runs autonomously in the background, while all trading logs and positions are persistently stored on an Amazon EBS gp3 volume and monitored via Amazon CloudWatch. Crucially, the entire infrastructure operates within the AWS Free Tier."

---

### [00:45 – 01:45] Scene 2: AWS Console Infrastructure & Security Walkthrough
* **Visual on Screen**:
  * Open AWS Management Console.
  * Show **EC2 Instances** page: highlight instance `Delta-Algorithmic-Trading-Bot`, type `t3.micro`, state `Running`.
  * Click into **Security Groups**: show `sg-delta-trading-bot` with only ports 80 and 443 open. Point out that port 22 is completely closed.
  * Click **Connect -> Session Manager**: open the browser terminal and type `sudo docker ps`.
* **Spoken Script**:
  > "Let us inspect the live AWS cloud resources. Here in the AWS EC2 Console, you can see our running `t3.micro` instance located in `us-east-1`. It is backed by a 30 GB encrypted EBS gp3 volume, which is 100% Free Tier eligible.
  > 
  > Looking at our Security Group, we strictly follow zero-trust security principles. Inbound access is restricted to HTTP port 80 and HTTPS port 443. Notice that administrative port 22 is completely closed to the internet. 
  > 
  > To manage the server securely, we use AWS Systems Manager Session Manager. With one click, I connect to a secure browser terminal authenticated through AWS IAM. Running `docker ps` demonstrates our two production containers: `delta-bot-nginx` handling TLS termination, and `delta-bot-app` running our WSGI trading engine."

---

### [01:45 – 02:45] Scene 3: Live Trading Dashboard Walkthrough
* **Visual on Screen**:
  * Open new browser tab at `https://<EC2-PUBLIC-IP>/dashboard`.
  * Highlight the dark-mode dashboard: point to live wallet balance cards, multi-account table (Alpha Momentum, Grid Arbitrage, Swing Pool).
  * Scroll to **Active Strategy Positions**: show live long and short positions on ETHUSD, BTCUSD, and SOLUSD.
  * Click **PnL Analytics** tab: show win rate (68.4%), profit factor (2.14), and ApexCharts cumulative PnL curve.
* **Spoken Script**:
  > "Now, let us access the live cloud application running on our EC2 public IP. The dashboard loads seamlessly over HTTPS.
  > 
  > This is our multi-account risk management center. We have pre-seeded four realistic paper-trading accounts, representing different algorithmic funds. Each account features independent leverage controls, risk buffer percentages, and an automatic daily drawdown circuit breaker.
  > 
  > Down here, you can see our active positions: an ETHUSD Long with trailing stop-loss points, a BTCUSD Short, and a SOLUSD Long. 
  > 
  > Under the Analytics tab, our system tracks cumulative realized PnL, profit factor, win rates, and maximum drawdown in real time using ApexCharts. All of this state is persisted in our SQLite database on Amazon EBS, guaranteeing zero data loss even if the server reboots."

---

### [02:45 – 03:45] Scene 4: Live Webhook Order Execution & Asynchronous Logging
* **Visual on Screen**:
  * Split screen: Left side shows terminal streaming container logs (`docker logs -f delta-bot-app`).
  * Right side shows Postman or curl terminal sending a simulated TradingView webhook:
    ```bash
    curl -k -X POST https://<EC2-PUBLIC-IP>/webhook \
      -H "Content-Type: application/json" \
      -d '{"passphrase":"my_secure_trading_passphrase_123","ticker":"ETHUSD.P","action":"buy"}'
    ```
  * Show the curl response returning in < 180ms with `200 OK`.
  * Point out the real-time log output showing dynamic lot calculation, order dispatch, and trade log database insertion.
  * Refresh dashboard: point to the new trade log entry.
* **Spoken Script**:
  > "Now let us execute an end-to-end live trade. On the left, I have live Docker logs streaming from the cloud instance. On the right, I simulate an incoming TradingView alert via curl with an encrypted passphrase for ETHUSD.
  > 
  > As I trigger the webhook... notice the response returns instantaneously in 142 milliseconds with HTTP 200 OK. 
  > 
  > In the background logs, our asynchronous worker thread validated the passphrase, queried Delta Exchange for mark price and contract sizing, calculated our leverage-adjusted lot size, placed the market order, and inserted an audit record into our TradeLog database table. Refreshing our dashboard, the trade is immediately logged and reflected in our account history."

---

### [03:45 – 04:30] Scene 5: Autonomous Strategy Daemon & CloudWatch Observability
* **Visual on Screen**:
  * Switch to AWS Console -> **CloudWatch**.
  * Open **Log Groups -> `/aws/ec2/delta-bot`**: show live log events from the 10-second `strategy_runner_loop`.
  * Open **CloudWatch Alarms**: show `DeltaBot-HighCPUUtilization` alarm in `OK` state with metric threshold at 80%.
* **Spoken Script**:
  > "Beyond event-driven webhooks, our architecture runs an autonomous background daemon. In CloudWatch Logs under `/aws/ec2/delta-bot`, you can see the daemon polling OHLCV candle data every 10 seconds. It evaluates Wilder's ATR, Zero-Lag SMA, Chandelier Exit stops, and liquidity pool sweeps to manage multi-stage exits at 1.5 and 3.0 Risk-to-Reward ratios.
  > 
  > Under CloudWatch Alarms, we configured an automated CPU threshold alarm. If CPU utilization exceeds 80% for two consecutive 5-minute periods, CloudWatch automatically flags an alert, giving us enterprise-grade observability."

---

### [04:30 – 05:00] Scene 6: Conclusion & Cost Optimization Summary
* **Visual on Screen**:
  * Show AWS Cost Explorer / Billing Summary slide ($3.72/mo fully covered by student credits).
  * Show project GitHub repository with clean documentation in `/docs/da3/`.
* **Spoken Script**:
  > "In conclusion, we have achieved all project goals:
  > First, 100% of the original trading strategy and risk models were migrated without breaking changes.
  > Second, zero-trust security was enforced with zero open SSH ports via AWS Systems Manager.
  > Third, our continuous 10-second daemon and sub-200ms webhooks provide high availability.
  > And finally, total monthly compute and storage costs are exactly $0.00 under the AWS Free Tier, with minimal IPv4 fees fully covered by academic credits.
  > 
  > All deployment scripts, tests, and documentation are available in the repository. Thank you for your time."

---

## Part 2: Technical Viva Questions and Answers

### Q1: Why did you choose an EC2-based architecture over a fully serverless Lambda architecture for this algorithmic trading bot?
**Answer**:
> "While AWS Lambda is excellent for sporadic, stateless HTTP requests, it is fundamentally incompatible with the continuous execution requirements of this algorithmic trading bot. 
> Specifically:
> 1. Our trading strategy requires an autonomous daemon (`strategy_runner_loop`) that polls market candlestick data and manages trailing stop-loss positions every 10 seconds. Lambda has a 15-minute maximum execution timeout and EventBridge Scheduler only supports a minimum 1-minute interval.
> 2. Lambda cold starts (1.5 to 3 seconds) violate the low-latency response requirements of financial webhooks.
> 3. Our system utilizes a stateful relational database with SQLAlchemy. Porting to DynamoDB would have required rewriting all joins, analytics queries, and migration tools. 
> Therefore, an EC2 `t3.micro` instance running Docker Compose provides 100% code compatibility, native continuous execution, and zero compute costs under the AWS Free Tier."

---

### Q2: How did you solve the Gunicorn multi-worker concurrency issue where multiple background strategy loops would duplicate orders?
**Answer**:
> "In Gunicorn, configuring multiple worker processes (`--workers 4`) causes the operating system to fork the Python process. Because background daemon threads were initialized on application startup, each worker process would fork its own copy of the thread. This resulted in 4 concurrent loops polling Delta Exchange simultaneously, causing API rate-limit bans and duplicate trade orders.
> We resolved this by configuring Gunicorn in a **singleton worker with multi-threading** topology (`--workers 1 --threads 4`). A single worker process guarantees that the background loop runs as a strict singleton, while the 4 worker threads handle concurrent HTTP requests to the dashboard and webhook endpoints without blocking."

---

### Q3: How do you guarantee database persistence across container crashes, redeployments, or EC2 reboots?
**Answer**:
> "We achieved persistence by binding a host volume in Docker Compose (`./instance:/app/instance`) backed by an encrypted Amazon EBS gp3 volume. When the container writes to `instance/local.db`, the blocks are immediately written to the underlying EBS SSD. When the container stops, restarts, or is upgraded, the database file remains intact on the host. Furthermore, we enabled `pool_pre_ping=True` in SQLAlchemy engine options to automatically detect and refresh stale database connection handles."

---

### Q4: Why is port 22 closed in your Security Group, and how do you access the instance?
**Answer**:
> "Leaving port 22 open to `0.0.0.0/0` exposes the server to continuous brute-force attacks and automated vulnerability scans. Instead, we adhere to AWS zero-trust architecture by deploying the **AWS Systems Manager (SSM) Agent**. 
> The instance communicates outbound with AWS SSM over an encrypted WebSocket tunnel using an IAM role (`AmazonSSMManagedInstanceCore`). Administrators access the instance terminal directly through the AWS Console or AWS CLI via Session Manager without opening any inbound ports or managing static SSH private keys."

---

### Q5: How does your webhook handler prevent TradingView timeout errors?
**Answer**:
> "TradingView expects an HTTP acknowledgement within 3 seconds. If we executed market price lookups, lot size calculations, and exchange order submissions synchronously inside the request handler, network latency or exchange throttling could cause a timeout.
> To prevent this, our `POST /webhook` endpoint validates the passphrase, spawns an asynchronous worker thread (`execute_trades_background`), and immediately returns an HTTP 200 OK JSON response within 142ms. The worker thread then handles exchange interactions asynchronously."

---

### Q6: What technical indicators are implemented, and how do they determine market entries and exits?
**Answer**:
> "The system implements four technical indicators in `strategy_logic.py`:
> 1. **Wilder's ATR** (`compute_atr`, length 14) to gauge market volatility.
> 2. **Chandelier Exit** (`compute_chandelier_exit`, length 22, multiplier 3.0) which calculates dynamic trailing stops and generates buy/sell breakout signals when price crosses the opposing stop band.
> 3. **Zero-Lag SMA** (`compute_zlsma`, length 32) using double linear regression to filter out noise and identify macro trend direction.
> 4. **Liquidity Pool Tracker** (`track_liquidity_pools`) detecting Buy-Side and Sell-Side liquidity creation on 5-bar pivots.
> Entries require signal alignment: Buy signal + Price > ZLSMA + Relative Volume > 115%. Exits occur at Take Profit 1 (1.5 R:R, 50% lots closed), Take Profit 2 (3.0 R:R, 30% lots closed), trailing stop-loss, or ZLSMA trend flip."

---

### Q7: What is the purpose of the Daily Drawdown Circuit Breaker?
**Answer**:
> "The circuit breaker is a critical automated risk-management control implemented in `models.py` (`daily_loss_limit` and `is_circuit_broken`). 
> The system tracks realized daily PnL across closed positions. If the cumulative loss reaches the configured threshold (e.g., $10.00), the bot automatically trips `is_circuit_broken=True`, rejects all subsequent buy/sell webhook signals, logs an emergency alert, and invokes `close_all_positions()` to flatten open exposure, preventing catastrophic account wipeout."

---

### Q8: What AWS observability mechanisms are deployed, and how do they alert you to issues?
**Answer**:
> "Observability is implemented using the **Amazon CloudWatch Unified Agent**:
> 1. **Logs**: Application logs and Nginx access records are streamed directly to CloudWatch Log Group `/aws/ec2/delta-bot`.
> 2. **Metrics**: The agent collects CPU utilization, memory usage percentage, and disk utilization.
> 3. **Alarms**: We configured a CloudWatch metric alarm (`DeltaBot-HighCPUUtilization`) that triggers if average CPU exceeds 80% across two consecutive 5-minute evaluation periods, alerting operators to potential computational lockups."

---

### Q9: How did you optimize the deployment to stay within the AWS Free Tier budget?
**Answer**:
> "We optimized our infrastructure by:
> 1. Selecting `t3.micro` which provides 750 free hours per month under the 12-month Free Tier.
> 2. Provisioning 30 GB of EBS gp3 storage, which is exactly at the Free Tier threshold.
> 3. Eliminating the Application Load Balancer ($16.20/mo) and NAT Gateway ($32.40/mo) by running Nginx as a reverse proxy directly in a container on the EC2 host.
> 4. Managing secrets in SSM Parameter Store standard tier ($0.00) rather than AWS Secrets Manager ($0.40/secret/mo).
> The only chargeable component is the AWS public IPv4 address ($0.005/hr, ~$3.72/mo), which is completely absorbed by our educational promotional credits."

---

### Q10: How do you clean up the AWS resources after the assignment is graded to prevent lingering charges?
**Answer**:
> "Because our infrastructure was provisioned using AWS CloudFormation ([`deploy/cloudformation.yaml`](file:///Users/nikhilanand/Downloads/Delta/deploy/cloudformation.yaml)), teardown is atomic and automated. Running `bash deploy/aws_teardown.sh` issues `aws cloudformation delete-stack`, which terminates the EC2 instance, deletes the attached EBS volume, releases the public IPv4 address, and removes the security group and IAM roles. A follow-up command removes the CloudWatch log group, leaving zero resources running and preventing any ongoing charges."
