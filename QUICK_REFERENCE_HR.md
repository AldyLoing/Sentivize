# 🚀 QUICK REFERENCE - Sentivize AI Analyzer

**Panduan Cepat untuk HR Team** 👥

---

## 🎯 Akses Aplikasi

**URL**: http://localhost:8502

**Browser**: Chrome, Firefox, Safari, atau Edge

**Login**: Tidak perlu login (local application)

---

## 📋 Menu Utama

### 🏠 Home
- Overview sistem
- Panduan singkat

### 🔍 Advanced Employee Analyzer
- **Untuk**: Analisis karyawan existing
- **Input**: CSV file dengan data karyawan
- **Output**: Scoring & recommendations

### 📄 Advanced CV Analyzer
- **Untuk**: Screening kandidat baru
- **Input**: Multiple CV files (PDF/DOCX)
- **Output**: Ranking & hiring decision

---

## 💼 Employee Analysis - Step by Step

### 1️⃣ Upload Data
- Klik "**Browse files**"
- Pilih CSV file karyawan
- File harus punya kolom: `name`, `feedback`, `performance`, dll

### 2️⃣ Run Analysis
- Klik tombol "**🚀 Analyze Employees**"
- Tunggu 10-30 detik (tergantung jumlah data)
- Loading indicator akan muncul

### 3️⃣ Baca Hasil
Setiap karyawan ditampilkan dalam format:

```
🌟 John Doe | Kecocokan: 85%

[3 Metric Cards]

💡 Ringkasan
- Overview singkat karyawan

✅ Kekuatan
- Apa yang baik
- Poin-poin positif

⚠️ Perlu Ditingkatkan
- Area concern
- Yang perlu perhatian

🎯 Rekomendasi
- Action items
- Next steps
```

### 4️⃣ Interpretasi Skor

| Emoji | Score | Meaning | Action |
|-------|-------|---------|--------|
| 🌟 | 80-100% | Sangat Cocok | Pertahankan & kembangkan |
| ✅ | 60-79% | Cocok | Monitor progress |
| 💡 | 40-59% | Cukup Potensial | Development plan |
| ⚠️ | <40% | Perlu Perhatian | Immediate intervention |

---

## 📄 CV Analysis - Step by Step

### 1️⃣ Upload CVs
- Klik "**Browse files**"
- Pilih multiple CVs (bisa lebih dari 1)
- Format: PDF, DOCX, atau TXT
- Max size: 10MB per file

### 2️⃣ Input Kriteria
- Tulis job requirements di text box
- Contoh:
  ```
  Posisi: Senior Software Engineer
  Skills: Python, React, AWS
  Experience: 5+ years
  Education: Bachelor degree or higher
  ```

### 3️⃣ Run Analysis
- Klik tombol "**🎯 Analyze CVs**"
- Tunggu 20-60 detik (tergantung jumlah CV)
- System akan processing semua CV

### 4️⃣ Review Ranking
CVs otomatis di-rank dari tertinggi ke terendah:

```
🌟 1. Jane Smith | Kecocokan: 88%
✅ 2. Bob Wilson | Kecocokan: 76%
💡 3. Alice Chen | Kecocokan: 62%
⚠️ 4. Tom Brown | Kecocokan: 45%
```

### 5️⃣ Interpretasi Keputusan

| Emoji | Score | Decision | Action |
|-------|-------|----------|--------|
| 🌟 | 80-100% | **Strong Hire** | 📞 Contact ASAP, interview segera |
| ✅ | 65-79% | **Hire** | 📋 Schedule interview |
| 💡 | 50-64% | **Consider** | 🔍 Deep dive interview |
| ⚠️ | <50% | **Pass** | 📁 Keep in database for future |

---

## 📊 Export Data

### Excel Export
- Klik "**📥 Download Excel Report**"
- File berisi semua data + scoring
- Bisa dibuka di Microsoft Excel

### JSON Export
- Klik "**💾 Export JSON**"
- File untuk technical team
- Bisa diproses lebih lanjut

---

## 🎨 Understanding Display

