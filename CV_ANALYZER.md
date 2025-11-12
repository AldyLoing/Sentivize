# 📄 CV/Resume Analyzer - Dokumentasi

## 🎯 Gambaran Umum

Fitur CV/Resume Analyzer adalah modul baru dalam aplikasi Sentivize yang memungkinkan Anda untuk menganalisis CV atau resume kandidat berdasarkan kriteria yang Anda tentukan. Fitur ini mendukung berbagai format file dan dapat menganalisis banyak CV sekaligus.

## ✨ Fitur Utama

### 1. **Multi-Format Support**
- **PDF**: Ekstraksi teks dari file PDF menggunakan PyPDF2
- **DOCX**: Ekstraksi dari Microsoft Word documents
- **TXT**: File teks biasa

### 2. **Upload Banyak File**
- Upload multiple CV sekaligus untuk analisis batch
- Proses otomatis dengan progress bar
- Hasil terurut berdasarkan skor relevansi

### 3. **Kriteria Fleksibel**
Anda dapat memasukkan kriteria dalam berbagai bentuk:
- **Kata Kunci Tunggal**: `Python`, `leadership`, `Excel`
- **Frase**: `machine learning`, `project management`
- **Kalimat Lengkap**: `pengalaman minimal 3 tahun dalam Python dan machine learning`

### 4. **Semantic Matching**
Sistem menggunakan teknologi semantic search untuk:
- Mendeteksi frase lengkap dalam CV
- Mencari bigram dan trigram yang relevan
- Mencocokkan kata kunci individual
- Memberikan bonus untuk urutan kata yang tepat

### 5. **Ekstraksi Informasi CV**
Sistem otomatis mengekstrak:
- **Nama Lengkap**: Dari bagian atas CV
- **Email**: Alamat email kandidat
- **Nomor Telepon**: Kontak telepon
- **Pendidikan**: Riwayat pendidikan
- **Pengalaman Kerja**: Riwayat pekerjaan
- **Skills**: Keahlian dan kompetensi

### 6. **AI-Powered Analysis**
Setiap CV dianalisis dengan:
- **Relevance Score**: Seberapa cocok CV dengan kriteria (0-1)
- **Sentiment Score**: Analisis tone/sentiment dari konten CV
- **Detailed Reasoning**: Penjelasan mengapa CV cocok/tidak cocok

### 7. **Section-Based Scoring**
Skor detail per section:
- 📧 Contact Info Score
- 🎓 Education Score
- 💼 Experience Score
- 🛠️ Skills Score

### 8. **Hasil Analisis Detail**
- Tampilan kartu expandable untuk setiap CV
- Informasi kontak lengkap
- Skor per section dengan progress bar
- AI Reasoning yang menjelaskan kecocokan

### 9. **Visualisasi**
- **Score Distribution**: Histogram distribusi skor
- **Sentiment Analysis**: Pie chart sentimen kandidat
- **Interactive Charts**: Grafik interaktif dengan Plotly

### 10. **Excel Export**
- Download hasil analisis lengkap dalam format Excel
- Include semua informasi: nama, kontak, skor, reasoning
- Siap untuk digunakan dalam proses rekrutmen

---

## 📋 Cara Menggunakan

### Step 1: Navigasi ke CV Analyzer
1. Buka aplikasi Sentivize di browser
2. Di sidebar kiri, pilih **"📄 CV/Resume Analyzer"**

### Step 2: Upload File CV
1. Klik area **"Pilih file CV/Resume (PDF, DOCX, TXT)"**
2. Pilih satu atau lebih file CV
3. Format yang didukung: `.pdf`, `.docx`, `.txt`
4. Multiple file upload supported

### Step 3: Masukkan Kriteria
Masukkan kriteria pencarian Anda. Contoh:

**Untuk kata kunci:**
```
Python, machine learning, SQL
```

**Untuk frase:**
```
project management, team leadership, data analysis
```

**Untuk kalimat:**
```
pengalaman minimal 3 tahun dalam pengembangan software menggunakan Python dan framework Django
```

**Tips:**
- Gunakan koma (,) untuk memisahkan multiple kriteria
- Sistem akan mencari exact phrases terlebih dahulu
- Kemudian mencari bigrams (2 kata berurutan)
- Terakhir mencari kata individual
- Urutan kata yang tepat mendapat bonus skor

