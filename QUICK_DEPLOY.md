# 🚀 Quick Deploy Guide

## ✅ Yang Sudah Selesai

1. ✅ File konfigurasi Vercel (`vercel.json`)
2. ✅ Streamlit config (`.streamlit/config.toml`)
3. ✅ `.vercelignore` untuk exclude file besar
4. ✅ `.gitignore` updated
5. ✅ GitHub Actions workflow (`.github/workflows/vercel-deploy.yml`)
6. ✅ LICENSE file (MIT)
7. ✅ Git repository initialized dan committed

## 📋 Langkah Selanjutnya

### 1️⃣ Buat Repository di GitHub

1. Buka https://github.com/new
2. **Repository name**: `Sentivize` (atau nama lain)
3. **Description**: `AI-Powered HR Analytics Platform with OpenRouter`
4. **Visibility**: Public atau Private (terserah Anda)
5. ❌ **JANGAN** centang "Initialize with README" (sudah ada)
6. Klik **"Create repository"**

### 2️⃣ Push ke GitHub

Setelah repository dibuat, jalankan command berikut di terminal:

```bash
# Ganti URL dengan repository Anda
git remote add origin https://github.com/AldyLoing/Sentivize.git

# Push ke GitHub
git branch -M main
git push -u origin main
```

**Jika sudah ada remote origin:**
```bash
git remote set-url origin https://github.com/AldyLoing/Sentivize.git
git push -u origin main
```

### 3️⃣ Deploy ke Vercel (Web UI - Termudah)

1. **Buka Vercel**: https://vercel.com/signup
2. **Login dengan GitHub**: Klik "Continue with GitHub"
3. **Import Project**:
   - Klik tombol **"Add New..."** → **"Project"**
   - Pilih **"Import Git Repository"**
   - Cari repository **"Sentivize"**
   - Klik **"Import"**

4. **Configure Project**:
   - **Project Name**: `sentivize` (atau custom)
   - **Framework Preset**: `Other`
   - **Root Directory**: `./` (default)
   - **Build Command**: Kosongkan atau `pip install -r requirements.txt`
   - **Output Directory**: Kosongkan
   - **Install Command**: `pip install -r requirements.txt`

5. **Environment Variables** (PENTING!):
   Klik **"Environment Variables"** dan tambahkan:
   ```
   Key: OPENROUTER_API_KEY
   Value: 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
   Environment: Production, Preview, Development (centang semua)
   ```

6. **Deploy**: Klik **"Deploy"**

7. **Tunggu**: Build process sekitar 2-5 menit

8. **Selesai!** Anda akan mendapat URL seperti:
   - `https://sentivize.vercel.app`
   - `https://sentivize-git-main-aldyloing.vercel.app`

### 4️⃣ Verifikasi Deployment

Setelah deploy berhasil:

1. **Buka URL** yang diberikan Vercel
2. **Test CV Analyzer**: Upload file CV PDF/DOCX
3. **Test Employee Analyzer**: Upload file Excel/CSV
4. **Pastikan AI berjalan**: Cek Preview dan Full Analysis

### 5️⃣ Deploy via Vercel CLI (Alternatif)

Jika lebih suka command line:

```bash
# Install Vercel CLI globally
npm install -g vercel

# Login ke Vercel
vercel login

# Deploy ke production
vercel --prod

# Set environment variable (saat prompt)
# OPENROUTER_API_KEY=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
```

## 🔄 Update Deployment

Setiap kali Anda push ke GitHub, Vercel akan otomatis build dan deploy:

```bash
# Make changes to your code
git add .
git commit -m "Update: fitur baru X"
git push origin main
```

Vercel akan otomatis:
- Detect push baru
- Build aplikasi
- Deploy ke production (untuk branch `main`)
- Deploy ke preview URL (untuk branch lain atau PR)

## 📊 Monitor Deployment

Dashboard Vercel: https://vercel.com/dashboard
- ✅ Deployment status
- 📈 Analytics & Usage
- 🐛 Real-time logs
- ⚠️ Error tracking

## ⚠️ Troubleshooting

### Error: "Module not found"
```bash
# Pastikan requirements.txt lengkap
# Rebuild:
vercel --prod --force
```

### Error: "Environment variable not set"
1. Buka Vercel Dashboard
2. Pilih project → Settings → Environment Variables
3. Add `OPENROUTER_API_KEY`
4. Redeploy

### Error: "Function timeout"
- Vercel free tier: 10 detik timeout
- Vercel Pro: 60 detik timeout
- Solution: Optimize AI processing atau upgrade plan

### Cold Start Lambat
- First request akan lambat (5-10 detik)
- Model loading di serverless environment
- Normal behavior untuk free tier

## 💡 Tips

1. **Environment Variable**: Jangan commit `.env` ke GitHub!
2. **Model Cache**: Models akan di-download pertama kali run
3. **Git Large Files**: Model cache di-exclude via `.gitignore`
4. **Free Tier Limits**:
   - 100GB bandwidth/month
   - 100 hours function execution
   - Unlimited deployments

## 🎉 Done!

Aplikasi Sentivize sekarang:
- ✅ Di-version dengan Git
- ✅ Hosted di GitHub
- ✅ Live di Vercel
- ✅ Otomatis deploy saat push
- ✅ Monitoring & logs tersedia

**Next:** Share URL ke tim atau client untuk testing!

---

## 📞 Need Help?

- 📖 Detailed guide: [DEPLOYMENT.md](DEPLOYMENT.md)
- 🐛 Issues: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- 💬 Questions: Open GitHub issue

**Happy Deploying! 🚀**
