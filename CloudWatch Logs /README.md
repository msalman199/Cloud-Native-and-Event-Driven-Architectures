# 📊 View CloudWatch Logs with Open-Source Tools

<div align="center">

# 🚀 Lab Guide: Centralized Log Monitoring with Loki & Promtail

![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange?style=for-the-badge&logo=linux)
![Loki](https://img.shields.io/badge/Grafana-Loki-F46800?style=for-the-badge&logo=grafana)
![Promtail](https://img.shields.io/badge/Promtail-Log%20Shipper-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.x-yellow?style=for-the-badge&logo=python)
![Logging](https://img.shields.io/badge/Logging-Centralized-success?style=for-the-badge)
![DevOps](https://img.shields.io/badge/DevOps-Observability-purple?style=for-the-badge)

</div>

---

# 📖 Overview

In this lab, you will learn how to build a centralized logging platform using **Grafana Loki**, **Promtail**, and **LogCLI** as open-source alternatives to AWS CloudWatch Logs.

You will:

✅ Configure Loki as a log aggregation server

✅ Configure Promtail as a log shipping agent

✅ Generate application logs using Python

✅ Stream logs into Loki

✅ Search and filter logs using LogCLI

✅ Identify errors and warnings efficiently

---

# 📋 Prerequisites

Before starting this lab, ensure you have:

- Basic Linux command-line knowledge
- Understanding of log files and monitoring concepts
- Familiarity with text editors (nano or vim)
- SSH access to a Linux machine

---

# 🎯 Learning Objectives

By the end of this lab, you will be able to:

- Configure a centralized logging platform
- Create and organize application log streams
- Collect logs using Promtail
- Query logs using LogCLI
- Filter and search error events
- Analyze application behavior through logs

---

# 🏗️ Architecture

```text
+-------------------+
| Python Application|
+---------+---------+
          |
          v
+-------------------+
|     Promtail      |
|   Log Shipper     |
+---------+---------+
          |
          v
+-------------------+
|       Loki        |
| Log Aggregation   |
+---------+---------+
          |
          v
+-------------------+
|      LogCLI       |
| Query & Analysis  |
+-------------------+
```

---

# ⚙️ Environment Setup

## 📦 Step 1: Update System

```bash
sudo apt update
```

---

## 📦 Step 2: Install Dependencies

```bash
sudo apt install -y wget curl unzip
```

---

## 📥 Step 3: Install Loki

```bash
cd /tmp

wget https://github.com/grafana/loki/releases/download/v2.9.3/loki-linux-amd64.zip

unzip loki-linux-amd64.zip

sudo mv loki-linux-amd64 /usr/local/bin/loki

sudo chmod +x /usr/local/bin/loki
```

Verify:

```bash
loki --help
```

---

## 📥 Step 4: Install Promtail

```bash
wget https://github.com/grafana/loki/releases/download/v2.9.3/promtail-linux-amd64.zip

unzip promtail-linux-amd64.zip

sudo mv promtail-linux-amd64 /usr/local/bin/promtail

sudo chmod +x /usr/local/bin/promtail
```

Verify:

```bash
promtail --help
```

---

## 📥 Step 5: Install LogCLI

```bash
wget https://github.com/grafana/loki/releases/download/v2.9.3/logcli-linux-amd64.zip

unzip logcli-linux-amd64.zip

sudo mv logcli-linux-amd64 /usr/local/bin/logcli

sudo chmod +x /usr/local/bin/logcli
```

Verify:

```bash
logcli --help
```

---

# 🧩 Task 1: Enable Logging and Create Log Groups

---

## 🛠️ Step 1: Configure Loki

Create configuration directory:

```bash
sudo mkdir -p /etc/loki
```

Create configuration file:

```bash
sudo nano /etc/loki/config.yml
```

Paste:

```yaml
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    address: 127.0.0.1
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
  chunk_idle_period: 5m
  chunk_retain_period: 30s

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb:
    directory: /tmp/loki/index

  filesystem:
    directory: /tmp/loki/chunks

limits_config:
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 168h

chunk_store_config:
  max_look_back_period: 0s

table_manager:
  retention_deletes_enabled: false
  retention_period: 0s
```

Save and exit.

---

## ▶️ Step 2: Start Loki

Create storage directories:

```bash
sudo mkdir -p /tmp/loki/index
sudo mkdir -p /tmp/loki/chunks
```

Start Loki:

```bash
loki -config.file=/etc/loki/config.yml &
```

Verify:

```bash
curl http://localhost:3100/ready
```

Expected Output:

```text
ready
```

---

# 🧩 Task 2: Generate Application Logs

---

## 📁 Step 1: Create Demo Application

```bash
mkdir -p ~/log-demo

cd ~/log-demo
```

Create application:

```bash
nano app.py
```

Paste:

```python
#!/usr/bin/env python3

import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('DemoApp')

def main():
    counter = 0

    while counter < 20:
        counter += 1

        if counter % 5 == 0:
            logger.error(
                f"Error processing request {counter}: Connection timeout"
            )

        elif counter % 3 == 0:
            logger.warning(
                f"Warning: High memory usage detected at iteration {counter}"
            )

        else:
            logger.info(
                f"Successfully processed request {counter}"
            )

        time.sleep(2)

if __name__ == "__main__":
    logger.info("Application started")
    main()
    logger.info("Application finished")
```

---

## ▶️ Step 2: Run Application

```bash
chmod +x app.py

python3 app.py &
```

Verify logs:

```bash
tail -f /tmp/app.log
```

---

# 🧩 Task 3: Stream Logs Using Promtail

---

## ⚙️ Step 1: Configure Promtail

```bash
sudo mkdir -p /etc/promtail

sudo nano /etc/promtail/config.yml
```

Paste:

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://localhost:3100/loki/api/v1/push

scrape_configs:

  - job_name: system

    static_configs:
      - targets:
          - localhost
        labels:
          job: varlogs
          __path__: /var/log/*.log

  - job_name: application

    static_configs:
      - targets:
          - localhost
        labels:
          job: app
          app: demo
          __path__: /tmp/app.log
```

Save and exit.

---

## ▶️ Step 2: Start Promtail

```bash
promtail -config.file=/etc/promtail/config.yml &
```

Wait:

```bash
sleep 10
```

---

# 🔎 Task 4: Query and Analyze Logs

---

## 🌐 Step 1: Configure LogCLI

```bash
export LOKI_ADDR=http://localhost:3100
```

---

## 📄 Step 2: View All Application Logs

```bash
logcli query '{job="app"}' --limit=50 --since=5m
```

---

## ❌ Step 3: Search ERROR Logs

```bash
logcli query '{job="app"} |= "ERROR"' \
--limit=20 \
--since=5m
```

---

## ⚠️ Step 4: Search WARNING Logs

```bash
logcli query '{job="app"} |= "WARNING"' \
--limit=20 \
--since=5m
```

---

## 🔍 Step 5: Search Specific Pattern

```bash
logcli query '{job="app"} |= "Connection timeout"' \
--limit=10 \
--since=5m
```

---

## 📊 Step 6: Count Errors

```bash
logcli query \
'count_over_time({job="app"} |= "ERROR" [5m])' \
--since=5m
```

---

# ✅ Verification

---

## Verify Loki Status

```bash
curl http://localhost:3100/ready
```

Expected:

```text
ready
```

---

## Verify Labels

```bash
curl -G -s \
"http://localhost:3100/loki/api/v1/label" \
| python3 -m json.tool
```

Expected labels:

```text
job
app
```

---

## Verify Log Statistics

```bash
logcli stats '{job="app"}' --since=5m
```

---

## Verify Error Logs

```bash
logcli query '{job="app"} |= "ERROR"' \
--limit=5 \
--since=5m
```

Expected:

```text
At least 4 ERROR entries
```

---

## Verify Log File

```bash
ls -lh /tmp/app.log

cat /tmp/app.log | grep ERROR
```

---

# 📈 Expected Results

After successful completion:

✅ Loki running on port 3100

✅ Promtail shipping logs

✅ Application generating logs

✅ 20+ log entries collected

✅ 4 ERROR events identified

✅ 6 WARNING events identified

✅ Log filtering and searching operational

---

# 🛠️ Troubleshooting

---

## ❌ Loki Not Starting

Check port usage:

```bash
sudo netstat -tulpn | grep 3100
```

Kill conflicting process:

```bash
sudo kill -9 <PID>
```

---

## ❌ Promtail Not Sending Logs

Verify process:

```bash
ps aux | grep promtail
```

Check permissions:

```bash
sudo chmod 644 /tmp/app.log
```

---

## ❌ No Results in LogCLI

Wait for indexing:

```bash
sleep 30
```

Use larger window:

```bash
logcli query '{job="app"}' --since=10m
```

---

## ❌ Python Script Fails

Install Python:

```bash
sudo apt install -y python3
```

Run manually:

```bash
python3 app.py
```

---

## ❌ Permission Errors

Create directories:

```bash
sudo mkdir -p /tmp/loki/index

sudo mkdir -p /tmp/loki/chunks
```

Set permissions:

```bash
sudo chmod -R 755 /tmp/loki
```

---

# 🧹 Cleanup

Stop all processes:

```bash
pkill -f loki

pkill -f promtail

pkill -f app.py
```

Remove temporary files:

```bash
rm -rf /tmp/loki

rm -f /tmp/app.log

rm -f /tmp/positions.yaml
```

---

# 🎓 Conclusion

Congratulations! 🎉

You successfully built a centralized logging solution using open-source technologies.

## Key Accomplishments

✅ Installed Loki log aggregation platform

✅ Configured Promtail log shipping

✅ Generated structured application logs

✅ Streamed logs to a centralized service

✅ Queried logs using LogCLI

✅ Identified warning and error events

## Real-World Applications

🔹 Application Monitoring

🔹 Security Event Analysis

🔹 Infrastructure Troubleshooting

🔹 Compliance Auditing

🔹 Performance Investigation

🔹 DevOps Observability

---

# 🚀 Next Steps

- Install Grafana dashboards
- Create log alerting rules
- Build centralized observability pipelines
- Integrate metrics and traces
- Explore Kubernetes log aggregation
- Implement production-grade monitoring

---

## 🏆 Lab Completed Successfully!

**You now understand how centralized log aggregation, querying, filtering, and analysis work using Loki and Promtail — concepts directly applicable to AWS CloudWatch Logs and enterprise observability platforms.**