### Step 4: Klik "Analisis CV"
1. Klik tombol **"🔍 Analisis CV"**
2. Tunggu proses selesai (progress bar akan muncul)
3. Proses mungkin memakan waktu tergantung jumlah file

### Step 5: Review Hasil

#### **Hasil Analisis CV**
Akan ditampilkan semua CV yang dianalisis dengan:
- Urutan berdasarkan Relevance Score (tertinggi ke terendah)
- Expandable card untuk detail setiap CV
- Informasi kontak (Email, Phone)
- Skor per section (Contact, Education, Experience, Skills)
- **AI Reasoning** yang menjelaskan tingkat kecocokan dengan kriteria

#### **Visualisasi**
- **Score Distribution**: Melihat distribusi skor semua CV
- **Sentiment Distribution**: Melihat sentimen keseluruhan

#### **Tabel Lengkap**
- Semua kandidat dengan skor lengkap
- Filter by nama atau minimum skor
- Sortable columns

### Step 6: Download Hasil
Klik tombol **"📥 Download Hasil Analisis (Excel)"** untuk:
- Mendapatkan file Excel lengkap
- Include: Nama, Email, Phone, Relevance Score, Sentiment Score, AI Reasoning
- Siap untuk proses seleksi lanjutan

---

## 🔧 Technical Details

### Arsitektur

```
cv_analyzer.py          # Backend logic untuk analisis CV
├── CVAnalyzer class
│   ├── extract_text_from_pdf()      # PyPDF2 untuk PDF
│   ├── extract_text_from_docx()     # python-docx untuk DOCX
│   ├── extract_text_from_txt()      # Text file handler
│   ├── extract_cv_sections()        # Regex-based section extraction
│   ├── analyze_cv_against_criteria() # Main analysis logic
│   └── analyze_multiple_cvs()       # Batch processing
│
cv_analyzer_page.py     # Frontend UI untuk CV analyzer
├── render_cv_analyzer_page()        # Main page renderer
├── analyze_cvs()                    # Processing with progress
└── display_cv_results()             # Results display dengan detail cards

app.py                  # Main application
└── Navigation sidebar              # Route to CV analyzer page
```

### Dependencies

```python
PyPDF2==3.0.1           # PDF text extraction
python-docx==1.1.0      # DOCX text extraction
re                      # Regex untuk section extraction
streamlit               # UI framework
pandas                  # Data manipulation
plotly                  # Visualizations
```

### Section Extraction Logic

Sistem menggunakan regex patterns untuk mengekstrak bagian CV:

```python
# Nama: 3 kata pertama dari CV
# Email: pattern [word]@[domain].[tld]
# Phone: pattern telepon Indonesia/international
# Pendidikan: keywords "pendidikan", "education", "universitas", dst
# Pengalaman: keywords "pengalaman", "experience", "pekerjaan", dst
# Skills: keywords "skill", "keahlian", "kompetensi", dst
```

### Scoring Algorithm

```python
# Relevance Score (0-1):
- Exact phrase match: 0.3 points per phrase
- Bigram match: 0.2 points per bigram
- Word match: 0.1 points per word
- Order bonus: +10% if correct order
- Normalization: score / max_possible_score

# Section Scores:
- Contact Info: Email + Phone presence
- Education: Length and keyword matches
- Experience: Length and keyword matches
- Skills: Length and keyword matches

# AI Reasoning:
Menggunakan existing AI analyzer untuk:
- calculate_relevance_with_reasoning()
- calculate_sentiment_score()
- Detailed explanation generation
```

---

## 💡 Tips & Best Practices

### 1. **Optimal Kriteria**
- **Spesifik**: Gunakan kriteria yang spesifik untuk hasil terbaik
  - ❌ Buruk: `pengalaman`
  - ✅ Baik: `pengalaman minimal 3 tahun dalam Python dan machine learning`

- **Kombinasi**: Gabungkan technical skills dengan soft skills
  ```
  Python, machine learning, team leadership, communication skills
  ```

### 2. **Format CV Kandidat**
- **Struktur Jelas**: CV dengan struktur jelas lebih mudah dianalisis
- **Heading Standar**: Gunakan heading seperti "Pendidikan", "Pengalaman", "Skills"
- **Format Konsisten**: Hindari format yang terlalu kompleks atau gambar terlalu banyak

