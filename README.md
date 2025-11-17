# 🔍 Sentivize Ultra - AI-Powered HR Analytics Platform

> **Ultra Advanced v3.0** - Sistem analisis karyawan dan CV berbasis AI murni dengan kemampuan reasoning setara HR profesional.

## 🌟 Mengapa Sentivize Ultra?

Sentivize Ultra adalah platform HR Analytics generasi ketiga yang menggunakan **pure AI semantic understanding** tanpa keyword matching. Sistem ini dapat memahami konteks, memberikan reasoning mendalam, dan beradaptasi dengan berbagai tingkat kompleksitas pekerjaan.

## ⚡ Fitur Unggulan v3.0

### 🎯 Job Complexity Auto-Detection
- **Automatic Analysis**: Deteksi otomatis kompleksitas pekerjaan (Low/Mid/High)
- **Adaptive Scoring**: Bobot penilaian menyesuaikan dengan level pekerjaan
- **Flexible Weights**: Fresh grad vs senior professional scoring
- **Context-Aware**: Memahami requirements implisit dari job description

### 📄 CV Preview & Smart Extraction
- **Instant Preview**: Lihat ekstraksi CV sebelum analisis penuh
- **Multi-Format Support**: PDF, DOCX, TXT dengan parsing sempurna
- **Comprehensive Data**: Nama, kontak, pendidikan, pengalaman, skills, projects
- **Initial Assessment**: Pra-analisis untuk screening cepat
- **Batch Processing**: Upload dan preview multiple CV sekaligus

### 🧠 Ultra CV Analyzer
- **Zero Keyword Matching**: 100% semantic AI understanding
- **Flexible Scoring System**: 
  - Entry-level friendly untuk fresh graduates
  - High standards untuk senior positions
- **Deep Skill Analysis**: Hard skills + soft skills detection
- **Experience Validation**: Quality over quantity
- **AI Reasoning Engine**: Penjelasan seperti HR profesional
- **Section-by-Section Scoring**: Contact, Education, Experience, Skills, Projects
- **Implicit Skills Detection**: Menemukan skills tersembunyi dari deskripsi

### 👥 Ultra Employee Analyzer
- **Single & Batch Analysis**: 1 kandidat atau ratusan sekaligus
- **Social Media Integration**: LinkedIn, Instagram, Facebook, Twitter/X
- **Deep Profile Analysis**: Beyond resume, into online presence
- **Sentiment Analysis**: Multi-layer emotional intelligence
- **Cultural Fit Assessment**: Personality dan work style analysis
- **Excel Export**: Comprehensive reports dengan reasoning

### 💡 Human-Friendly Output
- **Visual Cards**: Beautiful, expandable result cards
- **Progress Indicators**: Visual bars untuk setiap dimensi
- **Emoji Context**: 🎯 ⭐ 💡 untuk readability
- **Natural Language**: Output seperti conversation dengan HR expert
- **Actionable Insights**: Rekomendasi konkret, bukan hanya angka

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (Recommended: Python 3.9-3.11)
- 8GB RAM minimum (16GB recommended for smooth operation)
- Internet connection (for first-time model download ~2GB)

### Installation

1. **Clone repository**
```powershell
git clone https://github.com/AldyLoing/Sentivize.git
cd Sentivize
```

2. **Create virtual environment** (Recommended)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

> **Note**: First run akan download AI models (~2GB). Tunggu hingga selesai.

### Run Application

```powershell
streamlit run app_ultra.py
```

Aplikasi akan terbuka di `http://localhost:8501`

## 📖 Cara Penggunaan

### 🎯 CV Analyzer

**Tab 1: Upload & Preview**
1. Upload CV (PDF/DOCX/TXT) - support batch upload
2. Lihat preview ekstraksi otomatis
3. Verifikasi data yang ter-ekstrak

**Tab 2: Analisis**
1. Input job description atau kriteria
2. Sistem auto-detect kompleksitas pekerjaan
3. Klik "Analisis CV" dan tunggu proses

**Tab 3: Hasil**
1. Review comprehensive scoring (0-100)
2. Baca AI reasoning untuk setiap aspek
3. Lihat strengths, weaknesses, recommendations
4. Export ke Excel jika batch analysis

### 👥 Employee Analyzer

