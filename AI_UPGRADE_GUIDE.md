# 🚀 SENTIVIZE AI UPGRADE v3.0

## Ringkasan Upgrade

Sentivize telah di-upgrade dengan **AI Reasoning Engine** menggunakan **OpenRouter API** (model free: deepseek-chat) untuk analisis yang lebih cerdas, kontekstual, dan human-friendly.

---

## ✨ Fitur Baru

### 1. **OpenRouter AI Integration**
- Model: `deepseek-chat` (FREE, unlimited)
- Semantic reasoning untuk memahami konteks, bukan hanya keyword matching
- Temperature rendah (0.3) untuk hasil yang stabil dan konsisten

### 2. **Smart Job Complexity Detection**
Otomatis mendeteksi kompleksitas pekerjaan:
- **LOW**: Admin, kasir, staff entry-level, operator
  - Fokus: Soft skills, attitude, kemampuan belajar
  - Fresh graduate SANGAT FRIENDLY
  - Tidak menggugurkan kandidat tanpa pengalaman langsung
  
- **MID**: Supervisor, analyst junior, specialist
  - Balanced: Soft & hard skills
  - Fresh grad dengan skill kuat tetap dipertimbangkan
  
- **HIGH**: Engineer senior, data scientist, architect, manager
  - Fokus: Technical expertise, pengalaman relevan
  - Strict evaluation untuk memastikan kualitas

### 3. **CV Preview Before Analysis**
Sebelum analisis penuh, sistem menampilkan preview:
- ✅ Nama, kontak, pendidikan
- ✅ Total pengalaman (estimasi)
- ✅ Skill utama yang terdeteksi
- ✅ Level kandidat (Fresh Grad / Junior / Mid / Senior)
- ✅ Career pattern (Generalist / Specialist / Career Shifter)
- ✅ AI Career Summary (3-5 kalimat)
- ✅ Kekuatan yang terdeteksi

### 4. **Intelligent Scoring**
Scoring yang adil dan kontekstual:
- **Untuk LOW complexity job**: Tidak penalize fresh graduate
- **Potential Score**: Menilai potensi, bukan hanya track record
- **Transferable Skills**: Identifikasi skill yang bisa ditransfer dari pengalaman lain
- **Implicit Skills**: AI deteksi skill yang tidak ditulis eksplisit di CV

### 5. **Human-Friendly Output**
Semua output dalam bahasa natural yang mudah dipahami HR/Admin non-IT:
- ✅ Ringkasan eksekutif 3-5 kalimat
- ✅ Reasoning transparan
- ✅ Highlight strengths & concerns
- ✅ Rekomendasi actionable
- ✅ Alternative position suggestions
- ✅ Interview focus areas

### 6. **Batch Employee Analysis**
Analisis banyak karyawan sekaligus dari Excel/CSV:
- Auto-detect kolom walaupun struktur berantakan
- Semantic search berbasis makna
- Global summary untuk semua kandidat
- Export hasil ke Excel

---

## 🔧 Setup & Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies baru yang ditambahkan:
- `requests>=2.31.0` (untuk OpenRouter API)
- `httpx>=0.25.0` (async support)

### 2. Setup Environment Variables

Copy file `.env.example` menjadi `.env`:

```bash
cp .env.example .env
```

Edit `.env` dan isi dengan API key:

```env
OPENROUTER_API_KEY=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
```

> **Note**: API key di atas sudah disediakan dan GRATIS untuk model deepseek-chat.

### 3. Jalankan Aplikasi

```bash
streamlit run app_ultra.py
```

---

## 📁 Struktur File Baru

```
Sentivize/
├── ai/
│   ├── openrouter_engine.py        # NEW: OpenRouter AI integration
│   ├── cv_preview_extractor.py     # UPGRADED: AI-powered extraction
│   ├── job_complexity_detector.py  # UPGRADED: Better reasoning
│   └── advanced_ai_engine.py       # Legacy engine (fallback)
│
├── analysis/
│   ├── ultra_cv_analyzer.py        # UPGRADED: OpenRouter integration
│   └── ultra_employee_analyzer.py  # UPGRADED: Batch + OpenRouter
│
├── utils/
│   ├── env_loader.py               # NEW: Environment variable loader
│   └── human_friendly_formatter.py # Existing formatter
│
├── .env                            # NEW: Environment config (gitignored)
├── .env.example                    # NEW: Environment template
└── requirements.txt                # UPDATED: New dependencies
```

---

## 🎯 Cara Penggunaan

### A. CV / Resume Analyzer

1. **Upload CV** (PDF, DOCX, atau TXT)
2. **Preview Data**: Sistem ekstrak dan tampilkan preview
   - Nama, kontak, pendidikan
   - Pengalaman & skills
   - Level kandidat
   - AI career summary
3. **Input Job Description**
   - Judul posisi
   - Deskripsi lengkap
4. **Analisis**: AI reasoning mendalam
   - Job complexity detection
   - Semantic matching
   - Scoring dengan context awareness
5. **Lihat Hasil**:
   - Overall score & tier
   - Reasoning transparan
   - Strengths & weaknesses
   - Recommendations

### B. Employee Analyzer

#### Single Analysis:
1. **Input Job Requirements**
2. **Input Data Kandidat**
3. **Analisis** → AI reasoning
4. **Lihat Hasil**

#### Batch Analysis:
1. **Upload Excel/CSV** dengan kolom:
   - name
   - position
   - skills
   - experience / bio
2. **Input Job Requirements**
3. **Batch Analyze** → AI proses semua kandidat
4. **Download Hasil** dalam Excel

---

## 🧠 AI Reasoning Logic

### Untuk LOW Complexity Jobs (Admin, Kasir, dll):