### 3. **Batch Processing**
- Upload beberapa CV sekaligus untuk efisiensi
- Sistem akan otomatis mengurutkan berdasarkan relevansi (tertinggi ke terendah)
- Review hasil dengan skor tertinggi terlebih dahulu

### 4. **Interpretasi Hasil**

**Relevance Score Interpretation:**
- `0.8 - 1.0`: **Excellent** - CV sangat cocok dengan kriteria
- `0.6 - 0.8`: **Good** - CV cocok dengan banyak kriteria
- `0.4 - 0.6`: **Moderate** - CV cocok sebagian
- `0.2 - 0.4`: **Low** - Kandidat kurang cocok
- `0.0 - 0.2`: **Very Low** - Kandidat tidak cocok

**Sentiment Score Interpretation:**
- `0.7 - 1.0`: Positive tone (confidence, achievement)
- `0.4 - 0.7`: Neutral tone (factual)
- `0.0 - 0.4`: Negative tone (concerns)

### 5. **AI Reasoning**
Selalu baca **AI Reasoning** untuk memahami:
- Mengapa kandidat mendapat skor tersebut
- Kriteria mana yang match
- Kekuatan dan kelemahan kandidat
- Konteks dari matches yang ditemukan

---

## ⚠️ Keterbatasan & Disclaimer

### Keterbatasan Teknis

1. **OCR Tidak Didukung**
   - Sistem hanya bisa membaca text-based PDF
   - Scanned PDF (gambar) tidak akan ter-ekstrak dengan baik
   - Solusi: Gunakan OCR tool terlebih dahulu atau convert ke text

2. **Complex Layouts**
   - CV dengan layout kompleks (multi-column, table) mungkin ter-ekstrak tidak sempurna
   - Rekomendasi: CV dengan format sederhana dan linear

3. **Bahasa**
   - Optimized untuk Bahasa Indonesia dan English
   - Bahasa lain mungkin tidak ter-analyze dengan optimal

4. **File Size**
   - Recommended max 5MB per file
   - Multiple file upload: max total 50MB

### Disclaimer Penggunaan

⚠️ **PENTING**:

1. **Bukan Pengganti Manusia**
   - Hasil analisis adalah **indikasi awal** saja
   - TIDAK boleh digunakan sebagai satu-satunya dasar keputusan rekrutmen
   - Selalu review manual CV kandidat yang dipilih

2. **Bias & Fairness**
   - Sistem dapat memiliki bias berdasarkan kriteria yang Anda masukkan
   - Pastikan kriteria Anda non-diskriminatif
   - Review hasil untuk memastikan fairness

3. **Data Privacy**
   - Data CV hanya diproses di session Anda
   - Tidak disimpan di server
   - Pastikan Anda memiliki izin untuk memproses CV kandidat

4. **Akurasi**
   - Akurasi ekstraksi tergantung format CV
   - Selalu verifikasi informasi penting (email, phone)
   - Cross-check dengan CV original

---

## 🐛 Troubleshooting

### Issue 1: "File tidak bisa dibaca"

**Penyebab:**
- File corrupt atau password-protected
- Format tidak didukung
- File terlalu besar

**Solusi:**
1. Cek file bisa dibuka di aplikasi normal (Adobe Reader, Word)
2. Remove password protection
3. Convert ke format yang didukung (.pdf, .docx, .txt)
4. Compress file jika terlalu besar

### Issue 2: "Informasi tidak ter-ekstrak"

**Penyebab:**
- CV berbentuk gambar (scanned PDF)
- Layout terlalu kompleks
- Format tidak standar

**Solusi:**
1. Gunakan text-based PDF (bukan scan)
2. Convert ke format yang lebih sederhana
3. Manually input informasi penting

### Issue 3: "Skor terlalu rendah untuk kandidat bagus"

**Penyebab:**
- Kriteria terlalu spesifik
- Kata kunci tidak match dengan istilah di CV
- CV menggunakan istilah berbeda

**Solusi:**
1. Gunakan kriteria yang lebih luas
2. Include synonyms (e.g., "ML, machine learning, pembelajaran mesin")
3. Review AI Reasoning untuk memahami mismatch
4. Adjust kriteria berdasarkan feedback

