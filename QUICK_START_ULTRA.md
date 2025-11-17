# 🚀 Quick Start Guide - Sentivize Ultra v3.0

## ⚡ Instalasi & Jalankan dalam 3 Langkah

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

**Estimasi waktu:** 5-10 menit (tergantung koneksi internet)

### 2️⃣ Jalankan Aplikasi

```bash
streamlit run app_ultra.py
```

**Atau untuk port spesifik:**
```bash
streamlit run app_ultra.py --server.port 8503
```

### 3️⃣ Akses di Browser

Buka: **http://localhost:8501** (atau port yang dipilih)

---

## 🎯 Panduan Penggunaan Cepat

### Scenario A: Analisis CV Fresh Graduate untuk Posisi Admin

**Langkah-langkah:**

1. **Pilih Menu:** CV Analyzer
2. **Tab "Upload & Preview":**
   - Upload CV (PDF/DOCX/TXT)
   - Klik "Preview & Extract Data"
   - Lihat preview: nama, email, skills, experience, dll
3. **Tab "Analisis":**
   - Input Job Title: **Admin**
   - Input Job Description: 
     ```
     Mengelola administrasi kantor, membuat laporan, 
     komunikasi dengan tim. Skill: MS Office, komunikasi baik, 
     detail-oriented, attitude positif.
     ```
   - Klik "Mulai Analisis"
4. **Tab "Hasil":**
   - Lihat Job Complexity: **🟢 LOW (Entry-Level)**
   - Lihat Overall Score & Recommendation
   - Baca Executive Summary & Detailed Reasoning
   - Export hasil jika perlu

**Expected Result untuk Fresh Grad:**
- Overall Score: **70-85** (STRONG/EXCELLENT)
- Tier: **STRONG** atau **MEDIUM**
- Recommendation: **RECOMMEND** atau **CONSIDER**
- Reasoning: Menjelaskan bahwa fresh grad cocok untuk entry-level, fokus pada soft skills & attitude

### Scenario B: Analisis Karyawan untuk Promosi

**Langkah-langkah:**

1. **Pilih Menu:** Employee Analyzer
2. **Tab "Single Analysis":**
   - Input Target Position: **Supervisor Admin**
   - Input Job Criteria:
     ```
     Supervisor untuk tim admin. Requirements: 
     pengalaman 2+ tahun, leadership skills, 
     kemampuan koordinasi, communication, problem-solving.
     ```
   - Input Candidate Data:
     - Nama: John Doe
     - Posisi Saat Ini: Staff Admin
     - Skills: MS Office, koordinasi, komunikasi tim, reporting
     - Experience: Staff Admin PT ABC (3 tahun)
     - Bio: Berpengalaman mengelola dokumentasi, proaktif, team player
   - Klik "Mulai Analisis"
3. **Lihat Hasil:**
   - Job Complexity Analysis
   - Overall Score & Tier
   - Executive Summary
   - Key Strengths & Concerns
   - Position Fit Explanation
   - Export jika perlu

**Expected Result:**
- Overall Score: **75-90** (STRONG/EXCELLENT)
- Recommendation: **RECOMMEND** atau **STRONGLY RECOMMEND**
- Reasoning: Menjelaskan kesesuaian experience, leadership potential, dll

### Scenario C: Batch Screening 50 Kandidat

**Langkah-langkah:**

1. **Persiapkan File Excel/CSV:**
   ```
   Columns: name, position, skills, experience, bio
   
   Example:
   name          | position        | skills                  | experience           | bio
   John Doe      | Staff IT        | Python, React, SQL      | Junior Dev (2 th)    | Passionate developer
   Jane Smith    | Fresh Graduate  | Communication, Excel    | Org OSIS (1 th)      | Fast learner
   ...
   ```

2. **Pilih Menu:** Employee Analyzer
3. **Tab "Batch Analysis":**
   - Input Target Position: **Admin**
   - Input Job Criteria: *(sama seperti sebelumnya)*
   - Upload file Excel/CSV
   - Preview data
   - Klik "Mulai Batch Analysis"
   - Tunggu (estimasi: 10-30 detik per kandidat)
4. **Lihat Hasil:**
   - Summary stats: Total, Excellent, Strong, Avg Score
   - Table dengan semua kandidat (sorted by score)
   - Export to CSV/Excel

