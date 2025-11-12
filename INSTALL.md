# 📦 Panduan Instalasi Lengkap - Sentivize

## Persiapan

### 1. Install Python

Download dan install Python 3.8+ dari https://www.python.org/downloads/

**Windows**: 
- Download installer
- Centang "Add Python to PATH"
- Klik "Install Now"

Verifikasi instalasi:
```powershell
python --version
pip --version
```

### 2. (Opsional) Buat Virtual Environment

Sangat disarankan untuk mengisolasi dependencies:

```powershell
# Navigasi ke folder project
cd e:\Orders\Project\Sentivize

# Buat virtual environment
python -m venv venv

# Aktivasi virtual environment
.\venv\Scripts\activate

# Setelah aktivasi, prompt akan berubah: (venv) PS>
```

## Instalasi Dependencies

### Opsi 1: Instalasi Standar (Recommended)

```powershell
pip install -r requirements.txt
```

**Catatan**: Ini akan download PyTorch dengan CUDA support (~2GB). Jika Anda tidak memiliki GPU, gunakan Opsi 2.

### Opsi 2: Instalasi CPU-Only (Lebih Kecil)

Untuk komputer tanpa GPU NVIDIA atau untuk menghemat space:

```powershell
# Install PyTorch CPU-only terlebih dahulu
pip install torch --index-url https://download.pytorch.org/whl/cpu

# Kemudian install dependencies lainnya
pip install streamlit pandas openpyxl numpy transformers sentence-transformers sentencepiece googlesearch-python duckduckgo-search beautifulsoup4 requests vaderSentiment textblob scikit-learn plotly matplotlib
```

### Opsi 3: Instalasi Bertahap (Jika Ada Error)

Jika instalasi gagal, coba install satu per satu:

```powershell
# Core dependencies
pip install streamlit
pip install pandas openpyxl numpy

# AI/ML Libraries
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install transformers
pip install sentence-transformers
pip install sentencepiece

# Search & Scraping
pip install googlesearch-python
pip install duckduckgo-search
pip install beautifulsoup4 requests

# Mock models
pip install vaderSentiment textblob scikit-learn

# Visualization
pip install plotly matplotlib
```

## Verifikasi Instalasi

Jalankan script test berikut:

```powershell
python -c "import streamlit; import pandas; import transformers; print('✅ All imports successful!')"
```

Jika tidak ada error, instalasi berhasil!

## Download Model AI (Otomatis)

Model AI akan otomatis didownload saat pertama kali aplikasi dijalankan dalam mode Transformers:

- **IndoBERT**: ~500MB (untuk sentiment analysis)
- **Sentence Transformers**: ~400MB (untuk relevance scoring)

**Catatan**: 
- Download memerlukan koneksi internet
- Download hanya dilakukan sekali, selanjutnya menggunakan cache
- Lokasi cache default: `~/.cache/huggingface/`

### Manual Download (Opsional)

Untuk pre-download model sebelum menjalankan aplikasi:

```python
from transformers import pipeline
from sentence_transformers import SentenceTransformer

# Download sentiment model
pipeline("sentiment-analysis", model="indobenchmark/indobert-base-p1")

# Download embedding model
SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
```

## Troubleshooting Instalasi

### Error: "pip is not recognized"

**Solusi**: Python tidak ditambahkan ke PATH
```powershell
# Gunakan full path
C:\Users\YourName\AppData\Local\Programs\Python\Python39\Scripts\pip.exe install -r requirements.txt
```

### Error: "Microsoft Visual C++ required"

**Solusi**: Download dan install Microsoft C++ Build Tools
- https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Error: "torch not compatible"

**Solusi**: Install versi spesifik
```powershell
pip install torch==2.1.2 --index-url https://download.pytorch.org/whl/cpu
```

### Error: Memory during model loading

**Solusi**: Gunakan Mock Mode (tidak perlu download model besar)
- Centang checkbox "Gunakan Mock Mode" di aplikasi

### Error: "googlesearch-python" tidak berfungsi

**Solusi**: Package ini kadang bermasalah, alternatif:
```powershell
pip uninstall googlesearch-python
pip install googlesearch-python==1.2.3
```

Atau hanya gunakan duckduckgo-search:
```powershell
pip install duckduckgo-search
```

### Error: SSL Certificate

**Solusi**: 
```powershell
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

## Konfigurasi Streamlit (Opsional)

Buat folder `.streamlit` dan file `config.toml`:

```powershell
mkdir .streamlit
```

Buat file `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 200
```

## Menjalankan Aplikasi

### Cara 1: Menggunakan run.bat (Windows)

Double-click file `run.bat`

### Cara 2: Command Line

```powershell
streamlit run app.py
```

### Cara 3: Dengan Port Spesifik

```powershell
streamlit run app.py --server.port 8502
```

Aplikasi akan terbuka di browser: `http://localhost:8501`

## Update Dependencies

Untuk update ke versi terbaru:

```powershell
pip install --upgrade -r requirements.txt
```

## Uninstall

Untuk menghapus virtual environment dan dependencies:

```powershell
# Deactivate virtual environment
deactivate

# Hapus folder venv
Remove-Item -Recurse -Force venv

# Hapus cache models (opsional)
Remove-Item -Recurse -Force $env:USERPROFILE\.cache\huggingface
```

## Instalasi untuk Production

Untuk deployment production (server):

1. **Gunakan requirements.txt yang sudah pinned**:
```powershell
pip freeze > requirements_locked.txt
```

2. **Setup systemd service (Linux)** atau **Task Scheduler (Windows)**

3. **Gunakan Gunicorn atau Nginx** untuk load balancing

4. **Set environment variables** untuk konfigurasi

## Rekomendasi Resource

### Minimum Requirements:
- RAM: 4GB
- Storage: 2GB free space
- CPU: Dual-core processor

### Recommended:
- RAM: 8GB+
- Storage: 5GB free space
- CPU: Quad-core processor
- GPU: NVIDIA GPU dengan CUDA (opsional, untuk speed up)

## Testing Instalasi

Jalankan test sederhana:

```powershell
# Test import semua module
python -c "import config; import services; import ai_analyzer; import analyzer; print('✅ All modules OK')"

# Test dengan Mock Mode
streamlit run app.py
# Centang "Gunakan Mock Mode" di sidebar
# Upload sample_data.csv
# Masukkan keyword: "lingkungan"
# Klik "Mulai Analisis"
```

## Next Steps

Setelah instalasi berhasil:

1. ✅ Baca `README.md` untuk panduan penggunaan
2. ✅ Coba dengan `sample_data.csv` yang disediakan
3. ✅ Eksplorasi fitur-fitur di aplikasi
4. ✅ Kustomisasi `config.py` sesuai kebutuhan

---

**Need Help?**
- Review error messages di terminal
- Check troubleshooting section di atas
- Pastikan semua prerequisites terpenuhi
