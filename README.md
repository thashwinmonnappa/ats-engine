# AI Resume Screening Engine (ATS) - Version 2

An AI-powered **Applicant Tracking System (ATS) resume screening engine** that evaluates candidate resumes against job descriptions using **advanced skill extraction, experience analysis, semantic similarity scoring, and ontology-based matching**.

The system provides recruiters with **automated candidate ranking, skill gap detection, explainable scoring, and bulk processing capabilities**, enabling faster and more consistent resume screening for B2B applications.

## 🚀 Live Demo

[https://ats-engine-ashthwin.streamlit.app/](https://ats-engine-ashthwin.streamlit.app/)

---

## 📋 Project Overview

This project implements a **modern AI-powered ATS used by recruiters** to filter and evaluate resumes at scale.

Instead of simple keyword matching, the system performs:

- **Dynamic skill extraction** with ontology mapping
- **Experience requirement comparison** with alignment scoring
- **Semantic similarity** using transformer embeddings
- **Weighted scoring** across multiple evaluation factors
- **AI-generated candidate explanations** with hiring recommendations
- **Bulk resume processing** for high-volume screening
- **REST API** for integration with existing HR systems

The output helps recruiters quickly identify the **best matching candidates, their skill gaps, and experience alignment**.

---

## ✨ Key Features

### 📄 Multi-Format Resume Parsing

Supports multiple document formats:
- PDF (via pdfplumber)
- DOCX (via python-docx)
- TXT (plain text)

Extracts structured text for comprehensive analysis.

### 🛠️ Advanced Skill Extraction

Hybrid rule-based system extracts technical skills using:
- Curated technical vocabulary database
- Acronym detection (AWS, NLP, LLM, ML)
- CamelCase detection (LangChain, PyTorch)
- Hyphenated technologies (scikit-learn)
- Noise filtering for generic terms

### 🔄 Skill Normalization & Ontology

Skills are standardized using:
- Normalization engine (ML → machine learning)
- Synonym expansion (gen ai → generative ai)
- Ontology-based matching for related skills
- Hierarchical skill categorization

### ⚖️ Weighted Skill Matching

Skills are compared across different JD sections with varying importance:

| Section          | Weight | Purpose |
|------------------|--------|---------|
| Requirements     | High   | Core job needs |
| Technical Skills | Medium | Specific tech stack |
| Responsibilities | Medium | Role expectations |

### 📊 Experience Alignment Scoring

Experience requirements extracted from both resume and JD:

```
Resume: 2.9 years → JD: 4 years → Alignment Score: 72.5%
```

Evaluates how well candidates meet experience thresholds.

### 🧠 Semantic Similarity Scoring

Transformer-based embeddings compare contextual meaning:

- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Sections compared**: Experience vs Requirements, Skills vs Technical Skills
- **Benefit**: Detects relevance beyond exact keywords

### 📈 Final Candidate Score

Combines multiple scoring components:

| Component            | Weight | Description |
|----------------------|--------|-------------|
| Experience Alignment | 30%    | Years comparison |
| Skill Coverage       | 40%    | Weighted skill matching |
| Semantic Fit         | 30%    | Contextual similarity |

**Final Score Range**: 0-100 (higher = better match)

### 🤖 AI-Powered Explanations

Each candidate receives automated analysis:
- **Hiring verdict** (Strong/Moderate/Partial/Low Match)
- **Experience gap analysis**
- **Missing technical skills identification**
- **Strengths and recommendations**

### 📊 Recruiter Dashboard (Streamlit)

Interactive web interface for:
- Job description upload
- Bulk resume upload and processing
- Real-time candidate ranking
- Detailed scoring breakdowns
- Skill gap visualization
- AI explanation review
- Progress tracking for large batches

### 🔌 REST API (FastAPI)

Programmatic access for integrations:
- Single resume scoring: `POST /score`
- Bulk ranking: `POST /bulk_rank`
- JSON responses with detailed metrics

### ⚡ Bulk Processing Engine

Handles high-volume screening:
- Processes entire resume folders
- Parallel processing capabilities
- Error handling and logging
- Optimized for enterprise use

---

## 🏗️ System Architecture

The project follows a modular pipeline architecture:

```
Input (Resume + JD)
      │
├── Document Parser → Text Extraction
├── Section Segmenter → Structured Sections
│
├── Skill Extraction → Raw Skills
│   ├── Dynamic Extractor
│   └── JD-Specific Extractor
│
├── Skill Processing
│   ├── Normalization
│   └── Ontology Matching
│
├── Experience Extraction → Years Detection
│
├── Scoring Engine
│   ├── Weighted Skill Matcher
│   ├── Experience Matcher
│   ├── Semantic Matcher
│   └── Final Score Calculator
│
├── Explanation Generator → AI Analysis
│
└── Output
    ├── Dashboard (Streamlit)
    ├── API (FastAPI)
    └── Reports (JSON)
```

---

## 📁 Project Structure

```
resume_ats_engine_b2b/
│
├── app/                          # Core ATS Engine
│   ├── api.py                    # FastAPI REST endpoints
│   ├── bulk_ranker.py            # Bulk processing logic
│   ├── main.py                   # Single resume pipeline
│   │
│   ├── config/                   # Configuration files
│   │   └── scoring_weights.py    # Scoring parameters
│   │
│   ├── embeddings/               # Semantic similarity
│   │   ├── embedding_model.py
│   │   └── similarity_engine.py
│   │
│   ├── extraction/               # Skill & experience extraction
│   │   ├── dynamic_skill_extractor.py
│   │   ├── experience_extractor.py
│   │   ├── jd_skill_extractor.py
│   │   ├── skill_normalizer.py
│   │
│   ├── ontology/                 # Skill knowledge base
│   │   ├── ontology_loader.py
│   │   ├── ontology_matcher.py
│   │   └── skill_ontology.json
│   │
│   ├── parsing/                  # Document processing
│   │   ├── document_parser.py
│   │   ├── resume_parser.py
│   │   └── section_segmenter.py
│   │
│   ├── pipeline/                 # ATS Pipeline V2
│   │   └── ats_pipeline_v2.py
│   │
│   ├── ranking/                  # Ranking algorithms
│   │   ├── candidate_ranker.py
│   │   └── ranking_engine.py
│   │
│   ├── reporting/                # Output generation
│   │   ├── explanation_builder.py
│   │   └── explanation_generator.py
│   │
│   └── scoring/                  # Scoring components
│       ├── experience_matcher.py
│       ├── final_score_calculator.py
│       ├── section_scorer.py
│       ├── semantic_matcher.py
│       ├── weighted_scorer.py
│       └── weighted_skill_matcher.py
│
├── ui/                           # Dashboard components
│   ├── ai_insights.py
│   ├── dashboard_v2.py
│   ├── radar_chart.py
│   ├── score_cards.py
│   ├── skill_comparison_table.py
│   └── skill_gap_panel.py
│
├── ats/                          # Virtual environment
├── JD/                           # Sample job descriptions
├── resumes/                      # Sample resumes
│
├── app_1.py                      # Single resume test script
├── backend.py                    # SaaS backend (payments/auth)
├── bulk_test.py                  # Bulk processing test
├── dashboard.py                  # Main Streamlit dashboard
│
├── requirements.txt              # Frontend/dashboard dependencies
├── requirements-backend.txt      # API/backend dependencies
├── runtime.txt                   # Python version
├── start.sh                      # Deployment script
├── railway.toml                  # Railway deployment config
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/thashwinmonnappa/ats-engine.git
   cd ats-engine
   ```

2. **Create virtual environment**
   ```bash
   python -m venv ats
   ats\Scripts\activate  # Windows
   # source ats/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Streamlit Dashboard
```bash
streamlit run dashboard.py
```

#### Single Resume Test
```bash
python app_1.py
```

#### Bulk Processing Test
```bash
python bulk_test.py
```

#### API Server
```bash
pip install -r requirements-backend.txt
uvicorn app.api:app --reload
```

---

## 🔧 Configuration

### Scoring Weights

Modify `app/config/scoring_weights.py` to adjust scoring parameters:

```python
EXPERIENCE_WEIGHT = 0.3
SKILL_WEIGHT = 0.4
SEMANTIC_WEIGHT = 0.3
```

### Skill Ontology

Update `app/ontology/skill_ontology.json` to add new skills and relationships.

---

## 📦 Deployment

### Streamlit Cloud

1. Push to GitHub
2. Connect repository to Streamlit Cloud
3. Auto-deployment on commits

### Railway

```bash
# Uses railway.toml configuration
# Deploys with NIXPACKS builder
```

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["streamlit", "run", "dashboard.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

---

## 🛠️ Technology Stack

| Component          | Technology |
|--------------------|------------|
| **Backend**        | Python 3.8+ |
| **Web Framework**  | Streamlit, FastAPI |
| **Embeddings**     | Sentence Transformers |
| **NLP**            | Custom rule-based + spaCy |
| **Document Parsing**| pdfplumber, python-docx |
| **ML/AI**          | scikit-learn, Transformers |
| **Database**       | Supabase (SaaS features) |
| **Payments**       | Razorpay (SaaS features) |
| **Deployment**     | Railway, Streamlit Cloud |

---

## 🔮 Future Improvements

- **Enhanced Ontology**: Expand skill relationships and categories
- **Feedback Loop**: Recruiter feedback integration for model improvement
- **Advanced ML**: BERT-based skill extraction, custom embedding models
- **Scalability**: Distributed processing for enterprise-scale screening
- **Integrations**: ATS platform APIs (Greenhouse, Lever, Workday)
- **Analytics**: Hiring funnel analytics and bias detection
- **Mobile App**: React Native companion app
- **Multi-language**: Support for non-English resumes
- **Caching**: Redis for faster inference on repeated queries

---

## 📊 Performance Metrics

- **Processing Speed**: ~5-10 seconds per resume
- **Accuracy**: 85%+ skill extraction accuracy
- **Scalability**: Handles 100+ resumes in bulk processing
- **API Response**: <2 seconds for single resume scoring

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Thashwin Monnappa**

- Data Scientist
- LinkedIn: [thashwinmonnappa](https://linkedin.com/in/thashwinmonnappa)
- GitHub: [thashwinmonnappa](https://github.com/thashwinmonnappa)

---

## 🙏 Acknowledgments

- Sentence Transformers library for embeddings
- spaCy for NLP preprocessing
- Streamlit for rapid UI development
- FastAPI for robust API development