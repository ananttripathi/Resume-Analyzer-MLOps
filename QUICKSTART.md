# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Verify Setup

```bash
python verify_setup.py
```

### 3. Run the Application

```bash
python app.py
```

Open browser at: **http://localhost:7860**

---

## 📝 Usage Examples

### Upload Resume

1. Click "Upload Resume" button
2. Select PDF, DOCX, or TXT file
3. Click "Analyze Resume"

### Add Job Description (Optional)

1. Paste job description in text area
2. Get personalized matching score
3. View skill gap analysis

### View Results

- **Overview**: Contact info, experience years
- **ATS Score**: Compatibility score with feedback
- **Skills**: Extracted technical and soft skills
- **Job Match**: Similarity score and missing skills
- **Recommendations**: Personalized improvement tips

---

## 🔧 Run FastAPI Backend

```bash
python api/main.py
```

API docs at: **http://localhost:8000/docs**

### API Endpoints

**POST /api/analyze**
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@resume.pdf" \
  -F "job_description=Python developer with ML experience"
```

**GET /health**
```bash
curl http://localhost:8000/health
```

---

## 🐳 Docker Quick Start

```bash
docker build -t resume-analyzer .
docker run -p 7860:7860 resume-analyzer
```

---

## 📊 Sample Data

Sample job database included at `data/job_database.json`

Add sample resumes to `data/sample_resumes/` for testing

---

## 🧪 Run Tests

```bash
pytest tests/ -v
pytest tests/ --cov=src --cov-report=html
```

---

## 🚀 Deploy to HuggingFace Spaces

### Quick Deploy

1. Create HuggingFace Space
2. Connect to GitHub repo
3. Push code - auto-deploy!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

## 💡 Tips

- Keep resumes under 10MB
- Use simple formatting for best ATS scores
- Add job descriptions for personalized insights
- Check logs in `logs/app.log`

---

## 🆘 Troubleshooting

**Issue**: Models not loading
```bash
python -m spacy download en_core_web_sm
```

**Issue**: Port already in use
```bash
# Change port
python app.py --server-port 8080
```

**Issue**: Out of memory
- Use smaller models
- Process fewer files simultaneously

---

## 📚 More Resources

- Full documentation: [README.md](README.md)
- Deployment guide: [DEPLOYMENT.md](DEPLOYMENT.md)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Need Help?** Open an issue on GitHub!

