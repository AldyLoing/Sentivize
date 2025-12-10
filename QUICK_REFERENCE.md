# 🎯 SENTIVIZE QUICK REFERENCE CARD

## 🚀 Quick Start (3 Langkah)

```bash
# 1. Setup
cp .env.example .env
pip install -r requirements.txt

# 2. Test
python test_ai_system.py

# 3. Run
streamlit run app_ultra.py
```

---

## 📋 Fitur Utama

### 1️⃣ CV/Resume Analyzer
```
Upload CV → Preview → Input Job Desc → Analyze → View Results
```

### 2️⃣ Employee Analyzer  
```
Single: Input Job + Candidate → Analyze
Batch: Upload Excel + Input Job → Batch Analyze → Download
```

---

## 🎯 Job Complexity Rules

| Level | Jobs | Evaluation Focus | Fresh Grad? |
|-------|------|------------------|-------------|
| **LOW** | Admin, Kasir, Staff Entry | Soft skills, Attitude | ✅ FRIENDLY |
| **MID** | Supervisor, Analyst Jr | Balanced soft+hard skills | ⚠️ DEPENDS |
| **HIGH** | Engineer Sr, Manager | Hard skills, Experience | ❌ STRICT |

---

## 💡 Scoring Weights

### Low Complexity (Admin, Kasir):
- Soft Skills: **35%** ⬆️
- Attitude/Potential: **10%** ⬆️
- Hard Skills: **15%** ⬇️
- Experience: **15%** ⬇️

### High Complexity (Engineer, Manager):
- Hard Skills: **40%** ⬆️
- Experience: **30%** ⬆️
- Soft Skills: **10%** ⬇️

---

## 🧠 AI Reasoning Logic

### Fresh Graduate untuk LOW Job:
```
✅ DO:
- Focus soft skills & attitude
- Value organizational exp
- Consider projects/volunteer
- High potential score

❌ DON'T:
- Penalize "no experience"
- Strict keyword match
```

### Experienced untuk HIGH Job:
```
✅ DO:
- Strict technical evaluation
- Portfolio/projects critical
- Track record important

❌ DON'T:
- Accept without proof
- Over-weight soft skills
```

---

## 📊 Output Interpretation

### Score Tiers:
- **85-100**: EXCELLENT (Hire immediately)
- **70-84**: STRONG (Strongly recommend)
- **55-69**: MEDIUM (Consider, need interview)
- **<55**: LOW (Not suitable)

### Recommendations:
- **STRONGLY RECOMMEND**: Perfect match
- **RECOMMEND**: Good fit, minor gaps
- **CONSIDER**: Potential, need development
- **NOT SUITABLE**: Significant mismatch

---

## 🔧 Troubleshooting Cepat

| Issue | Solution |
|-------|----------|
| "API not configured" | Check `.env` file, set API key |
| "AI failed, fallback" | Check internet, system still works |
| "CV extraction error" | Try different format (PDF/DOCX) |
| "Models downloading" | First run only, wait ~10 min |

---

## 📝 Excel Format untuk Batch

Required columns:
```
name | position | skills | experience
```

Optional:
```
bio | education | social_media_url
```

Example:
```csv
name,position,skills,experience
John Doe,Staff,MS Office,2 tahun admin
Jane Smith,Fresh Grad,Python,Magang 6 bulan
```

---

## 🎓 Best Practices

### For HR/Admin:

1. **Detail Job Description**
   - Include responsibilities
   - List required skills
   - Mention nice-to-haves

2. **Trust AI Reasoning**
   - Read explanation carefully
   - Consider context not just score

3. **Entry-Level Hiring**
   - Focus on potential
   - Value attitude & learning ability
   - Don't expect full experience

### For Candidates:

1. **CV Structure**
   - Clear sections (Education, Experience, Skills)
   - Include projects & organizational exp
   - Quantify achievements

2. **Entry-Level**
   - Highlight projects & coursework
   - Emphasize soft skills
   - Show learning willingness

---

## 🔑 Key API Info

**Service**: OpenRouter  
**Model**: deepseek-chat  
**Cost**: FREE (unlimited)  
**Speed**: ~2-5 seconds per analysis  
**Privacy**: Data not stored by OpenRouter

---

## 📞 Support Quick Links

- **Full Guide**: `AI_UPGRADE_GUIDE.md`
- **Troubleshooting**: `TROUBLESHOOTING.md`
- **Testing**: `python test_ai_system.py`
- **Documentation**: `README_V3.md`

---

## 💬 Common Questions

**Q: Apakah wajib punya API key?**  
A: Untuk AI reasoning: Ya. Tapi sistem tetap jalan dengan fallback scoring.

**Q: Apakah gratis?**  
A: Yes! Model deepseek-chat free unlimited via OpenRouter.

**Q: Bahasa apa yang didukung?**  
A: Bahasa Indonesia & English. Optimal untuk Indonesia.

**Q: Bisakah offline?**  
A: Tidak untuk AI reasoning (need internet). Fallback mode bisa offline.

**Q: Data aman?**  
A: Ya. CV di-process lokal, OpenRouter tidak simpan data.

---

## 🎯 Quick Commands

```bash
# Test system
python test_ai_system.py

# Run app
streamlit run app_ultra.py

# Update dependencies
pip install -r requirements.txt --upgrade

# Check logs
streamlit run app_ultra.py --logger.level=debug
```

---

## 📈 Performance Tips

1. **First Run**: Wait for model downloads (~10 min)
2. **Batch Analysis**: Process max 50 candidates at once
3. **Large CVs**: Keep under 10MB
4. **API Limits**: deepseek-chat has no rate limit (free tier)

---

## ✅ Pre-Launch Checklist

- [ ] `.env` file configured
- [ ] Dependencies installed
- [ ] Test script passed
- [ ] Sample CV tested
- [ ] Sample job description ready
- [ ] Internet connection stable

---

**Version**: 3.0  
**Updated**: December 2024  
**Quick Help**: Read this card when you need quick answers!

---

**🚀 Now you're ready! Start analyzing!**
