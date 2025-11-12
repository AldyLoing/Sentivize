# 🚀 Quick Start Guide - Sentivize

Panduan cepat untuk mulai menggunakan aplikasi dalam 5 menit!

## ⚡ Install & Run (Fast Track)

### Windows PowerShell:

```powershell
# 1. Masuk ke folder project
cd e:\Orders\Project\Sentivize

# 2. (Opsional) Buat virtual environment
python -m venv venv
.\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Jalankan aplikasi
streamlit run app.py
```

Atau double-click: **`run.bat`**

## 🎯 First Time Use

### Step 1: Buka Aplikasi
Browser akan otomatis membuka `http://localhost:8501`

### Step 2: Test dengan Mock Mode
1. Di **Sidebar**, centang ✅ **"Gunakan Mock Mode (Testing Cepat)"**
2. Biarkan scraping **tidak dicentang** (lebih cepat)

### Step 3: Upload Sample Data
1. Klik **"Browse files"**
2. Pilih file **`sample_data.csv`** (sudah disediakan)
3. Lihat preview data muncul ✅

### Step 4: Masukkan Keyword
Ketik: **`lingkungan`**

### Step 5: Analisis
1. Klik **"🚀 Mulai Analisis"**
2. Tunggu ~30 detik
3. Lihat hasil! 🎉

## 📊 Memahami Hasil

### Tabel Hasil
- **Name**: Nama kandidat
- **Sentiment Label**: POSITIVE/NEGATIVE/NEUTRAL
- **Sentiment Score**: 0-1 (lebih tinggi = lebih positif)
- **Relevance Score**: 0-1 (lebih tinggi = lebih relevan dengan keyword)

### Visualisasi
- **Bar Chart**: Top 10 kandidat paling relevan
- **Pie Chart**: Distribusi sentiment
- **Scatter Plot**: Korelasi relevance vs sentiment

### Download
Klik **"📥 Download Excel"** untuk hasil lengkap

## 🔄 Test dengan Data Sendiri

### Format File yang Didukung:
- ✅ CSV (`.csv`)
- ✅ Excel (`.xlsx`, `.xls`)
- ✅ JSON (`.json`)

### Kolom yang Diperlukan:

**Minimal** (wajib):
```
Nama,Jabatan,Unit
John Doe,Manager,IT
Jane Smith,Analyst,Finance
```

**Lengkap** (opsional tambahan):
```
Nama,Jabatan,Unit,Social Media,Bio
John Doe,Manager,IT,https://linkedin.com/in/john,"Experienced manager..."
```

### Kolom yang Dikenali:
- **Nama**: nama, name, nama_lengkap, full_name
- **Jabatan**: jabatan, position, posisi, role, title
- **Unit**: unit, department, departemen, divisi, division
- **Social Media**: social, sosial, instagram, linkedin, twitter, link
- **Bio/Teks**: bio, description, deskripsi, keterangan, about

## 🎛️ Mode Aplikasi

### Mock Mode (Recommended untuk Testing)
- ⚡ Cepat (~30 detik untuk 10 kandidat)
- 💾 Tidak perlu download model (hemat space)
- 🎯 Akurasi: Good (70-80%)
- ✅ **Use this first!**

### Transformers Mode (Production)
- 🐢 Lambat (~2-3 menit untuk 10 kandidat)
- 💾 Perlu download model (~900MB) sekali
- 🎯 Akurasi: Excellent (85-95%)
- ⚡ Perlu GPU untuk speed optimal

## ⚠️ Common Issues & Quick Fix

### Issue 1: "Kolom nama tidak ditemukan"
**Fix**: Pastikan ada kolom: `Nama`, `Name`, atau variannya

### Issue 2: Proses terlalu lama
**Fix**: 
- ✅ Gunakan Mock Mode
- ❌ Matikan Scraping
- 📉 Kurangi jumlah kandidat (<20)

### Issue 3: Error saat install
**Fix**: 
```powershell
# Install CPU-only torch (lebih kecil)
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

### Issue 4: Social media tidak ditemukan
**Fix**: 
- ⏰ Normal - rate limiting dari search engine
- ✅ Tambahkan kolom social media manual di file Excel
- 🔄 Coba lagi nanti

## 🧪 Quick Test (Tanpa Streamlit)

Untuk test komponen tanpa UI:

```powershell
python test_simple.py
```

Ini akan test:
- ✅ File reading
- ✅ Column detection  
- ✅ AI models (mock mode)
- ✅ Full pipeline

## 📝 Tips & Tricks

### 1. Start Small
Mulai dengan 5-10 kandidat dulu untuk testing

### 2. Use Mock Mode First
Jangan langsung pakai Transformers Mode untuk testing

### 3. Prepare Your Data
Format data dengan baik sebelum upload:
- Kolom nama wajib ada
- Hapus baris kosong
- Pastikan encoding UTF-8

### 4. Keyword Selection
Pilih keyword yang spesifik:
- ✅ "lingkungan hidup"
- ✅ "teknologi digital"  
- ❌ "baik" (terlalu umum)

### 5. Manual Review
Selalu review hasil manual - jangan 100% percaya AI

## 🎓 Next Steps

Setelah berhasil:

1. ✅ Baca **README.md** untuk dokumentasi lengkap
2. ✅ Eksplorasi fitur-fitur lain
3. ✅ Coba dengan data real (kecil dulu!)
4. ✅ Upgrade ke Transformers Mode untuk accuracy
5. ✅ Kustomisasi **config.py** sesuai kebutuhan

## 📞 Need More Help?

- 📖 Read: `INSTALL.md` untuk troubleshooting detail
- 📖 Read: `README.md` untuk fitur lengkap
- 🧪 Run: `test_simple.py` untuk diagnosis
- ⚠️ Check: Terminal output untuk error messages

## ⏱️ Expected Timeline

| Task | Mock Mode | Transformers |
|------|-----------|--------------|
| First run setup | 2 min | 15 min* |
| 10 candidates | 30 sec | 2 min |
| 50 candidates | 2 min | 10 min |
| 100 candidates | 5 min | 20 min |

*Includes model download time

## ✅ Checklist

Sebelum mulai, pastikan:

- [ ] Python 3.8+ terinstall
- [ ] Dependencies terinstall (`pip install -r requirements.txt`)
- [ ] File `sample_data.csv` tersedia
- [ ] Port 8501 tidak dipakai aplikasi lain
- [ ] Koneksi internet aktif (untuk social search)

## 🎉 Success Indicators

Aplikasi berhasil jika:
- ✅ Browser terbuka ke Streamlit UI
- ✅ File upload berhasil dengan preview
- ✅ Analisis selesai tanpa error
- ✅ Tabel hasil tampil dengan data
- ✅ Visualisasi muncul
- ✅ Excel dapat didownload

---

**Happy Analyzing! 🚀**

Ada pertanyaan? Check error message di terminal atau baca dokumentasi lengkap.
