# 🚀 Sentivize - Advanced AI-Powered HR Analytics

## ⚡ Groq AI Integration - Version 2.0

**Sentivize** adalah sistem analisis HR yang revolusioner, kini didukung oleh **Groq AI** untuk memberikan analisis yang jauh lebih cerdas, cepat, dan kontekstual!

---

## 🌟 Key Features

### 🧠 Groq AI-Powered Analysis
- **Deep Reasoning Engine**: Analisis seperti HR profesional dengan konteks penuh
- **Multi-Model Support**: Llama 3, Mixtral, Gemma - pilih sesuai kebutuhan
- **Blazing Fast**: Response < 2 detik dengan Groq's LPU™ inference
- **Bilingual Understanding**: Natural Indonesian & English comprehension

### 👥 Advanced Employee Analysis
- ✅ Behavioral Profiling & Personality Assessment
- ✅ Big Five Personality Traits Detection
- ✅ Core Values Alignment
- ✅ Cultural Fit Evaluation
- ✅ Professional Maturity Scoring
- ✅ Sentiment & Emotion Analysis
- ✅ Red Flags & Green Flags Detection

### 📄 Intelligent CV/Resume Analysis
- ✅ Deep Semantic Understanding
- ✅ Context-Aware Skill Assessment
- ✅ Experience Quality Evaluation
- ✅ Achievement Impact Analysis
- ✅ Job Relevance Matching with Reasoning
- ✅ Automated Candidate Ranking
- ✅ Hiring Recommendations with Confidence Scores

### 📊 Dual-Mode Operation
- **🚀 Groq AI Mode**: Maximum intelligence dengan AI reasoning
- **⚡ Traditional NLP Mode**: Fast analysis dengan rule-based & TF-IDF
- **🔄 Automatic Fallback**: Seamless degradasi ke traditional mode

---

## 🎯 Quick Start

### 1. Prerequisites

- Python 3.8+
- Windows/Linux/Mac
- Internet connection (untuk Groq API)

### 2. Installation

```powershell
# Clone or navigate to project
cd Sentivize

# Create virtual environment (jika belum)
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Windows CMD:
.venv\Scripts\activate.bat

# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Get Groq API Key

1. Visit: **https://console.groq.com**
2. Sign up (FREE!)
3. Create API Key
4. Copy your API key

### 4. Configure API Key

```powershell
# Option A: Environment Variable (Recommended)
$env:GROQ_API_KEY = "gsk_your_api_key_here"

# Option B: Permanent Setup (Windows)
[System.Environment]::SetEnvironmentVariable('GROQ_API_KEY', 'gsk_your_api_key_here', 'User')
```

### 5. Run Application

```powershell
streamlit run app.py
```

Browser akan membuka di `http://localhost:8501`

### 6. Verify Installation

```powershell
# Run integration test
python test_groq_integration.py

# Expected output: "🎉 ALL TESTS PASSED!"
```

---

## 📚 Documentation

### Core Modules

1. **`groq_ai_reasoner.py`**
   - Core Groq AI reasoning engine
   - Deep contextual analysis
   - Multi-prompt templates for different analysis types

2. **`groq_employee_analyzer.py`**
   - Employee/candidate analysis dengan Groq
   - Behavioral profiling & personality assessment
   - Cultural fit evaluation

3. **`groq_cv_analyzer.py`**
   - CV/Resume deep analysis
   - Skills extraction & matching
   - Hiring recommendations

4. **`cv_parser.py`**
   - Universal document parser
   - Supports PDF, DOCX, TXT
   - Section extraction & contact info parsing

5. **`sentiment_analyzer.py`**
   - Multi-engine sentiment analysis
   - VADER, TextBlob, Transformers
   - Emotion profiling & tone analysis

6. **`groq_config.py`**
   - Configuration management
   - API key handling
   - Model selection

### User Interface

1. **`app.py`**
   - Main Streamlit application
   - Navigation & routing

2. **`advanced_employee_analyzer_page.py`**
   - Employee analysis UI
   - Data upload & configuration
   - Results visualization

3. **`advanced_cv_analyzer_page.py`**
   - CV analyzer UI
   - Batch CV analysis
   - Candidate ranking

---

## 🔧 Configuration

