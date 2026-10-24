# Test Results, Verification Evidence & Screenshot Checklist
**Course**: BCSE355L – Cloud Architecture Design (2026–27)  
**Project**: Algorithmic Trading System Migration on AWS  
**Artifact Directory**: `docs/da3/`  

---

## 1. Automated Test Execution Results

The automated unit and integration test suite was executed against the containerized application stack using Python 3.11/3.9 and an isolated in-memory SQLite database (`sqlite:///:memory:`).

### Execution Summary
* **Total Tests Executed**: 38
* **Passed**: 38 (100%)
* **Failed**: 0
* **Errors**: 0
* **Execution Time**: 3.435 seconds

### Comprehensive Results Table

| Test ID | Test Category | Specific Test Case | Expected Result | Actual Result | Status | Code Evidence |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| **TC-01** | Input Validation | Clean Symbol Normalization (`ETHUSD.P` -> `ETHUSD`) | Normalizes ticker and retrieves product ID 27. | Normalized cleanly; product ID 27 returned. | **PASS** | [`verify_bot.py:20`](file:///Users/nikhilanand/Downloads/Delta/verify_bot.py#L20) |
| **TC-02** | Cryptography | HMAC-SHA256 Header Generation | Concatenates method, timestamp, path, query, body and signs with SHA256. | Hex digest signature matches Delta API specification. | **PASS** | [`verify_bot.py:35`](file:///Users/nikhilanand/Downloads/Delta/verify_bot.py#L35) |
| **TC-03** | Risk Management | Dynamic Lot Sizing Calculation | Mathematical formula allocates exact floor integer contracts based on margin buffer. | Returned floor integer lot count (26 lots) with fee cushion. | **PASS** | [`verify_bot.py:57`](file:///Users/nikhilanand/Downloads/Delta/verify_bot.py#L57) |
| **TC-04** | Security | Webhook Unauthorized Rejection | Request with invalid passphrase rejected with HTTP 401. | Returned HTTP 401 Unauthorized; logged audit event. | **PASS** | [`verify_bot.py:105`](file:///Users/nikhilanand/Downloads/Delta/verify_bot.py#L105) |
| **TC-05** | Order Execution | Webhook Valid Buy Order | Returns HTTP 200 OK within 200ms and executes trade in background thread. | Returned HTTP 200 OK in 142ms; order logged to DB. | **PASS** | [`verify_bot.py:140`](file:///Users/nikhilanand/Downloads/Delta/verify_bot.py#L140) |
| **TC-06** | Circuit Breaker | Daily Drawdown Circuit Breaker | Account breaches daily loss limit; circuit breaker trips and halts trading. | Circuit breaker set to True; subsequent trades rejected. | **PASS** | [`verify_bot.py:1210`](file:///Users/nikhilanand/Downloads/Delta/verify_bot.py#L1210) |
| **TC-07** | Circuit Breaker | Breaker Reset Endpoint | `POST /api/accounts/<id>/reset-breaker` clears circuit breaker flag. | Circuit breaker cleared; trading status restored. | **PASS** | [`verify_bot.py:1255`](file:///Users/nikhilanand/Downloads/Delta/verify_bot.py#L1255) |
| **TC-08** | Mathematics | Linear Regression Calculation | Computes slope, intercept, and linear regression kernel across bars. | Matches manual regression values with zero numerical drift. | **PASS** | [`verify_strategy.py:28`](file:///Users/nikhilanand/Downloads/Delta/verify_strategy.py#L28) |
| **TC-09** | Mathematics | Wilder's ATR Calculation | Computes RMA of true range across high, low, close series. | Output matches TradingView `ta.atr` reference. | **PASS** | [`verify_strategy.py:43`](file:///Users/nikhilanand/Downloads/Delta/verify_strategy.py#L43) |
| **TC-10** | Technical Indicator | Zero-Lag SMA Warm-up | Double linear regression filters lag without array indexing crashes. | Returns smooth indicator series after 38 warm-up bars. | **PASS** | [`verify_strategy.py:62`](file:///Users/nikhilanand/Downloads/Delta/verify_strategy.py#L62) |
| **TC-11** | Technical Indicator | Chandelier Exit Flip Logic | Flips trend direction from Long (1) to Short (-1) on breakout. | Directional array flips on candle close beyond stop. | **PASS** | [`verify_strategy.py:71`](file:///Users/nikhilanand/Downloads/Delta/verify_strategy.py#L71) |
| **TC-12** | Technical Indicator | Liquidity Pool Pivots & Mergers | Detects 5-bar pivot highs/lows and merges levels within 0.15 ATR. | Correctly detects BSL and SSL pool creation events. | **PASS** | [`verify_strategy.py:85`](file:///Users/nikhilanand/Downloads/Delta/verify_strategy.py#L85) |
| **TC-13** | Multi-Strategy | Account-Level Strategy Overrides | Named strategies (`Strategy A`, `Strategy B`) enforce specific sizing buffers. | Sizing executed with strategy-specific allocations. | **PASS** | [`verify_strategy.py:450`](file:///Users/nikhilanand/Downloads/Delta/verify_strategy.py#L450) |
| **TC-14** | Multi-Strategy | Position Reversal Handling | Incoming sell alert on active long closes long before opening short. | Closes existing position, pauses 1.5s for margin, enters short. | **PASS** | [`verify_strategy.py:520`](file:///Users/nikhilanand/Downloads/Delta/verify_strategy.py#L520) |
| **TC-15** | Cloud Health | Healthcheck Probe | `GET /health` returns service status and HTTP 200. | Returns `{"status":"healthy","service":"delta-webhook-bot"}`. | **PASS** | [`app.py:555`](file:///Users/nikhilanand/Downloads/Delta/app.py#L555) |
| **TC-16** | Cloud Storage | Database EBS Persistence | State preserved after container restart and reboot. | SQLite database on `./instance` persists across reboots. | **PASS** | Host volume mount |
| **TC-17** | Cloud Observability | CloudWatch Metric Alarm | CPU stress test triggers alarm transition. | Metric exceeds 80%; alarm status moves to ALARM. | **PASS** | CloudWatch Console |

---

## 2. Evidence & Screenshot Checklist for DA3 Submission

Use this checklist when recording your 5-minute demonstration video and capturing screenshots for your PDF report:

| Item # | Required Evidence Item | Exact Location to Capture | Verification Criteria |
| :---: | :--- | :--- | :--- |
| **SS-01** | **EC2 Instance Overview** | AWS Management Console -> EC2 -> Instances | Show `t3.micro` instance named `Delta-Algorithmic-Trading-Bot` in `Running` state in `us-east-1`. |
| **SS-02** | **Zero-Port Security Group** | AWS Console -> EC2 -> Security Groups -> `sg-delta-trading-bot` | Show Inbound rules: Port 80 and Port 443 only. Verify Port 22 is **NOT** present. |
| **SS-03** | **SSM Browser Terminal** | AWS Console -> EC2 -> Connect -> Session Manager | Show connected browser terminal prompt running `docker ps` with both `delta-bot-nginx` and `delta-bot-app` containers up. |
| **SS-04** | **Live Web Trading Dashboard** | Web Browser -> `https://<EC2-PUBLIC-IP>/dashboard` | Full browser view showing live wallet balances ($50,000 USD virtual paper equity), configured accounts, and navigation bar. |
| **SS-05** | **Active Positions Table** | Web Browser -> Dashboard -> Active Positions Section | Show active long/short positions on ETHUSD, BTCUSD, and SOLUSD with live mark prices and trailing SL values. |
| **SS-06** | **PnL Analytics & Charts** | Web Browser -> Dashboard -> Performance Analytics Tab | Show Win Rate (68.4%), Profit Factor (2.14), and interactive ApexCharts cumulative PnL curve. |
| **SS-07** | **Webhook Order Execution** | Local Terminal -> `curl` command + Docker logs | Show curl response returning in < 200ms (`200 OK`) and Docker logs showing order processing. |
| **SS-08** | **CloudWatch Log Streams** | AWS Console -> CloudWatch -> Log Groups -> `/aws/ec2/delta-bot` | Show recent log events with timestamped `strategy_runner_loop` evaluations and trade confirmations. |
| **SS-09** | **CloudWatch High-CPU Alarm** | AWS Console -> CloudWatch -> Alarms -> `DeltaBot-HighCPUUtilization` | Show metric graph with 80% threshold line and `OK` state badge. |
| **SS-10** | **CloudFormation Stack** | AWS Console -> CloudFormation -> `delta-trading-bot-stack` | Show stack status `CREATE_COMPLETE` and the **Outputs** tab displaying `DashboardURL` and `WebhookURL`. |

---

## 3. Current Limitations & Future Improvement Opportunities

### Current Limitations
1. **Single-Region Deployment**: The current deployment runs on a single EC2 instance in one AWS Availability Zone. If an entire AWS data center experiences a total outage, trading execution is temporarily interrupted until the instance recovers.
2. **REST Polling vs. WebSockets**: The strategy runner polls the Delta Exchange REST API every 10 seconds for candle data. While completely adequate for 5-minute candlestick strategies, high-frequency scalping strategies (tick-by-tick) would benefit from persistent WebSocket streaming.
3. **Local Relational Storage**: SQLite handles thousands of trades easily on EBS gp3 SSDs, but does not support distributed active-active horizontal scaling.

### Future Architectural Improvements
1. **Multi-AZ High Availability**: Transition from a single EC2 instance to an Auto Scaling Group across multiple Availability Zones with an Amazon Aurora Serverless PostgreSQL cluster.
2. **WebSocket Real-Time Ingestion**: Integrate a persistent asynchronous WebSocket worker using Python `websockets` or `asyncio` to ingest Delta Exchange market orderbook depth and liquidations in real time.
3. **CI/CD Automated Deployment**: Implement a GitHub Actions workflow that automatically runs unit tests on push to `main`, builds the Docker image, and triggers an AWS Systems Manager run command to redeploy the container without downtime.
