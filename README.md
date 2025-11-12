# 🔍 Sentivize - Analisis Karyawan & CV dengan AI

Aplikasi web berbasis Streamlit untuk melakukan analisis data karyawan dan CV/resume menggunakan AI (sentiment analysis dan relevance scoring).

## 📋 Fitur Utama

### 🆕 CV/Resume Analyzer (NEW!)
- **Multi-Format Support**: PDF, DOCX, TXT
- **Batch Processing**: Upload dan analisis multiple CV sekaligus
- **Smart Extraction**: Auto-extract nama, email, phone, pendidikan, pengalaman, skills
- **Criteria Matching**: Support kata kunci, frasa, atau kalimat lengkap
- **AI-Powered Analysis**: Relevance + sentiment analysis per kandidat
- **Top 10 Display**: Expandable cards dengan detailed reasoning
- **Section Scoring**: Skor per section (Contact, Education, Experience, Skills)
- **Excel Export**: Download hasil analisis lengkap
- **📄 [Dokumentasi Lengkap CV Analyzer](CV_ANALYZER.md)**

### Employee Analysis
- **Multi-format File Support**: CSV, Excel (.xlsx, .xls), JSON
- **Smart Column Detection**: Deteksi otomatis kolom dengan struktur apapun
- **Adaptive File Parsing**: Handle file Excel kompleks (merged cells, multi-sheet, unnamed columns)
- **Semantic Search**: Support kata kunci, frasa, atau kalimat lengkap
- **Sentence-Level Understanding**: Analisis kesamaan makna, bukan hanya exact match
- **AI Reasoning Engine**: Penjelasan detail per kandidat kenapa mereka relevan

### AI & Analysis
- **Sentiment Analysis**: Hugging Face models (IndoBERT/Multilingual BERT)
- **Relevance Scoring**: Sentence-transformers untuk semantic similarity
- **Mock Mode**: Testing cepat dengan VADER + TF-IDF (tanpa download model besar)
- **Social Media Search**: Auto-search LinkedIn, Instagram, Facebook, Twitter/X
- **Context-Aware Matching**: Analisis di jabatan, unit, dan konten

### Visualization & Export
- **Top 10 Detailed Cards**: Expandable cards dengan reasoning lengkap
- **Interactive Charts**: Bar chart, pie chart, scatter plot, histogram
- **Export to Excel**: Download hasil dengan summary dan reasoning
- **Real-time Progress**: Progress bar dan status updates

## 🚀 Instalasi

### Prerequisites
- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Langkah Instalasi

1. **Clone atau download repository ini**
```powershell
cd e:\Orders\Project\Sentivize
```

2. **Install dependencies**

Untuk instalasi standar:
```powershell
pip install -r requirements.txt
```

Untuk instalasi CPU-only PyTorch (ukuran lebih kecil):
```powershell
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

**Catatan**: Instalasi pertama akan download model AI (~500MB) saat aplikasi pertama kali dijalankan dalam mode Transformers.

## 📖 Cara Menggunakan

### 1. Jalankan Aplikasi

```powershell
streamlit run app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`

### 2. Upload File Data

Siapkan file data karyawan dengan format:
- **Wajib**: Kolom nama (nama/name/nama_lengkap/full_name)
- **Opsional**: 
  - Jabatan (jabatan/position/posisi/role)
  - Unit kerja (unit/department/divisi/division)
  - Social media (social/sosial/instagram/linkedin/twitter)
  - Bio/deskripsi (bio/description/deskripsi/keterangan)

Contoh struktur CSV:
```csv
Nama,Jabatan,Unit,Social Media
John Doe,Manager,IT,https://linkedin.com/in/johndoe
Jane Smith,Analyst,Finance,
```

### 3. Konfigurasi Analisis

**Sidebar Options**:
- **Mock Mode**: Untuk testing cepat (tidak perlu download model)
- **Transformers Mode**: Untuk hasil terbaik (download model diperlukan)
- **Enable Scraping**: Coba ambil posting publik dari sosial media (opsional)

### 4. Masukkan Kata Kunci atau Kalimat

Sistem mendukung **3 jenis input**:

**A. Kata Kunci Tunggal:**
```
teknologi
kepemimpinan
hutan
```

**B. Frasa (2-3 kata):**
```
konservasi hutan
teknologi digital
manajemen sumber daya
```

**C. Kalimat/Maksud Lengkap:**
```
pengalaman dalam pengelolaan hutan lestari
kemampuan memimpin tim dan berkomunikasi efektif
ahli dalam teknologi informasi dan transformasi digital
berpengalaman menangani masalah lingkungan dan keberlanjutan
```

💡 **Tips**: 
- Gunakan kalimat untuk pencarian yang lebih spesifik dan akurat
- Sistem menggunakan analisis semantik untuk memahami kesamaan makna
- Semakin detail maksud, semakin tepat hasil yang didapat
- "lingkungan"
- "teknologi"
- "kepemimpinan"
- "inovasi"

### 5. Jalankan Analisis

Klik tombol **"🚀 Mulai Analisis"** dan tunggu prosesnya selesai.

### 6. Review Hasil

- **Tabel Hasil**: Lihat semua kandidat dengan skor sentiment dan relevansi
- **Visualisasi**: Bar chart top kandidat, pie chart distribusi sentiment
- **Filter**: Cari kandidat berdasarkan nama atau minimum relevance score
- **Download**: Download hasil dalam format Excel

## 📁 Struktur Proyek

```
Sentivize/
│
├── app.py                  # Main Streamlit application
├── config.py              # Configuration & constants
├── services.py            # Helper functions (file handling, web scraping)
├── ai_analyzer.py         # AI models (sentiment & relevance)
├── analyzer.py            # Main analysis pipeline
├── requirements.txt       # Python dependencies
└── README.md             # Documentation (this file)
```

## 🔧 Konfigurasi Lanjutan

Edit `config.py` untuk mengubah:

```python
# Model Configuration
SENTIMENT_MODEL = "indobenchmark/indobert-base-p1"
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

