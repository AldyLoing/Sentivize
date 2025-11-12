# 💡 Contoh Penggunaan - Sentivize

## Skenario 1: Recruitment untuk Posisi Environmental Manager

### Context
Perusahaan mencari kandidat untuk posisi Environmental Manager yang memiliki:
- Passion tentang lingkungan hidup
- Experience dalam sustainability
- Active presence di sosial media

### Steps

1. **Persiapan Data**

Buat file Excel `kandidat_env_manager.xlsx`:
```
Nama                 | Email                      | LinkedIn
---------------------|----------------------------|--------------------------
Budi Santoso        | budi@email.com             | https://linkedin.com/in/budisantoso
Ahmad Rizki         | ahmad@email.com            | 
Dewi Lestari        | dewi@email.com             | https://linkedin.com/in/dewilestari
Maya Putri          | maya@email.com             | https://linkedin.com/in/mayaputri
Linda Wijaya        | linda@email.com            | https://linkedin.com/in/lindawijaya
```

2. **Jalankan Aplikasi**
```powershell
streamlit run app.py
```

3. **Konfigurasi**
- Mode: Transformers (untuk hasil terbaik)
- Scraping: ON (untuk analisis mendalam)

4. **Analisis**
- Upload: `kandidat_env_manager.xlsx`
- Keyword: `"lingkungan hidup sustainability green environment"`

5. **Hasil yang Diharapkan**
```
Top 3 Kandidat:
1. Budi Santoso     - Relevance: 0.89 | Sentiment: POSITIVE (0.92)
2. Ahmad Rizki      - Relevance: 0.76 | Sentiment: POSITIVE (0.85)
3. Maya Putri       - Relevance: 0.68 | Sentiment: NEUTRAL (0.61)
```

6. **Decision Making**
- Review top 3 candidates manual
- Check social media profile
- Schedule interview

---

## Skenario 2: Employee Engagement Survey Analysis

### Context
Survey internal tentang "digital transformation" - ingin tahu sentiment karyawan

### Steps

1. **Data dari Survey**

Export dari Google Forms/SurveyMonkey ke CSV:
```csv
Nama,Departemen,Feedback
John Doe,IT,"Digital transformation sangat penting untuk perusahaan kita"
Jane Smith,Finance,"Saya khawatir dengan perubahan teknologi yang terlalu cepat"
Bob Wilson,HR,"Excited about new digital tools and automation"
```

2. **Quick Analysis dengan Mock Mode**
```powershell
# Fast testing
streamlit run app.py
# Centang "Mock Mode"
```

3. **Settings**
- Upload: `survey_digital_transformation.csv`
- Keyword: `"digital transformation technology change"`
- Scraping: OFF (tidak perlu untuk internal survey)

4. **Interpretasi Hasil**

```
Sentiment Distribution:
- POSITIVE: 65% (65 employees)
- NEUTRAL: 25% (25 employees)  
- NEGATIVE: 10% (10 employees)

Average Relevance: 0.72
Average Sentiment: 0.71
```

**Insights**:
- Mayoritas karyawan positif tentang digital transformation
- 10% perlu attention & support
- Relevance score tinggi = feedback on-topic

5. **Action Items**
- Address concerns dari negative sentiment group
- Share success stories dari positive group
- Training program untuk neutral group

---

## Skenario 3: Brand Ambassador Selection

### Context
Mencari karyawan untuk jadi brand ambassador dengan tema "innovation"

### Steps

1. **Data Source**
HR database export:
```csv
Nama,Jabatan,Instagram,Twitter,LinkedIn
Alice Chen,Product Manager,@alicechen,@alice_chen,linkedin.com/in/alicechen
Bob Kumar,Engineer,,@bobkumar,linkedin.com/in/bobkumar
Carol Lee,Designer,@carolee,,linkedin.com/in/carollee
```

2. **Configuration**
- Mode: Transformers (accuracy matters)
- Scraping: ON (perlu lihat content mereka)
- Keyword: `"innovation creative technology future"`

3. **Additional Criteria**
Filter di hasil:
- Relevance Score > 0.7
- Sentiment: POSITIVE
- Social Media Count > 2 (active di multiple platforms)

4. **Top Candidates**
```
1. Alice Chen
   - Relevance: 0.91
   - Sentiment: POSITIVE (0.95)
   - Platforms: 3 (IG, Twitter, LinkedIn)
   - Preview: "Always excited about new tech innovations..."
   
2. Carol Lee
   - Relevance: 0.84
   - Sentiment: POSITIVE (0.88)
   - Platforms: 2 (IG, LinkedIn)
   - Preview: "Creative solutions for tomorrow's challenges..."
```

5. **Validation**
- Manual review their social media posts
- Check followers count
- Review post engagement
- Interview finalists

---

## Skenario 4: Department Culture Assessment

### Context
IT Department wants to assess team alignment dengan company values: "collaboration"

### Steps

1. **Collect Data**
```csv
Nama,Role,Bio/Description
John,Senior Dev,"Team player, love pair programming and code reviews"
Jane,Junior Dev,"Learning fast, sometimes prefer working independently"
Bob,Tech Lead,"Building collaborative culture, mentor to junior devs"
```

2. **Batch Analysis**
```powershell
# Multiple keywords untuk comprehensive view
```

Settings:
- Keyword 1: "collaboration teamwork"
- Keyword 2: "independent solo"

Run dua kali dengan keyword berbeda, compare results.

3. **Results Comparison**

**Keyword: "collaboration"**
```
Average Relevance: 0.68
Top: Bob (0.89), John (0.72), Jane (0.43)
```

**Keyword: "independent"**
```
Average Relevance: 0.45
Top: Jane (0.71), John (0.38), Bob (0.26)
```