### Groq Models

```python
from groq_config import GroqConfig

# Available models:
GroqConfig.GROQ_MODEL = "llama3-8b-8192"      # Fast, balanced (Default)
GroqConfig.GROQ_MODEL = "llama3-70b-8192"     # Highest quality
GroqConfig.GROQ_MODEL = "mixtral-8x7b-32768"  # Large context
GroqConfig.GROQ_MODEL = "gemma-7b-it"         # Instruction-tuned
```

### Analysis Settings

```python
from groq_config import AnalysisConfig

# Enable/disable features
AnalysisConfig.USE_GROQ_AI = True
AnalysisConfig.USE_MOCK_MODELS = True
AnalysisConfig.ENABLE_BEHAVIORAL_ANALYSIS = True
AnalysisConfig.ENABLE_CULTURAL_FIT = True

# Performance tuning
AnalysisConfig.MAX_SOCIAL_POSTS = 20
AnalysisConfig.CV_TEXT_LIMIT = 4000
AnalysisConfig.BATCH_SIZE = 5
```

---

## 💻 Usage Examples

### Employee Analysis

```python
from groq_employee_analyzer import get_groq_employee_analyzer

# Initialize
analyzer = get_groq_employee_analyzer(enable_groq=True)

# Analyze
result = analyzer.analyze_employee(
    name="John Doe",
    position="Software Engineer",
    bio="Passionate about AI and sustainable tech",
    social_posts=[
        "Just shipped new microservices!",
        "Love collaborative teamwork",
        "Weekend learning Rust"
    ],
    keyword="innovation technology",
    company_values=["innovation", "collaboration", "excellence"]
)

# Access results
print(f"Score: {result['scores']['overall_score']}")
print(f"Recommendation: {result['recommendation']['decision']}")
```

### CV Analysis

```python
from groq_cv_analyzer import get_groq_cv_analyzer

# Initialize
analyzer = get_groq_cv_analyzer(enable_groq=True)

# Analyze CV
result = analyzer.analyze_cv(
    cv_file_or_text="path/to/resume.pdf",
    job_description="Senior Python Developer",
    required_skills=["Python", "Django", "AWS", "Docker"]
)

# Results
print(f"Candidate: {result.candidate_name}")
print(f"Overall: {result.overall_score}/100")
print(f"Decision: {result.hiring_decision}")
```

### Batch CV Analysis & Ranking

```python
# Batch analyze
results = analyzer.analyze_cv_batch(
    cv_files=[
        (cv1_data, "john.pdf"),
        (cv2_data, "jane.pdf"),
        (cv3_data, "bob.pdf")
    ],
    job_description="Full Stack Developer",
    required_skills=["React", "Node.js", "MongoDB"]
)

# Rank candidates
ranked = analyzer.rank_candidates(results)

for i, (result, rank_score) in enumerate(ranked, 1):
    print(f"{i}. {result.candidate_name}: {rank_score:.1f}")
```

---

## 📖 Detailed Guides

- **[GROQ_SETUP_GUIDE.md](GROQ_SETUP_GUIDE.md)** - Complete setup & configuration
- **[ADVANCED_AI_DOCUMENTATION.md](ADVANCED_AI_DOCUMENTATION.md)** - AI features documentation
- **[CV_ANALYZER.md](CV_ANALYZER.md)** - CV analyzer usage guide
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues & solutions

---

## 🎨 UI Features

### Employee Analyzer
- 📁 File upload (CSV, Excel, JSON)
- 🎯 Theme/value templates
- ⚙️ Configurable analysis options
- 📊 Rich visualizations
- 💾 Export results

### CV Analyzer
- 📄 Multi-file upload (PDF, DOCX, TXT)
- 🔍 Job description matching
- 🎯 Required skills specification
- 📈 Candidate ranking
- 📊 Detailed scoring breakdown
- 💡 AI recommendations

---

## 🛠️ Development

### Project Structure

