# 🎉 CV/Resume Analyzer - Quick Start Guide

## ✅ Installation Complete!

Fitur CV/Resume Analyzer telah berhasil diintegrasikan ke dalam aplikasi Sentivize!

### 📦 Dependencies Installed
- ✅ **PyPDF2 3.0.1** - untuk ekstraksi PDF
- ✅ **python-docx 1.1.0** - untuk ekstraksi DOCX
- ✅ **All core modules** - cv_analyzer.py, cv_analyzer_page.py

### 📁 Files Created/Modified

**New Files:**
1. **cv_analyzer.py** (400+ lines)
   - CVAnalyzer class dengan full functionality
   - PDF, DOCX, TXT extraction
   - Section parsing (nama, email, phone, education, experience, skills)
   - AI-powered analysis
   - Batch processing support

2. **cv_analyzer_page.py** (350+ lines)
   - Complete UI page
   - Multi-file uploader
   - Criteria input with examples
   - Detail display dengan expandable cards per CV
   - Visualizations
   - Excel export

3. **CV_ANALYZER.md** (1000+ lines)
   - Complete documentation
   - Usage guide
   - Best practices
   - Troubleshooting
   - Examples

**Modified Files:**
1. **app.py**
   - Added navigation sidebar
   - Route ke CV Analyzer page
   - Fixed syntax errors ✅

2. **requirements.txt**
   - Added PyPDF2==3.0.1
   - Added python-docx==1.1.0

3. **README.md**
   - Updated dengan CV Analyzer features
   - Link to full documentation

---

## 🚀 How to Use

### 1. Start the Application

```powershell
cd e:\Orders\Project\Sentivize
.\.venv\Scripts\streamlit run app.py
```

### 2. Navigate to CV Analyzer

Aplikasi akan terbuka di browser. Di **sidebar kiri**, Anda akan melihat 2 opsi:
- 👥 **Analisis Karyawan** (existing feature)
- 📄 **CV/Resume Analyzer** (NEW!)

Klik pada **"📄 CV/Resume Analyzer"**

### 3. Upload CV Files

- Klik area "**Pilih file CV/Resume (PDF, DOCX, TXT)**"
- Pilih satu atau lebih file CV
- Format yang didukung: `.pdf`, `.docx`, `.txt`

### 4. Enter Criteria

Masukkan kriteria pencarian, contoh:

**Kata Kunci:**
```
Python, machine learning, SQL, communication skills
```

**Frase:**
```
project management, team leadership, data analysis
```

**Kalimat:**
```
pengalaman minimal 3 tahun dalam pengembangan software menggunakan Python dan framework Django
```

### 5. Analyze

Klik tombol **"🔍 Analisis CV"** dan tunggu proses selesai.

### 6. Review Results

Anda akan mendapatkan:
- **Hasil Analisis CV** dengan expandable cards (urutan berdasarkan skor tertinggi)
- **AI Reasoning** detail per CV
- **Section Scores** (Contact, Education, Experience, Skills)
- **Visualizations** (score distribution, sentiment)
- **Tabel Lengkap** dengan filter
- **Excel Export** untuk download

---

## 💡 Quick Tips

1. **Format CV**
   - Gunakan CV dengan format sederhana (tidak terlalu complex layout)
   - Text-based PDF (bukan scanned)
   - Struktur yang jelas (heading untuk Education, Experience, Skills)

2. **Criteria**
   - Semakin spesifik, semakin baik
   - Kombinasikan technical skills dan soft skills
   - Gunakan koma (,) untuk multiple criteria

3. **Batch Size**
   - Bisa upload beberapa CV sekaligus
   - Sistem akan urutkan berdasarkan skor tertinggi

4. **Review**
   - Selalu baca **AI Reasoning** untuk context
   - Focus pada CV dengan skor tertinggi
   - Download Excel untuk review lebih lanjut

---

## 📊 Sample Test Data

Untuk testing, Anda bisa create sample CV atau gunakan CV template. Contoh criteria untuk testing:

### Software Engineer
```
Bachelor degree in Computer Science, 3+ years Python experience, 
REST API development, PostgreSQL, Git, agile methodology
```

### Data Analyst
```
analytical skills, Excel, SQL, Python or R, 
data visualization, Tableau or Power BI, statistical analysis
```

### Marketing Manager
```
5+ years marketing experience, digital marketing, SEO, 
social media management, team leadership, budget management
```

---

## 🔧 Troubleshooting

### Issue: "Module not found: PyPDF2"
**Solution:**
```powershell
.\.venv\Scripts\pip install PyPDF2==3.0.1 python-docx==1.1.0
```

### Issue: "File tidak bisa dibaca"
**Solution:**
- Pastikan file adalah text-based PDF (bukan scan)
- Cek file tidak corrupt atau password-protected
- Try convert ke TXT atau DOCX format

### Issue: "No module named 'cv_analyzer'"
**Solution:**
- Pastikan file `cv_analyzer.py` ada di root directory
- Restart Streamlit app

### Issue: "No module named 'cv_analyzer_page'"
**Solution:**
- Pastikan file `cv_analyzer_page.py` ada di root directory
- Restart Streamlit app

---

## 📚 Full Documentation

Untuk dokumentasi lengkap, lihat **[CV_ANALYZER.md](CV_ANALYZER.md)**

Topics covered:
- ✅ Detailed features explanation
- ✅ Complete usage guide dengan screenshots
- ✅ Best practices & tips
- ✅ Technical architecture
- ✅ Scoring algorithms
- ✅ Troubleshooting guide
- ✅ Use cases & examples
- ✅ Limitations & disclaimer

---

## ✨ Features Summary

### What This Module Can Do:

✅ **Multi-Format Support**: PDF, DOCX, TXT
✅ **Batch Processing**: Upload multiple CVs at once
✅ **Smart Extraction**: Auto-extract key information
✅ **Flexible Criteria**: Keywords, phrases, or sentences
✅ **Semantic Matching**: Understand meaning, not just exact match
✅ **AI Analysis**: Relevance + sentiment scoring
✅ **Detailed Reasoning**: Explanation per CV
✅ **Section Scoring**: Score per section (Contact, Education, etc.)
✅ **Detail Display**: Expandable cards untuk setiap CV
✅ **Visualizations**: Charts for score distribution
✅ **Excel Export**: Download full results
✅ **Filter & Search**: Interactive table dengan filter

### What Makes It Different:

🌟 **Semantic Understanding**: Tidak hanya exact keyword match
🌟 **Context-Aware**: Memahami context dari matches
🌟 **AI Reasoning**: Penjelasan detail kenapa match/tidak match
🌟 **Section-Based**: Analisis terpisah per section CV
🌟 **Batch Efficient**: Process banyak CV sekaligus
🌟 **Flexible Input**: Support berbagai format criteria
🌟 **User-Friendly**: Simple UI, clear results

---

## 🎯 Next Steps

1. **Test Basic Functionality**
   - Upload 1-2 sample CVs
   - Test dengan simple criteria
   - Verify extraction works

2. **Test Batch Processing**
   - Upload beberapa CVs
   - Check performance
   - Review hasil dengan skor tertinggi

3. **Test Different Formats**
   - Try PDF files
   - Try DOCX files
   - Try TXT files

4. **Test Complex Criteria**
   - Try sentence-based criteria
   - Try multiple keywords
   - Check semantic matching

5. **Export & Review**
   - Download Excel
   - Check data completeness
   - Verify reasoning quality

---

## 🆘 Need Help?

1. **Read Documentation**: [CV_ANALYZER.md](CV_ANALYZER.md)
2. **Check Troubleshooting**: See section above
3. **Review Code**: Check `cv_analyzer.py` and `cv_analyzer_page.py`
4. **Test with Samples**: Use simple test cases first

---

## ✅ System Ready!

Your CV/Resume Analyzer is ready to use! 🎉

**Start the app and navigate to "📄 CV/Resume Analyzer" in the sidebar.**

Happy analyzing! 🚀
