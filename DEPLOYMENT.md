# 🚀 Deployment Guide - Sentivize ke Vercel

## 📋 Prasyarat

1. **Akun GitHub** - Untuk repository
2. **Akun Vercel** - Untuk hosting (gratis)
3. **OpenRouter API Key** - Sudah tersedia

## 🔧 Langkah 1: Push ke GitHub

```bash
# Inisialisasi Git (jika belum)
git init

# Add semua file
git add .

# Commit
git commit -m "Initial commit - Sentivize HR Analytics with AI"

# Add remote repository (ganti dengan repository Anda)
git remote add origin https://github.com/AldyLoing/Sentivize.git

# Push ke GitHub
git branch -M main
git push -u origin main
```

## ☁️ Langkah 2: Deploy ke Vercel

### Via Vercel Dashboard (Termudah)

1. **Buka Vercel**: https://vercel.com/
2. **Login** dengan akun GitHub
3. **Import Project**: Klik "Add New..." → "Project"
4. **Pilih Repository**: Cari dan pilih repository "Sentivize"
5. **Configure Project**:
   - Framework Preset: **Other**
   - Build Command: (kosongkan)
   - Output Directory: (kosongkan)
   - Install Command: `pip install -r requirements.txt`

6. **Environment Variables** - Klik "Environment Variables":
   ```
   Key: OPENROUTER_API_KEY
   Value: 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
   ```

7. **Deploy**: Klik "Deploy"

### Via Vercel CLI (Alternatif)

```bash
# Install Vercel CLI
npm i -g vercel

# Login ke Vercel
vercel login

# Deploy
vercel

# Ikuti prompt:
# - Set up and deploy? Y
# - Which scope? Pilih account Anda
# - Link to existing project? N
# - Project name? sentivize
# - Directory? ./
# - Override settings? N

# Set environment variable
vercel env add OPENROUTER_API_KEY
# Paste API key: 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

# Deploy production
vercel --prod
```

## 🎯 Langkah 3: Verifikasi Deployment

Setelah deploy berhasil, Vercel akan memberikan URL seperti:
- **Production**: `https://sentivize.vercel.app`
- **Preview**: `https://sentivize-git-main-aldyloing.vercel.app`

### Test Aplikasi:
1. Buka URL production
2. Test **CV Analyzer**: Upload file CV PDF/DOCX
3. Test **Employee Analyzer**: Upload file Excel/CSV
4. Pastikan AI analysis berjalan (cek Preview dan Full Analysis)

## ⚠️ Troubleshooting

### Error: "Module not found"
- Pastikan semua dependencies ada di `requirements.txt`
- Rebuild: `vercel --prod --force`

### Error: "API Key not found"
- Cek environment variable di Vercel Dashboard
- Settings → Environment Variables → Add/Edit

### Error: "File too large"
- Vercel free tier limit: 50MB per function
- File upload limit sudah diatur di config.py

### Error: "Timeout"
- Vercel serverless function timeout: 10s (free), 60s (pro)
- AI processing mungkin perlu optimasi untuk file besar

## 🔄 Update Deployment

Setiap push ke GitHub akan otomatis trigger deployment baru:

```bash
# Make changes
git add .
git commit -m "Update fitur X"
git push origin main
```

Vercel akan otomatis:
1. Detect push baru
2. Build aplikasi
3. Deploy ke production (jika di branch main)

## 📊 Monitoring

- **Dashboard Vercel**: https://vercel.com/dashboard
- **Analytics**: Lihat traffic, performance, errors
- **Logs**: Real-time logs untuk debugging

## 💡 Tips Deployment

1. **Environment Variables**: Jangan commit `.env` ke GitHub (sudah di `.gitignore`)
2. **Model Cache**: Transformer models akan di-download saat pertama kali run di Vercel
3. **Cold Start**: First request mungkin lambat (5-10 detik) karena loading models
4. **Free Tier Limits**:
   - 100GB bandwidth/month
   - 100 hours serverless function execution
   - Cukup untuk testing dan small-scale usage

## 🎉 Selesai!

Aplikasi Sentivize sekarang live di internet dan bisa diakses dari mana saja!

**Next Steps:**
- Share URL ke tim HR/Admin
- Monitor usage via Vercel Dashboard
- Collect feedback untuk improvement

---

**Support**: Jika ada masalah, check logs di Vercel Dashboard atau GitHub Issues.