### Metric Cards
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│     🌟      │  │     💼      │  │     💯      │
│     85%     │  │   7 years   │  │     88%     │
│ Kesesuaian  │  │ Pengalaman  │  │ Confidence  │
└─────────────┘  └─────────────┘  └─────────────┘
```

### Color Boxes
- 🟢 **Hijau**: Positive decision (Hire/Strong Hire)
- 🟡 **Kuning**: Neutral decision (Consider)
- 🔴 **Merah**: Negative decision (Pass)

### Expand/Collapse
- **Top 3**: Otomatis terbuka
- **Others**: Klik untuk expand
- **Detail Teknis**: Tersembunyi, klik "📊 Lihat Detail Teknis"

---

## 💡 Pro Tips

### Employee Analysis:
✅ **Upload complete data** untuk hasil akurat
✅ **Check feedback quality** - feedback yang detail = analisis lebih baik
✅ **Review top & bottom performers** untuk prioritas action
✅ **Export regularly** untuk tracking over time

### CV Analysis:
✅ **Use clear criteria** - spesifik = hasil lebih akurat
✅ **Upload batch** - lebih efisien daripada satu-satu
✅ **Focus on top 5-10** candidates untuk interview
✅ **Read full profile** untuk final decision
✅ **Check contact info** sebelum menghubungi

---

## ⚠️ Common Mistakes to Avoid

### ❌ DON'T:
- Upload CVs tanpa criteria yang jelas
- Hanya lihat score tanpa baca recommendations
- Ignore warning signs (⚠️)
- Make decision hanya based on score
- Skip reading "Perlu Ditingkatkan" section

### ✅ DO:
- Input detailed job criteria
- Read full analysis, especially recommendations
- Consider both strengths & weaknesses
- Use score as guidance, not absolute rule
- Combine AI insights dengan human judgment

---

## 🆘 Quick Troubleshooting

### Problem: Upload Error
**Solution**: 
- Check file format (CSV for employees, PDF/DOCX for CVs)
- Verify file size (<10MB)
- Ensure file not corrupted

### Problem: Analysis Stuck
**Solution**:
- Wait 1-2 minutes (large files take time)
- Check internet connection
- Refresh browser (Ctrl+F5)

### Problem: Weird Results
**Solution**:
- Verify input data quality
- Check criteria clarity
- Re-run analysis
- Contact admin if persists

### Problem: Can't Export
**Solution**:
- Check browser allows downloads
- Try different browser
- Clear browser cache

---

## 📞 Need Help?

### Quick Help:
1. Klik "❓ Help" di sidebar
2. Hover mouse di field untuk tooltip
3. Check dokumentasi lengkap

### Contact:
- **Technical Issue**: IT Support team
- **How-to Questions**: HR Manager
- **Feature Requests**: Project Manager

---

## 🎓 Learning Resources

### Documents:
- `USER_FRIENDLY_UPDATE.md` - Detailed UI guide
- `USAGE_EXAMPLES.md` - Example scenarios
- `QUICK_START.md` - Complete tutorial

### Training:
- Request demo dari IT team
- Weekly HR workshop
- One-on-one training tersedia

---

## ✅ Daily Workflow

### Morning Routine:
1. Open application
2. Check overnight CV submissions
3. Run batch analysis
4. Review top candidates
5. Schedule interviews

### Weekly Review:
1. Export employee data
2. Compare week-over-week trends
3. Identify top/bottom performers
4. Plan interventions
5. Update management reports

---

## 🎯 Success Metrics

Track your usage:
- **CVs processed per week**
- **Time saved vs manual screening**
- **Hiring decision accuracy**
- **Employee retention correlation**

---

## 🌟 Best Practices

### For Maximum Value:
1. ✅ **Use consistently** - regular usage = better insights
2. ✅ **Trust the AI** - but verify with interviews
3. ✅ **Document decisions** - use export functions
4. ✅ **Share insights** - collaborate with team
5. ✅ **Provide feedback** - help improve system

---

## 🚀 Quick Start Checklist

- [ ] Bookmark http://localhost:8502
- [ ] Prepare employee CSV template
- [ ] Gather sample CVs for testing
- [ ] Read this quick reference
- [ ] Run first test analysis
- [ ] Export sample reports
- [ ] Share with team
- [ ] Start using daily!

---

## 📈 ROI Indicators

**Time Saved**:
- Manual CV screening: ~15 min per CV
- AI screening: ~2 sec per CV
- **Savings**: ~98% time reduction

**Quality Improved**:
- Consistent scoring criteria
- Reduced bias
- Better candidate matches
- Data-driven decisions

---

**🎉 You're ready to use Sentivize AI Analyzer!**

**Remember**: AI is a tool to **augment** your expertise, not replace it. Use the insights wisely! 🧠

---

_Quick Reference v2.0_
_Last Updated: 2024_
_For HR Team Use_

---

**💡 Tip of the Day**: Top 3 candidates auto-expand - start your review from there for quick wins! 🏆