**Single Analysis:**
1. Input data kandidat (nama, posisi, bio, social media)
2. Pilih kriteria pencarian atau job requirements
3. System akan analyze profile dan online presence
4. Review hasil dengan detailed reasoning

**Batch Analysis:**
1. Upload Excel/CSV dengan kolom: nama, jabatan, unit, social media, bio
2. Input kriteria pencarian
3. Proses semua kandidat secara bersamaan
4. Download hasil lengkap dengan scoring dan reasoning

## 🏗️ Arsitektur Sistem

```
Sentivize/
├── ai/
│   ├── job_complexity_detector.py    # Auto-detect job complexity
│   └── cv_preview_extractor.py       # CV preview & extraction
├── analysis/
│   ├── ultra_cv_analyzer.py          # Advanced CV analysis
│   └── ultra_employee_analyzer.py    # Employee profiling
├── services/
│   ├── cv_parser_service.py          # Multi-format CV parsing
│   ├── social_media_service.py       # Social media integration
│   └── web_scraper_service.py        # Web scraping utilities
├── utils/
│   ├── human_friendly_formatter.py   # Beautiful output formatting
│   └── text_processor.py             # NLP utilities
├── models/
│   └── ai_models.py                  # AI model management
├── parsers/
│   ├── pdf_parser.py                 # PDF extraction
│   ├── docx_parser.py                # DOCX extraction
│   └── txt_parser.py                 # TXT extraction
├── advanced_ai_core.py               # Core AI engine
├── config.py                         # Configuration
├── app_ultra.py                      # Main application
├── ultra_cv_analyzer_page.py         # CV analyzer UI
├── ultra_employee_analyzer_page.py   # Employee analyzer UI
└── requirements.txt                  # Dependencies
```

## 🔧 Konfigurasi

### AI Models (config.py)
```python
# Embedding Model - Semantic Understanding
EMBEDDING_MODEL = "paraphrase-multilingual-mpnet-base-v2"

# Sentiment Model - Multilingual
SENTIMENT_MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

# NER Model - Entity Extraction
NER_MODEL = "dslim/bert-base-NER"

# Zero-shot Classifier - Flexible Classification
ZERO_SHOT_MODEL = "facebook/bart-large-mnli"
```

### Job Complexity Weights
```python
# Low Complexity (Fresh Graduate Friendly)
LOW_COMPLEXITY_WEIGHTS = {
    'soft_skills': 0.65,    # Prioritas soft skills
    'hard_skills': 0.35,
    'min_threshold': 40     # Passing score lebih rendah
}

# High Complexity (Senior Level)
HIGH_COMPLEXITY_WEIGHTS = {
    'soft_skills': 0.30,
    'hard_skills': 0.70,    # Prioritas technical skills
    'min_threshold': 70     # Standard lebih tinggi
}
```

## 🎯 AI Technology Stack

### Core Models
1. **Sentence Transformers** (`paraphrase-multilingual-mpnet-base-v2`)
   - 768-dimensional embeddings
   - Semantic similarity dengan 85%+ accuracy
   - Support 50+ languages termasuk Indonesia

2. **XLM-RoBERTa Sentiment** (`cardiffnlp/twitter-xlm-roberta-base-sentiment`)
   - Multilingual sentiment analysis
   - 3-class: Positive, Neutral, Negative
   - Fine-tuned on social media data

3. **BERT NER** (`dslim/bert-base-NER`)
   - Named Entity Recognition
   - Extract: Person, Organization, Location, Date
   - 95%+ precision on standard benchmarks

4. **BART Zero-Shot** (`facebook/bart-large-mnli`)
   - Flexible classification without training
   - Dynamic category detection
   - Context-aware labeling

### Analysis Pipeline
```
Input → Preprocessing → Feature Extraction → Multi-Model Analysis → 
Reasoning Generation → Score Aggregation → Human-Friendly Format → Output
```

### Key Algorithms
- **Semantic Similarity**: Cosine similarity on dense embeddings
- **Contextual Scoring**: Weighted aggregation based on job complexity
- **Implicit Detection**: Pattern matching + semantic clustering
- **Adaptive Thresholding**: Dynamic cutoffs based on data distribution

## 📊 Output & Reporting