```
Sentivize/
├── app.py                              # Main Streamlit app
├── groq_ai_reasoner.py                 # Core Groq AI engine
├── groq_employee_analyzer.py           # Employee analysis with Groq
├── groq_cv_analyzer.py                 # CV analysis with Groq
├── groq_config.py                      # Configuration management
├── cv_parser.py                        # Document parser
├── sentiment_analyzer.py               # Sentiment analysis
├── advanced_employee_analyzer_page.py  # Employee UI
├── advanced_cv_analyzer_page.py        # CV UI
├── advanced_employee_analyzer.py       # Traditional employee analyzer
├── advanced_cv_analyzer.py             # Traditional CV analyzer
├── advanced_ai_core.py                 # NLP core engine
├── services.py                         # Utility services
├── config.py                           # App configuration
├── test_groq_integration.py            # Integration tests
├── requirements.txt                    # Dependencies
└── GROQ_SETUP_GUIDE.md                # Setup guide
```

### Testing

```powershell
# Run all integration tests
python test_groq_integration.py

# Test specific modules
python groq_employee_analyzer.py
python groq_cv_analyzer.py
python sentiment_analyzer.py
python cv_parser.py
```

---

## 🔐 Security & Privacy

- ✅ API keys stored in environment variables
- ✅ No data sent to external servers (except Groq API for analysis)
- ✅ Local processing untuk document parsing
- ✅ Configurable data retention
- ✅ Secure HTTPS communication with Groq

---

## 📊 Performance

### Benchmarks (Average)

| Operation | Traditional | With Groq AI |
|-----------|-------------|--------------|
| Employee Analysis | 0.5s | 1.5s |
| CV Analysis | 1.0s | 2.0s |
| Batch (10 CVs) | 10s | 20s |

### Resource Usage

- **Memory**: ~200MB (without transformers), ~1GB (with transformers)
- **CPU**: Light usage (API calls offloaded to Groq)
- **Network**: ~1-5KB per API request

---

## 🚧 Troubleshooting

### Common Issues

**1. "Groq API key not found"**
```powershell
$env:GROQ_API_KEY = "gsk_your_key_here"
```

**2. "Module not found errors"**
```powershell
pip install -r requirements.txt --upgrade
```

**3. "Rate limit exceeded"**
- Wait 1 minute
- Reduce batch size
- Consider Groq paid tier

**4. "Analysis too slow"**
- Use Mock Models mode
- Disable Groq AI untuk faster processing
- Reduce text length limits

For more troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 🎓 Best Practices

1. **API Key Management**
   - Use environment variables
   - Never commit keys to version control
   - Rotate keys regularly

2. **Performance Optimization**
   - Batch analyze when possible
   - Use appropriate model for task
   - Cache results for repeated queries

3. **Analysis Quality**
   - Provide rich context (bio, posts, job description)
   - Use structured data when available
   - Review AI recommendations manually

4. **Error Handling**
   - Always have fallback to traditional mode
   - Log errors for debugging
   - Provide user-friendly messages

---

## 🔄 Updates & Changelog

### Version 2.0 (Groq Integration)
- ✨ Added Groq AI reasoning engine
- ✨ Deep contextual employee analysis
- ✨ Intelligent CV analysis with recommendations
- ✨ Multi-engine sentiment analysis
- ✨ Universal document parser
- ✨ Cultural fit evaluation
- ✨ Personality assessment (Big Five)
- ✨ Automated candidate ranking
- 🚀 Major performance improvements
- 📚 Comprehensive documentation

### Version 1.x
- Basic NLP analysis
- Social media scraping
- Keyword matching
- Simple sentiment analysis

---

## 📞 Support

Need help?

1. **Documentation**: Check guide files in project
2. **Issues**: Review error messages - they're descriptive
3. **Testing**: Run `python test_groq_integration.py`
4. **Groq Docs**: https://console.groq.com/docs

---

## 📜 License

This project is for educational and professional use.

---

## 🙏 Credits

- **Groq** for blazing-fast LLM inference
- **Streamlit** for amazing web framework
- **Hugging Face** for NLP models
- **Python community** for excellent libraries

---

## 🎉 Getting Started

```powershell
# 1. Install
pip install -r requirements.txt

# 2. Configure
$env:GROQ_API_KEY = "gsk_your_key_here"

# 3. Test
python test_groq_integration.py

# 4. Run
streamlit run app.py

# 5. Analyze! 🚀
```

---

**Ready to revolutionize your HR analytics with AI? Let's go! 🚀**
