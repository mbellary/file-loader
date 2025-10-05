# file-loader

[![Powered by ChatGPT](https://img.shields.io/badge/Powered%20by-ChatGPT-10a37f?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/chatgpt)

The **file-loader** service is a foundational component of the *Unstruct AI Data Processing Pipeline*.  
It handles the **ingestion and loading of raw files** (PDFs, text, images, etc.) into cloud storage (e.g., AWS S3) and queues (e.g., SQS) for downstream processing by other services.

This repository is fully **Dockerized**, supports **AWS service emulation** via **LocalStack**, and provides **observability** through **Prometheus + Grafana**.

---

## 🧩 System Architecture Overview

The `file-loader` is one of several modular repositories that make up the full data pipeline:

| Component | Repository | Description |
|------------|-------------|-------------|
| **File Loader** | [`file-loader`](https://github.com/mbellary/file-loader) | Uploads and manages raw input files into S3 / SQS |
| **Ingestion** | `ingestion` | Listens to SQS messages and triggers file parsing |
| **Processor** | `processor` | Handles text cleaning, OCR, and metadata extraction |
| **Extractor** | `extraction` | Extracts entities, keywords, and structure from text |
| **Embeddings** | `embeddings` | Generates vector embeddings using AWS Bedrock (Titan models) |
| **Search** | `search` | Indexes processed data into OpenSearch for semantic retrieval |
| **Infra (Terraform)** | `infra` | Deploys shared AWS resources (VPC, ECS, Redis, DynamoDB, etc.) |

Each module is **decoupled**, runs independently in ECS Fargate, and communicates through AWS-managed services:
- **S3** for file and artifact storage  
- **SQS** for inter-service communication  
- **DynamoDB** for metadata and job tracking  
- **Redis** for caching and coordination  
- **OpenSearch** for search indexing and retrieval  

---

## ⚙️ Core Responsibilities

- Uploads raw files (PDF, DOCX, TXT, etc.) to **S3 buckets**
- Publishes file metadata and job info to **SQS** for ingestion service
- Optionally persists metadata to **DynamoDB**
- Logs and exposes operational metrics for **Prometheus**
- Integrates with **Grafana** for system observability
- Supports local development with **LocalStack** for AWS emulation

---

## 🏗️ Repository Structure

```
file-loader/
├─ src/file_loader/            # Core Python package
│  ├─ main.py                  # Entry point for worker or CLI
│  ├─ loader.py                # Handles file upload and SQS notification
│  ├─ utils/                   # Helper modules (logging, AWS, etc.)
│  └─ __init__.py
├─ data/                       # Sample input files for testing
├─ localstack_data/            # LocalStack persistent state
├─ grafana_data/               # Grafana storage
├─ Dockerfile.dev              # Development Docker image
├─ Dockerfile.prod             # Production Docker image
├─ docker-compose.yml          # App + LocalStack + Prometheus + Grafana
├─ prometheus.yml              # Prometheus scrape config
├─ requirements.txt            # Python dependencies
├─ pyproject.toml              # Build and packaging metadata
├─ LICENSE                     # Apache License 2.0
└─ README.md                   # Project documentation
```

---

## 🚀 Quickstart

### 1️⃣ Prerequisites

- Python 3.10+
- Docker & Docker Compose
- (Optional) AWS CLI and LocalStack CLI (`awslocal`)

### 2️⃣ Clone the repo

```bash
git clone https://github.com/mbellary/file-loader.git
cd file-loader
```

### 3️⃣ Launch with Docker Compose

```bash
docker compose up --build
```

This starts:
- `file-loader` app container
- `localstack` (mock AWS: S3, SQS, DynamoDB)
- `prometheus` (metrics)
- `grafana` (dashboards)

> Prometheus → [http://localhost:9090](http://localhost:9090)  
> Grafana → [http://localhost:3000](http://localhost:3000)  
> LocalStack → [http://localhost:4566](http://localhost:4566)

---

## 🧠 Local Development

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m file_loader
```

---

## ⚙️ Configuration

### Environment Variables (`.env`)

```env
# AWS LocalStack configuration
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
AWS_DEFAULT_REGION=ap-south-1
LOCALSTACK_ENDPOINT=http://localstack:4566

# S3 / SQS / DynamoDB resources
SOURCE_PATH=data/
DESTINATION_S3_BUCKET=unstruct-ingestion-bucket
SQS_QUEUE_NAME=unstruct-file-events
DYNAMODB_TABLE=unstruct-file-metadata

# Observability
LOG_LEVEL=INFO
PROMETHEUS_PORT=9091
```

Create your bucket and queue inside LocalStack:
```bash
docker exec -it localstack awslocal s3 mb s3://unstruct-ingestion-bucket
docker exec -it localstack awslocal sqs create-queue --queue-name unstruct-file-events
```

---

## 📦 Example Usage

### Python

```python
from file_loader import FileLoader

loader = FileLoader()
loader.load_file(
    source_path="data/sample.pdf",
    destination_bucket="unstruct-ingestion-bucket",
    queue_name="unstruct-file-events",
)
```

### CLI (optional)

```bash
file-loader load   --source data/sample.pdf   --bucket unstruct-ingestion-bucket   --queue unstruct-file-events
```

This:
1. Uploads the file to S3  
2. Sends a job notification to SQS  
3. Optionally records metadata in DynamoDB  
4. Exposes metrics to Prometheus  

---

## 📊 Observability

### Prometheus
- Configuration in `prometheus.yml`
- Scrapes metrics from the app’s `/metrics` endpoint
- Example metrics: file count, upload latency, SQS messages sent, errors

### Grafana
- Dashboards persisted in `grafana_data/`
- Default URL: [http://localhost:3000](http://localhost:3000)
- Default creds: `admin` / `admin`

You can create a dashboard to visualize:
- Upload throughput (files/sec)
- SQS message backlog
- Error rate
- DynamoDB write latency

---

## 🧩 Integration in the Meta-System

```
[file-loader] ──▶ [S3 bucket + SQS]
                       │
                       ▼
                [ingestion service]
                       │
                       ▼
                 [processor (OCR, NLP)]
                       │
                       ▼
                [extractor + embeddings]
                       │
                       ▼
                 [search (OpenSearch)]
```

Each component runs independently in AWS ECS (Fargate) and uses:
- **SQS** for triggering the next step
- **S3** for storing intermediate artifacts
- **DynamoDB** for state tracking
- **Redis** for caching
- **OpenSearch** for querying

---

## 🧪 Testing

Run local tests:
```bash
pytest -q
```

Lint and format:
```bash
ruff check src
black src
```

---

## 🚀 Deployment

In production, `file-loader` is deployed on **AWS ECS Fargate** through the **Terraform infra repo**:

- ECS Task Definition (includes environment variables, IAM role)
- Task Role grants access to S3, SQS, DynamoDB
- Logs sent to CloudWatch
- Prometheus metrics scraped via ECS service discovery

> CI/CD pipeline (GitHub Actions) handles automated build and deploy on push to `main`.

---

## 🧭 Roadmap

- [X] Add asyncio + parallel batch loading  
- [X] Integrate DynamoDB metadata writes  
- [X] Extend S3 multipart upload for large files  
- [X] Add CI/CD workflows for ECS deploy  
- [ ] Add example Grafana dashboards  
- [ ] Support cross-region uploads  


---

## 📜 License

Licensed under the [Apache License 2.0](./LICENSE).  
You’re free to use, modify, and distribute this code.

---

## 🧾 Author

**Mohammed Ali**  
📧 [www.linkedin.com/in/mbellary](www.linkedin.com/in/mbellary)

🌐 [https://github.com/mbellary](https://github.com/mbellary)

---

### 🤖 Powered by [ChatGPT](https://openai.com/chatgpt)
_This project was documented and scaffolded with assistance from OpenAI’s ChatGPT._

---
> _Part of the **Unstruct Modular Data Pipeline** — a fully containerized, serverless-ready ecosystem for ingestion, processing, and search._