```
IF candidate = fresh graduate:
    - DON'T penalize untuk "no experience"
    - FOCUS on: attitude, education, learning capability
    - PROJECT experience = valuable
    - ORGANIZATIONAL experience = relevant
    - POTENTIAL SCORE = high weight

SCORING WEIGHTS:
    - Soft skills: 35%
    - Hard skills: 15%
    - Experience: 15%
    - Organizational exp: 15%
    - CV clarity: 10%
    - Attitude/Potential: 10%
```

### Untuk HIGH Complexity Jobs (Engineer, Specialist):

```
IF candidate = experienced professional:
    - STRICT evaluation on technical skills
    - PORTFOLIO & projects = important
    - TRACK RECORD = critical
    
IF candidate = fresh graduate:
    - Need STRONG relevant projects
    - Internship experience = valuable
    - Technical certifications = plus

SCORING WEIGHTS:
    - Soft skills: 10%
    - Hard skills: 40%
    - Experience: 30%
    - Organizational exp: 5%
    - CV clarity: 5%
    - Attitude/Potential: 10%
```

---

## 🔐 Security & Privacy

1. **API Key Safety**:
   - `.env` file di-gitignore (tidak akan ter-commit)
   - API key tidak di-hardcode di source code
   - Gunakan environment variables

2. **Data Privacy**:
   - CV data tidak disimpan permanen
   - Hanya temporary file saat processing
   - OpenRouter tidak menyimpan data request (sesuai privacy policy)

---

## 📊 Output Examples

### CV Analysis Output:

```
✅ Kandidat: John Doe
📊 Overall Score: 82/100
🏆 Tier: STRONG

💭 Executive Summary:
"John adalah kandidat fresh graduate dengan latar belakang pendidikan S1 Manajemen. 
Meskipun belum memiliki pengalaman kerja formal, ia aktif di organisasi kampus 
sebagai Ketua BEM dan memiliki pengalaman project management. Kandidat menunjukkan 
POTENSI TINGGI untuk posisi Admin dengan kemampuan organisasi dan komunikasi yang baik."

💪 Key Strengths:
- Fresh graduate dengan pengalaman organisasi kuat
- Leadership experience (Ketua BEM)
- Soft skills lengkap: komunikasi, teamwork, time management
- Attitude: proaktif dan bertanggung jawab
- Quick learner dengan adaptability tinggi

⚠️ Key Weaknesses:
- Belum ada pengalaman kerja formal
- Skill teknis MS Office perlu development

✅ Recommendation: STRONGLY RECOMMEND
Posisi Admin adalah SANGAT COCOK untuk kandidat ini karena job complexity-nya LOW 
dan lebih mengutamakan soft skills serta attitude, yang mana kandidat miliki dengan baik.

🎯 Alternative Positions:
- Staff Administrasi
- Coordinator Assistant
- Customer Service

💡 Interview Focus Areas:
- Tanya detail pengalaman organisasi
- Test situasional untuk problem-solving
- Evaluasi kemampuan belajar cepat
```

---

## 🆘 Troubleshooting

### 1. "OpenRouter API: Not configured"

**Solusi**: 
- Pastikan file `.env` ada di root folder
- Cek isi `.env` ada `OPENROUTER_API_KEY=...`
- Restart aplikasi

### 2. "Error: API key invalid"

**Solusi**:
- Cek API key di https://openrouter.ai/keys
- Generate new key jika perlu
- Update di `.env` file

### 3. "AI analysis failed, using fallback"

**Solusi**:
- Cek koneksi internet
- OpenRouter mungkin down (rare)
- Aplikasi tetap jalan dengan fallback scoring (tidak pakai AI reasoning)

### 4. "CV extraction failed"

**Solusi**:
- Pastikan file CV valid (PDF/DOCX readable)
- Coba export CV ke format lain
- Cek ukuran file tidak terlalu besar (max 10MB)

---

## 🎓 Best Practices

### Untuk Admin/HR:

1. **Tulis Job Description yang Detail**:
   - Semakin detail, AI semakin akurat
   - Include: responsibilities, requirements, nice-to-have

2. **Trust AI Reasoning**:
   - AI sudah di-train untuk fair evaluation
   - Baca reasoning dengan seksama
   - Jangan pure lihat score, baca context

3. **Entry-Level Positions**:
   - Jangan expect fresh grad punya semua skill
   - Fokus pada POTENTIAL dan ATTITUDE
   - Project & organizational experience = valuable

4. **Batch Analysis**:
   - Siapkan Excel dengan kolom lengkap
   - Nama, posisi, skills, experience/bio
   - Semakin lengkap data, semakin akurat

### Untuk Developer:

1. **Extend AI Prompts**:
   - Edit `ai/openrouter_engine.py`
   - Customize system prompts untuk use case spesifik

2. **Add Custom Scoring Logic**:
   - Edit `analysis/ultra_cv_analyzer.py`
   - Tambah custom weights untuk industry tertentu

3. **Integrate Other AI Models**:
   - OpenRouter support 100+ models
   - Ganti model di `config.py`: `OPENROUTER_MODEL`

---

## 📈 Roadmap Future

- [ ] Multi-language support (English, Indonesia)
- [ ] Custom scoring templates per industry
- [ ] AI interview question generator
- [ ] Candidate comparison report
- [ ] Integration dengan ATS systems
- [ ] Mobile app version

---

## 🤝 Support

Jika ada pertanyaan atau issue:
1. Check TROUBLESHOOTING.md
2. Review dokumentasi ini
3. Contact: support@sentivize.app

---

## 📄 License

Sentivize v3.0 - All Rights Reserved
Powered by OpenRouter AI (deepseek-chat)