---

## 💡 Tips & Best Practices

### ✅ DO:

1. **Job Description Detail**
   - Jelaskan responsibilities, requirements, skills
   - Mention soft skills untuk entry-level
   - Mention hard skills untuk technical positions

2. **Entry-Level Jobs**
   - Gunakan kata: "Admin", "Entry", "Junior", "Staff"
   - Fokus pada soft skills di job description
   - Jangan khawatir dengan fresh graduate

3. **CV Data**
   - Input sebanyak mungkin informasi
   - Include pengalaman organisasi/volunteer
   - Mention projects untuk fresh grad

4. **Batch Analysis**
   - Pastikan format Excel/CSV konsisten
   - Check preview sebelum analyze
   - Use untuk initial screening

### ❌ DON'T:

1. **Jangan** expect keyword matching kaku
2. **Jangan** otomatis reject fresh grad untuk entry-level
3. **Jangan** input job description terlalu pendek (min 3-4 kalimat)
4. **Jangan** lupa export hasil untuk dokumentasi

---

## 🐛 Troubleshooting

### Issue: "Fresh graduate mendapat score rendah untuk Admin"

**Solution:**
- Pastikan job title mengandung kata entry-level: "Admin", "Staff", "Junior"
- Tambahkan soft skill requirements di job description
- System akan auto-detect sebagai LOW complexity dan scoring akan fleksibel

### Issue: "Error loading CV"

**Solution:**
- Check format file: PDF, DOCX, TXT
- Pastikan file tidak corrupted
- Untuk PDF, pastikan bukan scan image (harus text-based)
- Try convert ke TXT dan upload

### Issue: "Batch analysis terlalu lama"

**Solution:**
- Normal untuk banyak kandidat (10-30 detik per kandidat)
- Untuk 50 kandidat: estimasi 10-20 menit
- Run saat tidak sibuk
- Consider split menjadi multiple batches

### Issue: "Model download lambat"

**Solution:**
- First-time run akan download models (~2GB)
- Setelah itu models di-cache
- Pastikan koneksi internet stabil
- Jika gagal, delete folder `~/.cache/huggingface` dan retry

---

## 📊 Interpretasi Hasil

### Score Ranges:

| Score | Tier | Meaning | Action |
|-------|------|---------|--------|
| 85-100 | EXCELLENT 🏆 | Perfect fit | Strongly recommend interview |
| 70-84 | STRONG ⭐ | Good fit | Recommend interview |
| 55-69 | MEDIUM 👤 | Potential | Consider with evaluation |
| <55 | LOW ⚠️ | Not suitable | Consider other positions |

### Job Complexity:

| Level | Indicator | Scoring Focus | Fresh Grad? |
|-------|-----------|---------------|-------------|
| 🟢 LOW | Admin, CS, Entry | Soft skills 65% | ✅ YES |
| 🟡 MID | Coordinator, Analyst | Balanced | ⚠️ Maybe |
| 🔴 HIGH | Engineer, Manager | Hard skills 70% | ❌ NO |

### Recommendations:

| Recommendation | Meaning | Next Step |
|----------------|---------|-----------|
| ✅ STRONGLY RECOMMEND | Top candidate | Fast-track interview |
| 👍 RECOMMEND | Good candidate | Schedule interview |
| 🤔 CONSIDER | Potential candidate | Additional screening |
| ❌ NOT SUITABLE | Gap too large | Consider other roles |

---

## 🔗 Resources

- **Full Documentation:** `README_ULTRA.md`
- **Implementation Details:** Check module files in `ai/` and `analysis/`
- **Help in App:** Tab "Help" di Employee Analyzer page
- **Old Version:** `app_advanced.py` (v2.0) masih tersedia

---

## 📞 Support

Jika ada issue:
1. Check Troubleshooting section di atas
2. Review documentation files
3. Check terminal output untuk error messages
4. Contact development team

---

## 🎉 Selamat Menggunakan Sentivize Ultra!

Sistem ini dirancang untuk membuat recruitment lebih **adil**, **akurat**, dan **berbasis data**.

Fresh graduate untuk entry-level? **No problem!**
Batch screening 100 kandidat? **Easy!**
Human-like reasoning? **Built-in!**

**Happy Hiring! 🚀**