### CV Analysis Output
```
📄 Candidate Profile
├── 🎯 Overall Score: 85/100
├── 💼 Match Quality: Excellent
├── 📈 Scoring Breakdown:
│   ├── Hard Skills: 90/100 ⭐⭐⭐⭐⭐
│   ├── Soft Skills: 80/100 ⭐⭐⭐⭐
│   ├── Experience: 88/100 ⭐⭐⭐⭐
│   └── Education: 82/100 ⭐⭐⭐⭐
├── 💡 AI Reasoning:
│   "Kandidat menunjukkan expertise kuat dalam..."
├── ✨ Strengths:
│   • Technical proficiency in [skills]
│   • Demonstrated leadership in [context]
├── ⚠️ Considerations:
│   • Limited experience in [area]
└── 🚀 Recommendations:
    • Consider for: Senior Developer role
    • Interview focus: System architecture
```

### Employee Analysis Output
- **Profile Summary**: Comprehensive overview
- **Sentiment Analysis**: Emotional intelligence assessment
- **Cultural Fit**: Personality & work style indicators
- **Social Presence**: Online professional footprint
- **Risk Flags**: Potential concerns or red flags
- **Hiring Recommendation**: Clear action items

### Excel Export Format
**Sheet 1: Analysis Results**
- Candidate details
- All scores (overall + dimensional)
- AI reasoning (full text)
- Strengths & weaknesses
- Recommendations

**Sheet 2: Summary Statistics**
- Distribution charts
- Average scores
- Top performers
- Analysis metadata

## 🔍 Troubleshooting

### ❌ Model Download Error
```
Error: Cannot download model from Hugging Face
```
**Solution:**
- Check internet connection
- Try using VPN if blocked
- Manually download models:
```powershell
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')"
```

### ❌ Memory Error
```
Error: Out of memory during processing
```
**Solution:**
- Process smaller batches (10-20 CVs at a time)
- Close other applications
- Use CPU instead of GPU (set in config.py)
- Restart application

### ❌ CV Parsing Error
```
Error: Cannot extract text from CV
```
**Solution:**
- Ensure CV is not password-protected
- Check file format (PDF/DOCX/TXT only)
- Try converting to different format
- Check if CV contains selectable text (not scanned image)

### ❌ Slow Performance
```
Issue: Analysis takes too long
```
**Solution:**
- First run always slow (model loading)
- Subsequent runs much faster (models cached)
- Reduce batch size
- Disable social media scraping
- Use SSD instead of HDD

### ❌ Type Error in Scoring
```
TypeError: can't multiply sequence by non-int
```
**Solution:**
- Update to latest version (v3.0+)
- Check requirements.txt versions
- Reinstall: `pip install -r requirements.txt --force-reinstall`

## 💎 Best Practices

### For CV Analysis
1. ✅ **Detailed Job Descriptions**: Semakin detail JD, semakin akurat matching
2. ✅ **Batch Processing**: Upload 10-50 CVs sekaligus untuk efficiency
3. ✅ **Review Preview**: Selalu cek preview ekstraksi sebelum analisis penuh
4. ✅ **Combine with Human Review**: AI adalah co-pilot, bukan replacement
5. ✅ **Multiple Criteria**: Test dengan beberapa variasi JD untuk perspective

### For Employee Analysis
1. ✅ **Complete Profiles**: Semakin lengkap data input, semakin baik hasil
2. ✅ **Social Media Optional**: Jangan paksa jika kandidat privacy-focused
3. ✅ **Contextual Search**: Gunakan kalimat lengkap, bukan hanya keywords
4. ✅ **Verify Results**: Cross-check AI findings dengan data faktual
5. ✅ **Respect Privacy**: Pastikan legal dan ethical use

### For Production Use
1. ✅ **Data Privacy**: Anonymize sensitive information
2. ✅ **Regular Updates**: Update models setiap 6 bulan
3. ✅ **Bias Monitoring**: Regular audit untuk fairness
4. ✅ **Version Control**: Track model versions dan configs
5. ✅ **Backup Data**: Backup results dan raw inputs

## ⚠️ Disclaimer & Ethics