# Processing Limits
MAX_TEXT_LENGTH = 512
MAX_POSTS_PER_ACCOUNT = 5
MAX_SEARCH_RESULTS = 3
```

## 🧪 Testing Mode (Mock Models)

Untuk testing cepat tanpa download model besar:

1. Aktifkan checkbox **"Gunakan Mock Mode"** di sidebar
2. Mock mode menggunakan:
   - **VADER Sentiment** untuk sentiment analysis
   - **TF-IDF + Cosine Similarity** untuk relevance scoring

## ⚠️ Disclaimer & Batasan

1. **Tujuan Analisis**: Hasil bersifat indikatif, BUKAN untuk keputusan HR tunggal
2. **Data & Privasi**: Pastikan Anda memiliki hak memproses data yang diupload
3. **Web Scraping**: Dapat melanggar Terms of Service platform tertentu
4. **Akurasi AI**: Model memiliki keterbatasan dan dapat menghasilkan kesalahan
5. **Rate Limiting**: Pencarian web memiliki batasan request

## 🔍 Troubleshooting

### Error: Model tidak bisa didownload
**Solusi**: 
- Gunakan Mock Mode
- Pastikan koneksi internet stabil
- Install PyTorch versi CPU: `pip install torch --index-url https://download.pytorch.org/whl/cpu`

### Error: Kolom nama tidak ditemukan
**Solusi**: 
- Pastikan file memiliki kolom dengan nama: "nama", "name", "nama lengkap", atau "full name"
- Cek preview data untuk melihat nama kolom yang terdeteksi

### Proses terlalu lama
**Solusi**: 
- Gunakan Mock Mode untuk testing
- Matikan scraping
- Kurangi jumlah kandidat (<50)

### Error saat pencarian sosial media
**Solusi**: 
- Rate limiting dari search engine - tunggu beberapa menit
- Coba jalankan ulang dengan delay lebih lama
- Social media links dapat dimasukkan manual dalam file data

## 📊 Output Format

File Excel hasil analisis berisi 2 sheet:

### Sheet 1: Hasil Analisis
Kolom:
- Name
- Position
- Unit
- Social Media
- Social Media Count
- Search Performed
- Sentiment Label (POSITIVE/NEGATIVE/NEUTRAL)
- Sentiment Score (0-1)
- Relevance Score (0-1)
- Text Preview
- Texts Analyzed

### Sheet 2: Summary
Ringkasan statistik:
- Total kandidat
- Rata-rata scores
- Distribusi sentiment
- Coverage social media

## 🚧 Pengembangan Lebih Lanjut

Kode sudah didesain modular untuk pengembangan:

1. **FastAPI Backend**: Semua fungsi di `analyzer.py` dan `services.py` dapat digunakan sebagai API endpoints
2. **Database Integration**: Tambahkan penyimpanan hasil ke database
3. **Advanced Scraping**: Gunakan library khusus (selenium, playwright) untuk scraping lebih robust
4. **Custom Models**: Fine-tune model untuk domain spesifik
5. **Batch Processing**: Tambahkan job queue untuk analisis file besar

## 📝 Dependencies

Core libraries:
- `streamlit` - Web framework
- `pandas` - Data manipulation
- `transformers` - Hugging Face models
- `sentence-transformers` - Semantic embeddings
- `torch` - Deep learning framework

Search & Scraping:
- `duckduckgo-search` - Web search
- `googlesearch-python` - Google search
- `beautifulsoup4` - HTML parsing

Mock models:
- `vaderSentiment` - Rule-based sentiment
- `scikit-learn` - TF-IDF vectorization

Visualization:
- `plotly` - Interactive charts

## 📧 Support

Untuk pertanyaan atau issue, silakan:
1. Review dokumentasi di README
2. Check troubleshooting section
3. Review error messages di aplikasi

## 🎯 Best Practices

1. **Start dengan Mock Mode** untuk testing struktur file
2. **Batasi kandidat** (<50) untuk run pertama
3. **Validasi hasil** manual sebelum keputusan penting
4. **Backup data** sebelum proses
5. **Patuhi privasi** dan kebijakan data

## 📜 License

Aplikasi ini untuk tujuan edukasi dan research. Pastikan mematuhi:
- Terms of Service platform yang di-scrape
- Kebijakan privasi data karyawan
- Regulasi data protection (GDPR, dll)

---

**Version**: 1.0.0  
**Last Updated**: 2025-11-12
