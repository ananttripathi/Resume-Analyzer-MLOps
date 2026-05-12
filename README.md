---
title: Resume Analyzer
emoji: 📄
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: "4.8.0"
python_version: "3.9"
app_file: app.py
pinned: false
---

# 🚀 Intelligent Resume Analyzer + Job Match Recommendation System

[![HuggingFace Spaces](https://img.shields.io/badge/🤗-HuggingFace%20Space-blue)](https://huggingface.co/spaces/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 Overview

An end-to-end AI-powered system that analyzes resumes, extracts key information, and provides intelligent job matching recommendations. Built with MLOps best practices, featuring automated CI/CD pipelines and deployed on HuggingFace Spaces.

### ✨ Key Features

- **📄 PDF Resume Parsing**: Intelligent extraction of text from PDF resumes
- **🧠 NLP-Powered Analysis**: Uses transformer models for skill extraction and summarization
- **🎯 ATS Score Calculation**: Evaluates resume compatibility with Applicant Tracking Systems
- **🔍 Job Matching**: Semantic similarity matching using sentence embeddings
- **📊 Skill Gap Analysis**: Identifies missing skills for target roles
- **💡 Smart Recommendations**: Suggests improvements and suitable job roles
- **📈 MLOps Pipeline**: Complete CI/CD, model versioning, and monitoring

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Upload    │────▶│   FastAPI    │────▶│   ML Models │
│  Resume PDF │     │   Backend    │     │  (HF Hub)   │
└─────────────┘     └──────────────┘     └─────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │   Gradio UI  │
                    │   Frontend   │
                    └──────────────┘
```

## 🛠️ Tech Stack

### AI/ML
- **Transformers**: HuggingFace transformers for NLP tasks
- **Sentence-Transformers**: Semantic similarity and embeddings
- **spaCy**: Named Entity Recognition and text processing
- **PyPDF2**: PDF text extraction

### Backend
- **FastAPI**: High-performance API framework
- **Pydantic**: Data validation and settings management
- **Python 3.9+**: Core programming language

### Frontend
- **Gradio**: Interactive web interface
- **Plotly**: Data visualization

### MLOps
- **GitHub Actions**: CI/CD pipeline
- **HuggingFace Hub**: Model versioning and storage
- **HuggingFace Spaces**: Deployment platform
- **Docker**: Containerization (optional)
- **Pytest**: Testing framework
- **Black & Flake8**: Code quality tools

## 📦 Installation

### Local Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/Resume_Analyzer_MLOps.git
cd Resume_Analyzer_MLOps

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run the application
python app.py
```

### Docker Setup

```bash
# Build the image
docker build -t resume-analyzer .

# Run the container
docker run -p 7860:7860 resume-analyzer
```

## 🚀 Usage

### Web Interface

1. Launch the application: `python app.py`
2. Open your browser at `http://localhost:7860`
3. Upload a PDF resume
4. Optionally paste a job description
5. Click "Analyze Resume"
6. View results including:
   - ATS Score
   - Extracted Skills
   - Job Matches
   - Skill Gap Analysis
   - Improvement Recommendations

### API Usage

```python
import requests

# Upload resume
with open("resume.pdf", "rb") as f:
    files = {"file": f}
    data = {"job_description": "Python developer with ML experience"}
    response = requests.post(
        "http://localhost:8000/api/analyze",
        files=files,
        data=data
    )
    
print(response.json())
```

## 📂 Project Structure

```
Resume_Analyzer_MLOps/
├── src/
│   ├── __init__.py
│   ├── resume_parser.py       # PDF parsing and text extraction
│   ├── nlp_processor.py       # NLP models and skill extraction
│   ├── job_matcher.py         # Embedding-based job matching
│   ├── ats_scorer.py          # ATS score calculation
│   └── utils.py               # Helper functions
├── models/
│   ├── __init__.py
│   └── model_loader.py        # Model loading and caching
├── api/
│   ├── __init__.py
│   └── main.py                # FastAPI endpoints
├── tests/
│   ├── __init__.py
│   ├── test_parser.py
│   ├── test_nlp.py
│   └── test_api.py
├── data/
│   ├── sample_resumes/        # Sample resumes for testing
│   └── job_database.json      # Sample job descriptions
├── logs/
│   └── app.log                # Application logs
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI/CD
├── app.py                     # Main Gradio application
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
└── LICENSE                    # MIT License
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_parser.py -v
```

## 📊 MLOps Features

### 1. **Model Versioning**
- Models stored on HuggingFace Hub
- Version-controlled model artifacts
- Easy rollback capabilities

### 2. **CI/CD Pipeline**
- Automated testing on push
- Code quality checks (Black, Flake8)
- Automatic deployment to HF Spaces

### 3. **Monitoring & Logging**
- Request/response logging
- Performance metrics tracking
- Error monitoring and alerting

### 4. **Reproducibility**
- Pinned dependencies
- Seed setting for deterministic results
- Documented model versions

## 🎯 How It Works

### 1. Resume Parsing
```python
# Extract text from PDF
resume_text = parse_resume("resume.pdf")
```

### 2. Skill Extraction
```python
# Use NER and pattern matching
skills = extract_skills(resume_text)
experience = extract_experience(resume_text)
education = extract_education(resume_text)
```

### 3. ATS Scoring
```python
# Calculate ATS compatibility
ats_score = calculate_ats_score(
    resume_text,
    formatting_score,
    keyword_match,
    section_completeness
)
```

### 4. Job Matching
```python
# Generate embeddings and find similar jobs
resume_embedding = model.encode(resume_text)
job_embeddings = model.encode(job_descriptions)
similarities = cosine_similarity(resume_embedding, job_embeddings)
```

### 5. Skill Gap Analysis
```python
# Compare resume skills with job requirements
missing_skills = required_skills - resume_skills
recommendations = generate_recommendations(missing_skills)
```

## 🌐 Deployment

### HuggingFace Spaces

1. Create a new Space on HuggingFace
2. Connect your GitHub repository
3. Configure Space settings:
   - SDK: Gradio
   - Python version: 3.9
4. Push to main branch - auto-deployment triggers!

### Environment Variables

```bash
HF_TOKEN=your_huggingface_token  # For model access
LOG_LEVEL=INFO                    # Logging level
MAX_FILE_SIZE=10                  # Max upload size (MB)
```

## 📈 Performance Metrics

- **Resume Processing**: ~2-3 seconds per resume
- **ATS Score Calculation**: <1 second
- **Job Matching**: ~1-2 seconds for 100 jobs
- **API Response Time**: <5 seconds average

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- HuggingFace for model hosting and deployment
- Sentence-Transformers team for embedding models
- FastAPI team for the excellent framework
- Gradio team for the UI framework

## 📧 Contact

Your Name - [Your Email]

Project Link: [https://github.com/yourusername/Resume_Analyzer_MLOps](https://github.com/yourusername/Resume_Analyzer_MLOps)

---

Made with ❤️ and 🤖 by [Your Name]

