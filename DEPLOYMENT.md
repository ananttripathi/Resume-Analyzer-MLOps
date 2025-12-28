# 🚀 Deployment Guide

This guide covers deployment options for the Resume Analyzer MLOps project.

## Table of Contents

1. [HuggingFace Spaces (Recommended)](#huggingface-spaces)
2. [Local Deployment](#local-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)

---

## HuggingFace Spaces (Recommended)

### Prerequisites
- GitHub account
- HuggingFace account
- Git installed

### Step-by-Step Deployment

#### 1. Create HuggingFace Space

```bash
# Login to HuggingFace
pip install huggingface_hub
huggingface-cli login

# Create a new Space
# Go to: https://huggingface.co/spaces
# Click "Create new Space"
```

#### 2. Configure Space Settings

- **Space Name**: `resume-analyzer-mlops` (or your choice)
- **License**: MIT
- **SDK**: Gradio
- **SDK Version**: 4.8.0
- **Python Version**: 3.9

#### 3. Connect to GitHub Repository

```bash
# Initialize git in your project
cd Resume_Analyzer_MLOps
git init
git add .
git commit -m "Initial commit: Resume Analyzer MLOps"

# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/Resume_Analyzer_MLOps.git
git branch -M main
git push -u origin main
```

#### 4. Link Space to GitHub

In HuggingFace Space settings:
- Go to "Settings" → "Repository"
- Connect to your GitHub repository
- Enable automatic deployments

#### 5. Create README.md for HF Space

The project includes a `README.md` that works for HuggingFace Spaces.

#### 6. Push and Deploy

```bash
git add .
git commit -m "Configure for HF Spaces"
git push
```

Your app will automatically deploy! 🎉

**Access your app at**: `https://huggingface.co/spaces/YOUR_USERNAME/resume-analyzer-mlops`

---

## Local Deployment

### Option 1: Python Virtual Environment

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/Resume_Analyzer_MLOps.git
cd Resume_Analyzer_MLOps

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run Gradio app
python app.py

# Or run FastAPI backend
python api/main.py
```

Access the app at: `http://localhost:7860`

### Option 2: Using Conda

```bash
# Create conda environment
conda create -n resume_analyzer python=3.9
conda activate resume_analyzer

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run application
python app.py
```

---

## Docker Deployment

### Build and Run

```bash
# Build Docker image
docker build -t resume-analyzer .

# Run container
docker run -p 7860:7860 resume-analyzer
```

Access at: `http://localhost:7860`

### Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "7860:7860"
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    environment:
      - LOG_LEVEL=INFO
      - MAX_FILE_SIZE_MB=10
```

Run with:
```bash
docker-compose up
```

---

## Cloud Deployment

### AWS EC2

```bash
# 1. Launch EC2 instance (Ubuntu 20.04, t2.medium or larger)

# 2. SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# 3. Install dependencies
sudo apt update
sudo apt install -y python3-pip git

# 4. Clone and setup
git clone https://github.com/YOUR_USERNAME/Resume_Analyzer_MLOps.git
cd Resume_Analyzer_MLOps
pip3 install -r requirements.txt
python3 -m spacy download en_core_web_sm

# 5. Run with nohup
nohup python3 app.py > app.log 2>&1 &

# Access at: http://your-ec2-ip:7860
```

### Google Cloud Run

```bash
# 1. Install gcloud CLI
# 2. Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/resume-analyzer

# 3. Deploy to Cloud Run
gcloud run deploy resume-analyzer \
  --image gcr.io/PROJECT_ID/resume-analyzer \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --port 7860
```

### Azure Container Instances

```bash
# 1. Login to Azure
az login

# 2. Create resource group
az group create --name resume-analyzer-rg --location eastus

# 3. Build and push to ACR
az acr build --registry YOUR_REGISTRY --image resume-analyzer .

# 4. Deploy container
az container create \
  --resource-group resume-analyzer-rg \
  --name resume-analyzer \
  --image YOUR_REGISTRY.azurecr.io/resume-analyzer \
  --dns-name-label resume-analyzer \
  --ports 7860
```

---

## Environment Variables

Create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Edit values as needed:
- `HF_TOKEN`: For private HuggingFace models
- `LOG_LEVEL`: DEBUG, INFO, WARNING, ERROR
- `MAX_FILE_SIZE_MB`: Maximum upload size

---

## CI/CD Pipeline

### GitHub Actions

The project includes `.github/workflows/ci.yml` which:

1. **On Push/PR**:
   - Runs linting (flake8, black)
   - Executes tests with pytest
   - Generates coverage reports

2. **On Main Branch**:
   - Deploys to HuggingFace Spaces automatically

### Setup Secrets

Add to GitHub repository secrets:
- `HF_TOKEN`: Your HuggingFace token

---

## Monitoring & Logging

### Application Logs

Logs are stored in `logs/`:
- `app.log`: Application logs
- `analysis_log.jsonl`: Analysis metrics (JSONL format)

### View Logs

```bash
# Tail application logs
tail -f logs/app.log

# Parse analysis logs
python -c "
import json
with open('logs/analysis_log.jsonl', 'r') as f:
    for line in f:
        print(json.loads(line))
"
```

---

## Troubleshooting

### Common Issues

**1. spaCy model not found**
```bash
python -m spacy download en_core_web_sm
```

**2. Memory issues on small instances**
- Use at least 2GB RAM
- Reduce batch sizes
- Use lighter models

**3. Port already in use**
```bash
# Change port in app.py or use environment variable
export GRADIO_SERVER_PORT=8080
python app.py
```

**4. Model download fails**
```bash
# Use HuggingFace mirror
export HF_ENDPOINT=https://hf-mirror.com
```

---

## Performance Optimization

### Production Settings

1. **Use GPU** (if available):
```python
# In model initialization
job_matcher = JobMatcher(use_gpu=True)
```

2. **Enable Caching**:
```python
# Models are automatically cached
MODEL_CACHE_DIR=./model_cache
```

3. **Load Balancing** (for high traffic):
```bash
# Use gunicorn for FastAPI
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

## Support

For issues and questions:
- GitHub Issues: [Your Repo URL]
- Email: [Your Email]

---

## Next Steps

After deployment:
1. ✅ Test with sample resumes
2. ✅ Monitor logs for errors
3. ✅ Set up monitoring (optional)
4. ✅ Configure custom domain (optional)
5. ✅ Enable authentication (optional)

Happy Deploying! 🚀

