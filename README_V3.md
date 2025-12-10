# 🚀 SENTIVIZE v3.0 - AI-Powered HR Analytics

![Version](https://img.shields.io/badge/version-3.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![AI](https://img.shields.io/badge/AI-OpenRouter-orange.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)

> **Aplikasi web berbasis Python + Streamlit untuk analisis CV dan karyawan dengan AI reasoning yang cerdas dan kontekstual.**

---

## 🌟 Highlight Features

### 🤖 **AI Semantic Reasoning** (NEW!)
- Powered by **OpenRouter** dengan model `deepseek-chat` (FREE, unlimited)
- Memahami **KONTEKS**, bukan hanya keyword matching
- Reasoning seperti **HR profesional**
- Output **mudah dipahami** oleh non-IT user

### 🎯 **Smart Job Complexity Detection**
Otomatis kategorikan pekerjaan:
- **LOW**: Entry-level (admin, kasir) → Fresh grad friendly
- **MID**: Mid-level (supervisor, analyst) → Balanced evaluation  
- **HIGH**: Senior-level (engineer, manager) → Strict technical assessment

### 📊 **Dual Analysis Mode**
1. **CV/Resume Analyzer**
   - Upload PDF/DOCX/TXT
   - Preview ekstraksi otomatis
   - Deep semantic matching
   - Career trajectory analysis
   
2. **Employee Analyzer**
   - Single candidate analysis
   - Batch analysis (Excel/CSV)
   - Social media integration (optional)

### 💡 **Intelligent Scoring**
- **Potential-based** untuk fresh graduate
- **Transferable skills** detection
- **Implicit skills** identification (AI-powered)
- **Fair evaluation** sesuai job complexity

---

## 📸 Screenshots

### CV Preview Before Analysis
```
👤 John Doe
📧 john.doe@email.com | 📱 +62-812-xxx-xxxx

🎓 Pendidikan: S1 / Sarjana
💼 Level: Fresh Graduate
📊 Pengalaman: 0.5 tahun

🎯 Fokus: Administration & Operations
⚡ Skill Utama: MS Office, Communication, Teamwork

🌱 Fresh Graduate | 🌟 Leadership Experience

💭 AI Career Summary:
"Lulusan S1 Administrasi dengan pengalaman organisasi kuat sebagai Ketua BEM.
Menunjukkan leadership dan kemampuan koordinasi yang baik. Cocok untuk posisi
entry-level yang membutuhkan soft skills kuat dan learning agility tinggi."
```

### Analysis Result
```
✅ Kandidat: John Doe
📊 Overall Score: 85/100
🏆 Tier: STRONG
✅ Recommendation: STRONGLY RECOMMEND

💭 Executive Summary:
"Kandidat sangat cocok untuk posisi Admin. Meskipun fresh graduate, memiliki
pengalaman organisasi yang relevan, soft skills lengkap, dan attitude proaktif.
AI menilai kandidat memiliki POTENSI TINGGI untuk berkembang dalam 3-6 bulan."

💪 Key Strengths:
✅ Leadership experience (Ketua BEM)
✅ Soft skills: komunikasi, teamwork, time management
✅ Quick learner dengan adaptability tinggi
✅ Attitude: proaktif dan bertanggung jawab

🎯 Recommended Positions:
- Admin Staff (PERFECT MATCH)
- Coordinator Assistant
- Customer Service
```

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone <repository-url>
cd Sentivize
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Note**: First run akan download AI models (~1-2 GB). Pastikan koneksi internet stabil.

### 3. Setup Environment
```bash
# Copy template
cp .env.example .env

# Edit .env dan pastikan API key terisi:
# OPENROUTER_API_KEY=sk-or-v1-xxxx...
```

### 4. Test System
```bash
python test_ai_system.py
```

Jika semua test ✅ PASS, sistem siap digunakan!

### 5. Run Application
```bash
streamlit run app_ultra.py
```

Aplikasi akan terbuka di browser: `http://localhost:8501`

---

## 📖 User Guide

### A. CV/Resume Analyzer

**Step 1: Upload CV**
- Klik tab "Upload & Preview"
- Upload file CV (PDF/DOCX/TXT)
- Klik "Preview & Extract Data"

**Step 2: Review Preview**
- Lihat data yang berhasil diekstrak
- Review career summary dari AI
- Check detected skills & experience

**Step 3: Input Job Description**
- Pindah ke tab "Analisis"
- Input judul posisi (contoh: "Admin Staff")
- Input deskripsi lengkap pekerjaan
- Klik "Mulai Analisis"

**Step 4: View Results**
- Pindah ke tab "Hasil"
- Lihat score, tier, dan recommendation
- Baca AI reasoning secara detail
- Review strengths, weaknesses, dan recommendations

### B. Employee Analyzer

**Single Analysis:**
1. Input job requirements
2. Input data kandidat (nama, posisi, skills, experience)
3. Klik "Analisis"
4. Lihat hasil

**Batch Analysis:**
1. Prepare Excel/CSV dengan kolom:
   - `name`: Nama lengkap
   - `position`: Posisi saat ini
   - `skills`: Skills yang dimiliki
   - `experience`: Pengalaman kerja / bio
2. Upload file
3. Input job requirements
4. Klik "Batch Analyze"
5. Download hasil dalam Excel

---

## 🧠 How AI Works

### Job Complexity Detection

```python
# LOW Complexity (Admin, Kasir, Entry-level)
IF job_complexity == LOW:
    scoring_focus = {
        'soft_skills': 35%,      # TINGGI
        'attitude': 10%,         # TINGGI  
        'hard_skills': 15%,      # RENDAH
        'experience': 15%        # RENDAH (tidak penalize fresh grad)
    }
    
# HIGH Complexity (Engineer, Specialist)
IF job_complexity == HIGH:
    scoring_focus = {
        'hard_skills': 40%,      # TINGGI
        'experience': 30%,       # TINGGI
        'soft_skills': 10%,      # RENDAH
        'attitude': 10%
    }
```

### Fresh Graduate Evaluation

**Untuk LOW complexity jobs:**
```
✅ DO:
- Focus pada soft skills & attitude
- Value organizational experience
- Consider project/volunteer work
- Assess learning capability
- Give high potential score

❌ DON'T:
- Penalize "no experience"
- Strict keyword matching
- Ignore transferable skills
```

### Semantic Reasoning Process

1. **Context Understanding**: AI baca CV secara menyeluruh
2. **Pattern Recognition**: Identifikasi career trajectory, skill development
3. **Transferable Skills**: Detect skill dari konteks lain yang applicable
4. **Holistic Assessment**: Combine semua faktor dengan weighted scoring
5. **Human-like Reasoning**: Generate explanation yang natural & actionable

---

## 🔧 Configuration

### Environment Variables (`.env`)

```env
# Required
OPENROUTER_API_KEY=your_api_key_here

# Optional
DEBUG_MODE=false
MAX_UPLOAD_SIZE_MB=50
```

### Model Configuration (`config.py`)

```python
# OpenRouter settings
OPENROUTER_MODEL = "deepseek/deepseek-chat"  # Free model
OPENROUTER_TEMPERATURE = 0.3  # Low = stable, High = creative
OPENROUTER_MAX_TOKENS = 2000
```

### Scoring Weights (customize in code)

Edit `ai/job_complexity_detector.py`:

```python
def get_scoring_weights(self, complexity):
    if complexity == JobComplexity.LOW:
        return {
            'soft_skills': 0.35,  # Adjust ini
            'hard_skills': 0.15,  # Adjust ini
            # ...
        }
```

---

## 📊 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **AI Engine**: 
  - OpenRouter API (deepseek-chat)
  - Sentence Transformers (embeddings)
  - Transformers (NER, sentiment)
- **Data Processing**: Pandas, NumPy
- **Document Parsing**: pdfplumber, python-docx

---

## 🐛 Troubleshooting

### Issue: "OpenRouter API: Not configured"
**Solution**: 
- Check `.env` file exists
- Verify `OPENROUTER_API_KEY` is set
- Restart application

### Issue: "AI analysis failed, using fallback"
**Solution**:
- Check internet connection
- Verify API key is valid
- System will work with fallback scoring (no AI reasoning)

### Issue: "CV extraction failed"
**Solution**:
- Ensure CV file is valid and readable
- Try different format (PDF → DOCX or vice versa)
- Check file size < 10MB

### Issue: Models downloading too slow
**Solution**:
- First run downloads ~1-2GB models
- Use stable internet connection
- Or use Mock Mode (see TROUBLESHOOTING.md)

---

## 📚 Documentation

- **AI_UPGRADE_GUIDE.md**: Complete upgrade documentation
- **TROUBLESHOOTING.md**: Common issues & solutions
- **QUICK_START_ULTRA.md**: Quick start guide
- **IMPLEMENTATION_SUMMARY_ULTRA.md**: Implementation details

---

## 🎯 Roadmap

- [ ] Multi-language support (EN/ID)
- [ ] Custom industry templates
- [ ] AI interview question generator
- [ ] Candidate comparison report
- [ ] ATS integration
- [ ] Mobile app

---

## 📄 License

Sentivize v3.0 - Proprietary Software
All Rights Reserved © 2024

Powered by:
- OpenRouter AI (deepseek-chat)
- HuggingFace Transformers
- Sentence Transformers

---

## 🤝 Support

- **Documentation**: See `/docs` folder
- **Issues**: Create issue in repository
- **Email**: support@sentivize.app

---

## 🙏 Credits

Developed with ❤️ using:
- OpenRouter AI
- Streamlit
- HuggingFace Community

Special thanks to deepseek-ai for the free, powerful model!

---

**Made in Indonesia 🇮🇩**