### Data Privacy
- ❗ **Consent Required**: Pastikan kandidat aware data mereka diproses
- ❗ **GDPR Compliance**: Follow data protection regulations
- ❗ **Secure Storage**: Jangan simpan CV di public cloud tanpa encryption
- ❗ **Right to Delete**: Kandidat bisa request data deletion

### AI Limitations
- ⚠️ **Not 100% Accurate**: Model bisa error, selalu verify
- ⚠️ **Bias Potential**: AI bisa inherit bias dari training data
- ⚠️ **Context Dependent**: Hasil terbaik dengan data lengkap
- ⚠️ **Language Nuance**: Lebih optimal untuk English dan Indonesian

### Legal Considerations
- 📋 **Employment Law**: Patuhi regulasi hiring di region Anda
- 📋 **Discrimination**: Jangan gunakan AI sebagai satu-satunya kriteria
- 📋 **Transparency**: Kandidat berhak tahu jika dianalisis AI
- 📋 **Audit Trail**: Simpan log keputusan untuk accountability

## 📚 Documentation

### Main Documentation
- **README.md** (this file) - Overview dan quick start
- **README_ULTRA.md** - Technical deep dive (500+ lines)
- **QUICK_START_ULTRA.md** - Step-by-step tutorial
- **IMPLEMENTATION_SUMMARY_ULTRA.md** - Development summary
- **TROUBLESHOOTING.md** - Common issues & solutions

### Code Documentation
All modules have comprehensive docstrings:
```python
"""
Module: ultra_cv_analyzer.py
Purpose: Advanced CV analysis with flexible scoring
Features:
  - Job complexity detection
  - Adaptive weight adjustment
  - Multi-dimensional scoring
  - AI reasoning generation
"""
```

## 🚀 Roadmap & Future Features

### v3.1 (Q1 2026)
- [ ] Real-time interview question generator
- [ ] Candidate ranking comparison tool
- [ ] Integration dengan ATS systems
- [ ] Mobile-responsive UI

### v3.2 (Q2 2026)
- [ ] Video interview analysis (sentiment + body language)
- [ ] Skills gap analysis & training recommendations
- [ ] Predictive analytics for job success
- [ ] Multi-language UI (English, Indonesian, etc.)

### v4.0 (Q3 2026)
- [ ] Custom model fine-tuning interface
- [ ] Advanced bias detection & mitigation
- [ ] Integration dengan HR databases
- [ ] REST API untuk external integrations

## 🤝 Contributing

Contributions welcome! Areas yang bisa di-improve:
- **Model Performance**: Fine-tune untuk specific industries
- **UI/UX**: Enhance user experience
- **Documentation**: More examples dan use cases
- **Testing**: Unit tests dan integration tests
- **Localization**: Support more languages

## 📧 Support & Contact

- **Issues**: GitHub Issues untuk bug reports
- **Questions**: GitHub Discussions untuk pertanyaan
- **Documentation**: Lihat folder docs/ untuk guides
- **Email**: [Your contact email]

## 📜 License

MIT License - Free untuk personal dan commercial use dengan attribution.

### Attribution Required:
```
Powered by Sentivize Ultra v3.0
AI-Powered HR Analytics Platform
```

### Third-Party Licenses:
- Hugging Face Transformers: Apache 2.0
- Sentence Transformers: Apache 2.0
- Streamlit: Apache 2.0
- PyTorch: BSD 3-Clause

---

## 🎉 Version History

### v3.0 - Ultra Advanced (November 2025)
- ✨ Job complexity auto-detection
- ✨ CV preview & smart extraction
- ✨ Flexible scoring system
- ✨ Human-friendly output formatting
- ✨ Complete modular architecture

### v2.0 - Advanced (October 2025)
- 🚀 Zero keyword matching
- 🚀 Deep AI reasoning
- 🚀 Multi-dimensional scoring
- 🚀 ATS-level CV parsing

### v1.0 - Legacy (September 2025)
- 📊 Basic sentiment analysis
- 📊 Keyword-based matching
- 📊 Simple visualization
- 📊 Excel export

---

**Made with ❤️ by Sentivize Team**

**Status**: ✅ Production Ready  
**Version**: 3.0.0 Ultra Advanced  
**Last Updated**: November 17, 2025  
**Python**: 3.8+ Required  
**Models**: Hugging Face Transformers  
**Framework**: Streamlit