4. **Insights**
- Bob & John: High collaboration alignment ✅
- Jane: Prefer independence - perlu mentoring untuk teamwork

5. **Actions**
- Pair Jane dengan Bob (mentor)
- Team building activities
- Regular collaboration training

---

## Skenario 5: Quick Testing dengan Sample Data

### For Developers/Testers

1. **Quick Test**
```powershell
cd e:\Orders\Project\Sentivize
python test_simple.py
```

Output:
```
✅ File reading: OK
✅ Column detection: OK
✅ AI models (mock): OK
✅ Full pipeline: OK
Test passed: 4/4
```

2. **Streamlit Test**
```powershell
streamlit run app.py
```

Steps:
- Upload: `sample_data.csv` (provided)
- Keyword: `"lingkungan"`
- Mode: Mock
- Click: "Mulai Analisis"

Expected: ~30 seconds, 10 results, visualizations

3. **Verify Output**
- ✅ Tabel hasil muncul
- ✅ Charts rendered
- ✅ Excel download works
- ✅ No errors in terminal

---

## Tips untuk Berbagai Use Cases

### Use Case: Recruitment
```python
# Settings recommendation
mode = "transformers"  # Accuracy matters
scraping = True       # Need social media content
keyword = "specific job requirements"
filter = relevance_score > 0.7
```

### Use Case: Internal Survey
```python
# Settings recommendation
mode = "mock"         # Speed matters, large dataset
scraping = False      # No social media needed
keyword = "survey topic"
focus = sentiment_distribution
```

### Use Case: Brand Ambassador
```python
# Settings recommendation
mode = "transformers"
scraping = True
keyword = "brand values + industry"
filter = (relevance > 0.7) & (sentiment == "POSITIVE") & (social_count > 2)
```

### Use Case: Research/Analysis
```python
# Settings recommendation
mode = "transformers"
scraping = True
keyword = "research topic"
output = full_excel_with_text_preview
```

---

## Advanced: Programmatic Usage

Untuk automation, gunakan modules langsung tanpa Streamlit:

```python
import pandas as pd
from analyzer import analyze_candidates, save_results_to_excel

# Load data
df = pd.read_csv('kandidat.csv')

# Run analysis
results_df = analyze_candidates(
    df=df,
    keyword="lingkungan",
    enable_scraping=False,
    use_mock_models=True
)

# Save results
save_results_to_excel(results_df, 'hasil.xlsx')

# Get top 5
top_5 = results_df.nlargest(5, 'Relevance Score')
print(top_5[['Name', 'Relevance Score', 'Sentiment Label']])
```

---

## Integration Examples

### 1. dengan Pandas workflow
```python
import pandas as pd
from analyzer import analyze_candidates

# Read from multiple sources
df1 = pd.read_csv('source1.csv')
df2 = pd.read_excel('source2.xlsx')

# Combine
df = pd.concat([df1, df2])

# Normalize
df.columns = df.columns.str.lower()

# Analyze
results = analyze_candidates(df, keyword="tech")

# Further processing
filtered = results[results['Relevance Score'] > 0.8]
filtered.to_excel('shortlist.xlsx')
```

### 2. dengan Database
```python
import sqlite3
import pandas as pd
from analyzer import analyze_candidates

# Load from database
conn = sqlite3.connect('hr_database.db')
df = pd.read_sql('SELECT * FROM candidates', conn)

# Analyze
results = analyze_candidates(df, keyword="leadership")

# Save back to database
results.to_sql('analysis_results', conn, if_exists='replace')
conn.close()
```

### 3. Scheduled Jobs
```python
# schedule_analysis.py
import schedule
import time
from datetime import datetime
import pandas as pd
from analyzer import analyze_candidates, save_results_to_excel

def weekly_analysis():
    df = pd.read_csv('current_candidates.csv')
    results = analyze_candidates(df, keyword="innovation")
    filename = f'results_{datetime.now():%Y%m%d}.xlsx'
    save_results_to_excel(results, filename)
    print(f"Analysis completed: {filename}")

# Run every Monday at 9 AM
schedule.every().monday.at("09:00").do(weekly_analysis)

while True:
    schedule.run_pending()
    time.sleep(3600)
```

---

## Troubleshooting Real Cases

### Case 1: "Relevance score semua rendah"
**Problem**: Semua kandidat dapat relevance < 0.3

**Solution**:
- ✅ Check keyword terlalu spesifik? Coba general
- ✅ Check bahasa - use Bahasa Indonesia untuk IndoBERT
- ✅ Check data quality - apakah bio/text ada?

### Case 2: "Sentiment semua neutral"
**Problem**: 90% kandidat sentiment NEUTRAL

**Solution**:
- ✅ Text terlalu pendek atau formal
- ✅ Perlu scraping untuk lebih banyak data
- ✅ Try transformers mode (lebih sensitif)

### Case 3: "Social media not found"
**Problem**: 0% kandidat dengan social media found

**Solution**:
- ✅ Rate limiting - tunggu 5-10 menit
- ✅ Nama terlalu umum ("John Smith")
- ✅ Add social media column manual di Excel

---

## Best Practices Summary

1. **Start Small**: 5-10 kandidat untuk testing
2. **Use Mock First**: Validate workflow sebelum transformers
3. **Clear Keywords**: Specific, relevant keywords
4. **Data Quality**: Clean, complete data = better results
5. **Manual Review**: Always review top candidates manual
6. **Iterative**: Run multiple times dengan different keywords
7. **Documentation**: Document your criteria & process
8. **Validation**: Cross-check dengan manual assessment

---

**Selamat menggunakan Sentivize! 🚀**

Untuk pertanyaan lebih lanjut, check README.md atau INSTALL.md