### Issue 4: "Processing terlalu lama"

**Penyebab:**
- Too many files
- Files too large
- Complex criteria

**Solusi:**
1. Reduce jumlah files (10-20 per batch optimal)
2. Compress atau simplify CV files
3. Simplify criteria

---

## 📚 Contoh Use Cases

### Use Case 1: Rekrutmen Software Engineer

**Kriteria:**
```
Bachelor degree in Computer Science, 3+ years experience in Python, 
experience with Django or Flask, REST API development, 
PostgreSQL or MySQL, Git version control, agile methodology
```

**Expected Results:**
- CV dengan experience Python development
- Familiar dengan web frameworks (Django/Flask)
- Database experience
- Version control (Git)
- Agile/Scrum experience

**Action:**
1. Upload CV kandidat
2. Review hasil dengan relevance score tertinggi
3. Check AI Reasoning untuk understand match
4. Pilih CV yang paling sesuai untuk interview

---

### Use Case 2: Rekrutmen Data Analyst

**Kriteria:**
```
bachelor degree, strong analytical skills, 
experience with Excel, SQL, Python or R, 
data visualization with Tableau or Power BI,
statistical analysis, report writing
```

**Expected Results:**
- Kandidat dengan analytical background
- Technical skills: Excel, SQL, Python/R
- Visualization tools experience
- Communication skills (report writing)

**Action:**
1. Upload CV kandidat
2. Filter by Relevance Score >= 0.6
3. Review Education and Skills sections
4. Check Experience for analytical projects
5. Download Excel for further review

---

### Use Case 3: Rekrutmen Marketing Manager

**Kriteria:**
```
5+ years marketing experience, digital marketing expertise,
SEO and SEM knowledge, social media management,
content marketing strategy, team leadership,
budget management, campaign analytics
```

**Expected Results:**
- Senior marketing candidates
- Digital marketing focus
- Management experience
- Strategic thinking
- Analytics-driven

**Action:**
1. Upload CV pool
2. Focus on candidates with score > 0.7
3. Review Experience section carefully
4. Check for leadership experience
5. Verify achievements and results

---

## 🔄 Update Log

### Version 1.0 (Initial Release)
- ✅ Multi-format support (PDF, DOCX, TXT)
- ✅ Batch processing
- ✅ Semantic search dengan phrase/sentence support
- ✅ CV section extraction (Contact, Education, Experience, Skills)
- ✅ AI-powered relevance & sentiment analysis
- ✅ Detail display per CV dengan reasoning lengkap
- ✅ Section-based scoring
- ✅ Visualizations (score distribution, sentiment)
- ✅ Excel export functionality
- ✅ Complete documentation

### Planned Features (Future)
- 🔜 OCR support untuk scanned PDFs
- 🔜 Resume template suggestions
- 🔜 Skill gap analysis
- 🔜 Candidate comparison tool
- 🔜 Interview scheduling integration
- 🔜 Email notification untuk candidates
- 🔜 Multi-language support (enhanced)
- 🔜 Custom scoring weights

---

## 📞 Support

Jika Anda mengalami masalah atau memiliki pertanyaan:

1. **Check Documentation**: Baca dokumentasi ini terlebih dahulu
2. **Troubleshooting Guide**: Lihat section Troubleshooting
3. **Test dengan Sample Data**: Gunakan sample CV untuk test
4. **Check Format**: Pastikan file format sesuai requirement

---

## 🎓 Best Practices Summary

✅ **DO:**
- Gunakan kriteria spesifik dan jelas
- Upload CV dengan format standar dan simple
- Review hasil analisis secara manual
- Read AI Reasoning untuk context
- Combine technical dan soft skills criteria
- Download hasil untuk review lebih lanjut
- Verify informasi penting manual

❌ **DON'T:**
- Menggunakan hasil sebagai satu-satunya dasar keputusan
- Upload file dengan format tidak supported
- Menggunakan kriteria yang terlalu umum atau terlalu spesifik
- Ignore AI Reasoning
- Process too many files sekaligus (>50)
- Expect perfect extraction dari scanned PDFs
- Diskriminatif dalam kriteria

---

**Happy Recruiting! 🚀**

Untuk pertanyaan atau feedback tentang CV Analyzer, silakan hubungi tim development atau submit issue di repository.
