# Medical_AiBot 🩺

Medical_AiBot is an experimental conversational AI assistant designed to help answer medical questions by combining a LangChain-enabled Retrieval-Augmented Generation (RAG) backend with a lightweight React frontend.

Link: https://tinyurl.com/AIMediBot

## 🚀 Features
- Conversational RAG powered by LangChain and a vector store (Pinecone)
- PDF document ingestion and chunking for knowledge retrieval
- Environment-driven configuration (.env) for safe API key management

---

## 📦 Tech Stack
- Backend: Python, Flask, LangChain, Pinecone
- Embeddings: HuggingFace / sentence-transformers

---

## 🔧 Quick Start
Follow these steps to get the project running locally.

### Prerequisites
- Python 3.10+ (or a recent 3.x version)
- Pinecone account and API key
- OpenAI API key (or compatible LLM provider configured in env)

### Backend
1. Create and activate a virtual environment:
	```bash
	python -m venv .venv
	# Windows
	.venv\Scripts\activate
	# macOS / Linux
	source .venv/bin/activate
	```
2. Install backend dependencies:
	```bash
	pip install -r Backend/requirements.txt
	```
3. Create a `.env` in the `Backend/` directory with the following variables:
	```env
	OPENAI_API_KEY=your_openai_api_key_here
	PINECONE_API_KEY=your_pinecone_api_key_here
	```
4. Index your PDF documents (uploads are read from `Backend/data/`):
	```bash
	python Backend/store_index.py
	```
	This will create / populate a Pinecone index named `medical-assistant`.
5. Run the Flask server:
	```bash
	python Backend/app.py
	```
	The backend listens on http://localhost:8080 by default and exposes a POST `/ask` endpoint that expects JSON `{ "question": "..." }`.

---

## 🗂️ Project Structure (short)
  - `app.py` — Flask API and RAG chain
  - `store_index.py` — loads PDFs, creates embeddings, and stores vectors in Pinecone
  - `src/` — helper modules for loading, splitting, and embedding documents
  - templates/bot.html- Main page of bot
  - static/style.css- css for bot UI


---

## ⚠️ Security & Notes
- **Do not** commit `.env` or any API keys to source control.
- Pinecone and OpenAI usage may incur costs; monitor usage and quotas.

---


# 🚀 CI/CD Pipeline for Dockerized Application on AWS EC2

This project includes a **GitHub Actions workflow** that automates the build, push, and deployment of a Dockerized application to an **Amazon EC2 instance** using **Amazon Elastic Container Registry (ECR)**.

---

## 📦 Workflow Overview

The pipeline is defined in `.github/workflows/deploy.yml` and consists of two jobs:

### 1. Continuous Integration (CI)
- **Trigger**: Runs on every push to the `main` branch.
- **Steps**:
  - Checkout source code.
  - Configure AWS credentials using GitHub Secrets.
  - Authenticate with Amazon ECR.
  - Build Docker image.
  - Tag and push the image to ECR.

### 2. Continuous Deployment (CD)
- **Trigger**: Runs after CI completes successfully.
- **Runs on**: A **self-hosted runner** (your EC2 instance).
- **Steps**:
  - Checkout source code.
  - Configure AWS credentials.
  - Authenticate with Amazon ECR.
  - Stop and remove any container currently running on port `8080`.
  - Run the latest Docker image from ECR on port `8080`.

---

## 🔑 Secrets Required

You must configure the following secrets in your GitHub repository:

- `AWS_ACCESS_KEY_ID` – IAM user access key  
- `AWS_SECRET_ACCESS_KEY` – IAM user secret key  
- `AWS_DEFAULT_REGION` – AWS region (e.g., `us-east-1`)  
- `ECR_REPO` – Name of your ECR repository  
- `PINECONE_API_KEY` – Pinecone API key (if used in app)  
- `OPENAI_API_KEY` – OpenAI API key (if used in app)  

---

## 🖥️ Self-Hosted Runner Setup (EC2)

The **CD job** requires a self-hosted runner installed on your EC2 instance:

1. Launch an EC2 instance with Docker installed.  
2. Register the instance as a GitHub Actions self-hosted runner:  
   - Go to **GitHub → Settings → Actions → Runners → New self-hosted runner**.  
   - Follow the instructions to download and configure the runner.  
3. Ensure the runner has permission to run Docker commands.  

---

## ⚡ Deployment Flow

1. Developer pushes code to `main`.  
2. GitHub Actions builds and pushes Docker image to ECR.  
3. EC2 runner pulls the latest image.  
4. Old container on port `8080` is stopped and removed.  
5. New container is started on port `8080`.  

---

## ✅ Benefits

- **Automated builds** → No manual Docker commands needed.  
- **Zero-downtime deployment** → Old container stopped before new one starts.  
- **Secure** → AWS credentials and API keys managed via GitHub Secrets.  
- **Scalable** → Easily extend to multiple environments or ports.  