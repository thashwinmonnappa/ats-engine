# AI Resume Screening Engine (ATS)

An AI-powered **Applicant Tracking System (ATS) resume screening engine** that evaluates candidate resumes against job descriptions using **skill extraction, experience analysis, and semantic similarity scoring**.

The system provides recruiters with **automated candidate ranking, skill gap detection, and explainable scoring**, enabling faster and more consistent resume screening.

Live demo:
[https://ats-engine-ashthwin.streamlit.app/](https://ats-engine-ashthwin.streamlit.app/)

---

# Project Overview

This project simulates a **modern AI-powered ATS used by recruiters** to filter and evaluate resumes.

Instead of simple keyword matching, the system performs:

* Dynamic skill extraction
* Experience requirement comparison
* Semantic similarity using transformer embeddings
* Weighted scoring across multiple evaluation factors
* AI-generated candidate explanations

The output helps recruiters quickly identify the **best matching candidates and their missing skills**.

---

# Key Features

### Resume Parsing

Supports multiple document formats:

* PDF
* DOCX
* TXT

Extracts structured text for analysis.

---

### Dynamic Skill Extraction

A hybrid rule-based system extracts technical skills using:

* curated technical vocabulary
* acronym detection (AWS, NLP, LLM)
* CamelCase detection (LangChain, PyTorch)
* hyphenated technologies (scikit-learn)

Noise filtering removes generic words and non-technical phrases.

---

### Skill Normalization

Skills are standardized using a normalization engine.

Examples:

```
ML → machine learning
gen ai → generative ai
pyspark → spark
hugging face → huggingface
```

This ensures consistent skill matching across resumes and job descriptions.

---

### Weighted Skill Matching

Skills are compared across different sections of the job description:

| Section          | Weight |
| ---------------- | ------ |
| Requirements     | High   |
| Technical Skills | Medium |
| Responsibilities | Medium |

This improves realism compared to flat keyword scoring.

---

### Experience Alignment

Experience requirements are extracted from both resume and job description.

Example:

```
Resume experience: 2.9 years
JD requirement: 4 years
```

An alignment score evaluates how well the candidate meets the experience requirement.

---

### Semantic Similarity Scoring

Transformer-based embeddings compare the meaning of resume sections with job description sections.

Model used:

```
sentence-transformers/all-MiniLM-L6-v2
```

This allows the system to detect contextual relevance even when exact keywords differ.

---

### Final Candidate Score

The final score combines:

| Component            | Description                                 |
| -------------------- | ------------------------------------------- |
| Experience Alignment | Years of experience comparison              |
| Skill Coverage       | Weighted skill matching                     |
| Semantic Fit         | Contextual similarity between resume and JD |

Scores are normalized to provide an overall candidate fit score.

---

### AI Candidate Explanation

Each candidate receives an automated explanation including:

* hiring verdict
* experience gap analysis
* missing technical skills

Example verdict:

```
Strong Match — Recommended for Interview
Moderate Match — Review Recommended
Partial Match — Consider for Screening
Low Match — Not Recommended
```

---

### Recruiter Dashboard

A Streamlit-based dashboard allows recruiters to:

* Upload job descriptions
* Upload multiple resumes
* Automatically rank candidates
* View scoring breakdowns
* Identify missing skills
* Review AI explanations

Candidates are displayed in ranked order based on final score.

---

# System Architecture

The project follows a modular pipeline architecture:

```
Resume/JD Input
      │
Document Parser
      │
Section Segmentation
      │
Skill Extraction
      │
Skill Normalization
      │
Experience Extraction
      │
Weighted Skill Matching
      │
Semantic Similarity Scoring
      │
Final Weighted Scoring
      │
Explanation Generator
      │
Recruiter Dashboard
```

---

# Project Structure

```
resume_ats_engine_b2b
│
├── app
│   ├── parsing
│   │   ├── document_parser.py
│   │   ├── section_segmenter.py
│   │
│   ├── extraction
│   │   ├── dynamic_skill_extractor.py
│   │   ├── experience_extractor.py
│   │   ├── skill_normalizer.py
│   │
│   ├── embeddings
│   │   ├── embedding_model.py
│   │   ├── similarity_engine.py
│   │
│   ├── scoring
│   │   ├── section_scorer.py
│   │   ├── weighted_scorer.py
│   │   ├── weighted_skill_matcher.py
│   │
│   ├── reporting
│   │   ├── explanation_generator.py
│   │
│   ├── main.py
│   ├── api.py
│
├── dashboard.py
├── requirements.txt
```

---

# Deployment

The application is deployed using **Streamlit Cloud**.

Deployment workflow:

```
Local Development
      │
Git Commit
      │
Push to GitHub
      │
Streamlit Cloud Auto Build
      │
Live Application
```

Live URL:

[https://ats-engine-ashthwin.streamlit.app/](https://ats-engine-ashthwin.streamlit.app/)

---

# Technology Stack

| Component        | Technology                   |
| ---------------- | ---------------------------- |
| Backend          | Python                       |
| Web Interface    | Streamlit                    |
| Embeddings       | Sentence Transformers        |
| NLP              | Custom rule-based extraction |
| Resume Parsing   | pdfplumber, python-docx      |
| Machine Learning | scikit-learn                 |

---

# Future Improvements

Planned enhancements include:

* improved skill ontology
* recruiter feedback loop
* candidate shortlisting system
* CSV / PDF export reports
* caching for faster inference
* authentication and user accounts
* scalable API deployment

---

# Author

Thashwin Monnappa

Data Scientist

---