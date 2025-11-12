# 🔧 Troubleshooting Guide - Sentivize

## 📋 Daftar Isi
1. [File Upload Issues](#file-upload-issues)
2. [Column Detection Problems](#column-detection-problems)
3. [Analysis Errors](#analysis-errors)
4. [Performance Issues](#performance-issues)
5. [Model Loading Issues](#model-loading-issues)
6. [Export Problems](#export-problems)

---

## 🗂️ File Upload Issues

### ❌ Error: "Format file tidak didukung"

**Penyebab:**
- Extension file tidak termasuk: `.csv`, `.xlsx`, `.xls`, `.json`

**Solusi:**
```bash
# Convert di Excel:
File → Save As → CSV UTF-8 (.csv)

# Atau Excel Workbook (.xlsx)
```

---

### ❌ Error: "Tidak dapat menemukan data valid dalam file Excel"

**Penyebab:**
- Semua sheet kosong
- Header tidak ditemukan di 10 baris pertama
- File corrupt

**Solusi:**
1. **Periksa struktur file:**
   - Pastikan ada minimal 1 sheet dengan data
   - Header di baris 1-10
   - Minimal 3 baris data

2. **Clean file di Excel:**
   ```
   - Delete empty rows di awal
   - Delete empty columns
   - Pastikan header jelas
   - Save as new file
   ```

3. **Try CSV export:**
   - Buka file di Excel
   - Select sheet dengan data
   - Save As → CSV UTF-8
   - Upload file CSV

---

### ❌ Error: "Error membaca file: ..."

**Penyebab:**
- Encoding issue (CSV)
- Corrupted file
- File terlalu besar

**Solusi:**

**Untuk CSV encoding issue:**
```python
# Open di Excel:
Data → From Text/CSV → Select encoding: UTF-8
Save as new file
```

**Untuk file corrupt:**
```
1. Buka di Excel
2. Copy semua data
3. Paste ke new workbook
4. Save as new file
```

**Untuk file terlalu besar (>50MB):**
```
1. Filter data yang diperlukan
2. Split menjadi beberapa file
3. Atau delete kolom tidak penting
```

---

## 🎯 Column Detection Problems

### ❌ Error: "Kolom nama tidak ditemukan"

**Penyebab:**
- Nama kolom tidak mengandung keywords: `nama`, `pegawai`, `karyawan`, `nip`, `staff`
- Kolom nama berisi data non-string
- Semua kolom unnamed

**Diagnosis:**
```
1. Buka Preview Data di UI
2. Lihat "Kolom Terdeteksi"
3. Expand "Semua Nama Kolom"
4. Periksa nama kolom actual
```

**Solusi 1: Rename kolom di Excel**
```
# Rename header kolom menjadi:
"Nama" atau "Nama Lengkap" atau "Nama Pegawai"

# Sistem akan otomatis mendeteksi
```

**Solusi 2: Pastikan data string**
```
# Di Excel:
1. Select kolom nama
2. Format Cells → Text
3. Pastikan tidak ada formula
4. Save
```

**Solusi 3: Fix unnamed columns**
```
# Jika preview menunjukkan: unnamed:_0, unnamed:_1, ...

Di Excel:
1. Periksa baris pertama - apakah ini header?
2. Jika tidak, insert row di atas
3. Ketik header: "Nama", "NIP", "Jabatan", etc
4. Save dan re-upload
```

---

### ⚠️ Warning: "Menggunakan kolom '...' sebagai kolom nama"

**Arti:**
- Sistem tidak menemukan kolom dengan keyword
- Fallback ke kolom dengan data string terbanyak

**Validasi:**
```
1. Periksa Preview Data
2. Cek apakah kolom yang digunakan benar
3. Jika salah, rename kolom di Excel
```

---

### ⚪ Optional columns tidak terdeteksi

**Kolom Opsional:**
- Jabatan
- Unit Kerja
- Social Media
- Deskripsi

**Dampak:**
- Analisis tetap berjalan
- Informasi tambahan tidak digunakan

**Solusi (jika ingin dideteksi):**
```
Rename kolom dengan keywords:
- Jabatan: "Jabatan", "Posisi", "Position"
- Unit: "Unit", "Bagian", "Divisi"
- Social: "Social Media", "Link", "Facebook"
- Text: "Deskripsi", "Keterangan", "Info"
```

---

## 🔍 Analysis Errors

### ❌ Error: "Tidak ada kandidat yang berhasil dianalisis!"

**Penyebab:**
1. Semua baris nama kosong/invalid
2. Column detection salah
3. Data format error

**Diagnosis:**
```python
# Check debug output di terminal:
DEBUG INFO:
- Total rows: ...
- Name column: ...
- Detected columns: ...
- Sample names: ...
```

**Solusi:**

**1. Periksa data nama:**
```
Di Preview Data:
- Pastikan kolom nama terisi
- Pastikan bukan NaN/null
- Pastikan format text, bukan number
```

**2. Clean data:**
```
Di Excel:
1. Filter kolom nama ≠ blank
2. Trim whitespace (=TRIM(A2))
3. Remove special characters
4. Save
```

**3. Cek terminal output:**
```powershell
# Lihat terminal untuk errors:
PS> cd e:\Orders\Project\Sentivize
PS> .\.venv\Scripts\streamlit run app.py

# Look for:
"✅ Kolom nama terdeteksi: '...'"
"Processing candidate: ..."
```

---

### ❌ Error saat processing candidate tertentu

**Penyebab:**
- Special characters di nama
- Very long text
- Encoding issue

**Solusi:**
```python
# Clean special characters:
=SUBSTITUTE(SUBSTITUTE(A2, CHAR(10), " "), CHAR(13), " ")

# Limit text length:
=LEFT(A2, 100)
```

---

### ⚠️ Relevance Score selalu 0

**Penyebab:**
- Keyword tidak cocok dengan data
- Text column tidak terdeteksi
- Mock mode limitation

**Solusi:**
```
1. Gunakan keyword yang lebih general
2. Pastikan ada text/description column
3. Atau keyword ada di nama/jabatan
4. Try different keyword
```

---

### ⚠️ Sentiment Score selalu Neutral

**Penyebab:**
- Tidak ada public posts ditemukan
- Scraping disabled
- No social media column

**Expected Behavior:**
```
Mock Mode:
- Random sentiment scores untuk testing
- Not real sentiment analysis

Transformers Mode:
- Requires actual text/posts
- If no text, defaults to neutral
```

---

## 🐌 Performance Issues

### ⏰ Analysis sangat lambat

**Penyebab:**
- Banyak kandidat (>100)
- Scraping enabled
- Network slow

**Solusi:**

**1. Batch processing:**
```
- Split file menjadi chunks 50 candidates
- Process separately
- Merge results di Excel
```

**2. Disable scraping:**
```
Sidebar → ☐ Ambil Posting Publik (Scraping)
Uncheck untuk speed up 10x
```

**3. Use Mock Mode:**
```
Sidebar → ☑ Gunakan Mock Mode
Mock mode ~3 sec/candidate vs 10-30 sec dengan Transformers
```

**Time estimates:**
```
50 candidates:
- Mock Mode: ~2-3 minutes
- Transformers: ~5-10 minutes
- With Scraping: ~15-30 minutes

100 candidates:
- Mock Mode: ~5 minutes
- Transformers: ~10-20 minutes
- With Scraping: ~30-60 minutes
```

---

### 💾 Memory errors

**Penyebab:**
- File terlalu besar
- Too many columns
- RAM limitation

**Solusi:**
```
1. Remove unnecessary columns in Excel
2. Reduce number of rows
3. Close other applications
4. Restart Streamlit
```

---

## 🤖 Model Loading Issues

### ❌ Error: "Failed to load Transformers model"

**Expected Behavior:**
- Sistem otomatis fallback ke Mock Mode
- Analisis tetap berjalan

**Jika ingin gunakan Transformers:**

**1. Check internet connection**
```powershell
# Test connection:
PS> Test-NetConnection huggingface.co -Port 443
```

**2. Manual model download:**
```powershell
PS> .\.venv\Scripts\python -c "from transformers import pipeline; pipeline('sentiment-analysis')"
```

**3. Proxy settings (jika di corporate network):**
```powershell
PS> $env:HTTP_PROXY="http://proxy:port"
PS> $env:HTTPS_PROXY="http://proxy:port"
```

**4. Use Mock Mode:**
```
Sidebar → ☑ Gunakan Mock Mode
Tidak perlu download model, langsung analisis
```

---

### ⚠️ Warning: "Using mock models"

**Bukan Error:**
- Ini informasi bahwa Mock Mode active
- Analysis tetap berjalan
- Results for testing purposes

**Jika ingin real AI:**
```
Sidebar → ☐ Gunakan Mock Mode (Testing Cepat)
Uncheck, akan download model ~500MB
```

---

## 📤 Export Problems

### ❌ Error saat download Excel

**Penyebab:**
- No results to export
- Memory issue
- Browser block

**Solusi:**

**1. Verify results:**
```
- Pastikan analisis selesai
- Lihat tabel results
- Minimal 1 candidate processed
```

**2. Browser settings:**
```
Chrome/Edge:
Settings → Downloads → Ask where to save each file
Clear download history
```

**3. Try manual export:**
```python
# Di terminal:
PS> .\.venv\Scripts\python
>>> import pandas as pd
>>> # Copy dataframe code
>>> df.to_excel('manual_export.xlsx')
```

---

## 🔄 General Troubleshooting Steps

### Step 1: Check Prerequisites
```powershell
# Verify Python version:
PS> python --version
# Should be 3.9+

# Verify venv:
PS> .\.venv\Scripts\python --version

# Verify packages:
PS> .\.venv\Scripts\pip list
# Check: streamlit, pandas, transformers, etc.
```

---

### Step 2: Restart Application
```powershell
# Kill all Streamlit processes:
PS> taskkill /F /IM streamlit.exe

# Start fresh:
PS> .\.venv\Scripts\streamlit run app.py

# Or use batch file:
PS> .\run.bat
```

---

### Step 3: Clear Cache
```powershell
# Clear Streamlit cache:
PS> Remove-Item -Recurse -Force ~/.streamlit/cache

# Or in UI:
Click "Clear Cache" in hamburger menu (☰)
```

---

### Step 4: Reinstall Dependencies
```powershell
PS> .\.venv\Scripts\pip install -r requirements.txt --force-reinstall --no-cache-dir
```

---

### Step 5: Check Logs
```powershell
# Terminal output shows:
- File reading status
- Column detection
- Candidate processing
- Errors with traceback

# Look for:
"✅" = Success
"❌" = Error
"⚠️" = Warning
"DEBUG INFO:" = Debug information
```

---

## 🆘 Emergency Fixes

### Nuclear Option: Fresh Install
```powershell
# 1. Backup data
PS> Copy-Item sample_data.csv backup/

# 2. Delete venv
PS> Remove-Item -Recurse -Force .venv

# 3. Recreate venv
PS> python -m venv .venv

# 4. Activate
PS> .\.venv\Scripts\Activate.ps1

# 5. Install dependencies
PS> pip install -r requirements.txt

# 6. Downgrade NumPy
PS> pip install "numpy<2.0" --force-reinstall

# 7. Test
PS> streamlit run app.py
```

---

### Compatibility Issues

**NumPy 2.0 Error:**
```powershell
PS> .\.venv\Scripts\pip install "numpy<2.0" --force-reinstall
```

**Pandas Arrow Error:**
```
Expected - ini adalah warning, bukan error
Sistem otomatis fix column types
Analisis tetap berjalan normal
```

**Transformers Import Error:**
```
Expected - sistem fallback ke Mock Mode
Analisis tetap berjalan
```

---

## 📞 Getting Help

### Before Asking for Help:

1. **Check this guide** - Most issues covered here
2. **Read error message carefully** - Often contains solution
3. **Check terminal output** - Shows detailed errors
4. **Try Preview feature** - Validates file structure
5. **Test with sample_data.csv** - Isolates file issues

### Information to Provide:

```
When reporting issue, include:

1. Error message (full text)
2. Terminal output (last 20 lines)
3. File structure (Preview screenshot)
4. Steps to reproduce
5. System info:
   - Windows version
   - Python version
   - Virtual env active?
   - First time or was working before?
```

### Contact:

```
- GitHub Issues: [Preferred for bugs]
- Email: support@sentivize.ai
- Documentation: Check all .md files in /docs
```

---

## ✅ Checklist untuk Success

Sebelum analisis, pastikan:

- [ ] File format correct (.csv or .xlsx)
- [ ] File tidak corrupt
- [ ] Header ada dan jelas
- [ ] Kolom nama terisi (not blank)
- [ ] Preview shows ✅ for Name column
- [ ] Virtual env activated
- [ ] Dependencies installed
- [ ] Keyword entered
- [ ] Mode selected (Mock or Transformers)
- [ ] Internet connection (jika gunakan Transformers)

---

## 🎓 Learning Resources

### Dokumentasi:
- `README.md` - Overview dan getting started
- `QUICK_START.md` - Step-by-step tutorial
- `INSTALL.md` - Installation guide
- `ADAPTIVE_FEATURES.md` - Advanced features
- `USER_GUIDE.md` - Complete usage guide

### Video Tutorials:
- (Coming soon)

### Examples:
- `sample_data.csv` - Working example file
- Test dengan file ini first untuk validate setup

---

**Updated: 2025-11-12**  
**Version: 2.0**
