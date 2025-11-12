# 🎨 Visual Workflow Guide - Sentivize

## 📱 User Journey Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                     START: User Opens App                        │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                   Browser Opens Streamlit                        │
│              http://localhost:8501                               │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  Read Docs?    │
                    └────┬───────┬───┘
                         │       │
                    YES  │       │  NO (skip)
                         │       │
                         ▼       └─────────┐
              ┌────────────────┐           │
              │ View Disclaimer│           │
              │ & Instructions │           │
              └────────┬───────┘           │
                       │                   │
                       └───────┬───────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│              Step 1: Configure Settings (Sidebar)                │
├──────────────────────────────────────────────────────────────────┤
│  □ Mock Mode (Fast)         OR    ☑ Transformers (Accurate)     │
│  □ Enable Scraping                ☑ Disable Scraping            │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│              Step 2: Upload Data File                            │
├──────────────────────────────────────────────────────────────────┤
│  [Browse Files] → Select CSV/XLSX/JSON                          │
│                                                                   │
│  ✅ File uploaded successfully!                                  │
│  📊 Preview:                                                     │
│  ┌────────┬──────────┬──────┬──────────────┐                   │
│  │ Nama   │ Jabatan  │ Unit │ Social Media │                   │
│  ├────────┼──────────┼──────┼──────────────┤                   │
│  │ John   │ Manager  │ IT   │ linkedin...  │                   │
│  └────────┴──────────┴──────┴──────────────┘                   │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│              Step 3: Enter Keyword                               │
├──────────────────────────────────────────────────────────────────┤
│  🔑 Kata kunci: [lingkungan_____________]                       │
│  🎯 Kata kunci: lingkungan                                      │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│              Step 4: Start Analysis                              │
├──────────────────────────────────────────────────────────────────┤
│  [🚀 Mulai Analisis]  ← Click here                             │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
              ┌──────────────────────────┐
              │   Analysis Running...    │
              ├──────────────────────────┤
              │  ⏳ Progress: 45%        │
              │  ▓▓▓▓▓▓▓▓░░░░░░░         │
              │  Analyzing 45/100        │
              └──────────┬───────────────┘
                         │
                         ▼
              ┌──────────────────────────┐
              │  Analysis Complete! ✅   │
              └──────────┬───────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│              Step 5: Review Results                              │
├──────────────────────────────────────────────────────────────────┤
│  📈 Summary Stats:                                              │
│  ┌────────────────┬────────────────┬────────────────┐          │
│  │ Total: 100     │ Avg Rel: 0.65  │ Avg Sent: 0.72 │          │
│  └────────────────┴────────────────┴────────────────┘          │
│                                                                   │
│  📋 Results Table:                                              │
│  ┌──────┬──────────┬───────────┬──────────┬──────────┐        │
│  │ Name │ Position │ Sentiment │ S.Score  │ R.Score  │        │
│  ├──────┼──────────┼───────────┼──────────┼──────────┤        │
│  │ John │ Manager  │ POSITIVE  │ 0.89     │ 0.92     │        │
│  │ Jane │ Analyst  │ NEUTRAL   │ 0.61     │ 0.78     │        │
│  └──────┴──────────┴───────────┴──────────┴──────────┘        │
│                                                                   │
│  📊 Visualizations:                                             │
│  [Bar Chart] [Pie Chart] [Scatter Plot]                        │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
              ┌──────────────────────────┐
              │  Satisfied with results? │
              └────┬──────────────┬──────┘
                   │              │
              YES  │              │  NO
                   │              │
                   ▼              ▼
         ┌─────────────┐   ┌─────────────┐
         │   Download  │   │  Adjust &   │
         │    Excel    │   │  Re-analyze │
         └──────┬──────┘   └──────┬──────┘
                │                 │
                │                 └────────┐
                │                          │
                ▼                          ▼
    ┌────────────────────┐    ┌──────────────────┐
    │ 📥 Download File   │    │ Change keyword   │
    │ hasil_analisis.xlsx│    │ or settings      │
    └────────┬───────────┘    └─────────┬────────┘
             │                           │
             │                           └─────►[Back to Step 3]
             │
             ▼
┌──────────────────────────────────────────────────────────────────┐
│                        END: Mission Complete! 🎉                 │
└──────────────────────────────────────────────────────────────────┘
```

## 🔄 Processing Flow (Behind the Scenes)

```
User uploads file
      │
      ▼
┌─────────────────────────────────────────┐
│  services.read_any_file()               │
│  ├─ Parse file (CSV/XLSX/JSON)          │
│  ├─ Normalize column names              │
│  └─ Validate required columns           │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  services.detect_columns()              │
│  ├─ Find name column                    │
│  ├─ Find social media column            │
│  ├─ Find bio/text column                │
│  └─ Find position, unit columns         │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  analyzer.analyze_candidates()          │
│                                          │
│  FOR EACH CANDIDATE:                    │
└─────────────┬───────────────────────────┘
              │
              ▼
    ┌─────────────────┐
    │ Extract Info    │
    │ - Name          │
    │ - Position      │
    │ - Unit          │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────────────┐
    │ Get Social Media        │
    │ IF exists in file:      │
    │   └─ Extract links      │
    │ ELSE:                   │
    │   └─ Search web         │
    │      (DuckDuckGo/Google)│
    └────────┬────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │ Collect Texts           │
    │ - From bio column       │
    │ - From scraped posts    │
    │   (if scraping ON)      │
    │ - OR generate fallback  │
    └────────┬────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │ AI Analysis             │
    │                         │
    │ ┌─────────────────────┐ │
    │ │ Sentiment Analysis  │ │
    │ │ Input: texts[]      │ │
    │ │ ↓                   │ │
    │ │ Preprocess & clean  │ │
    │ │ ↓                   │ │
    │ │ Model inference     │ │
    │ │ (BERT/VADER)        │ │
    │ │ ↓                   │ │
    │ │ Output: (label,     │ │
    │ │         score)      │ │
    │ └─────────────────────┘ │
    │                         │
    │ ┌─────────────────────┐ │
    │ │ Relevance Analysis  │ │
    │ │ Input: texts[],     │ │
    │ │        keyword      │ │
    │ │ ↓                   │ │
    │ │ Encode texts        │ │
    │ │ Encode keyword      │ │
    │ │ ↓                   │ │
    │ │ Cosine similarity   │ │
    │ │ (Transformers/TF-   │ │
    │ │  IDF)               │ │
    │ │ ↓                   │ │
    │ │ Output: score       │ │
    │ └─────────────────────┘ │
    └────────┬────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │ Compile Result          │
    │ {                       │
    │   name: "John",         │
    │   position: "Manager",  │
    │   sentiment: POSITIVE,  │
    │   sent_score: 0.89,     │
    │   rel_score: 0.92,      │
    │   ...                   │
    │ }                       │
    └────────┬────────────────┘
             │
             └────► [Next candidate]
                    or
                    [All done]
                         │
                         ▼
              ┌──────────────────┐
              │ Aggregate Results│
              │ - To DataFrame   │
              │ - Sort by score  │
              │ - Calculate stats│
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Display to User  │
              │ - Table          │
              │ - Charts         │
              │ - Excel export   │
              └──────────────────┘
```

## 🎬 Timeline View

```
TIME ────────────────────────────────────────────────────────────►

t=0s    User opens browser
        │
        ▼
t=1s    Streamlit UI loads
        │
        ▼
t=2s    User uploads file
        │
        ▼
t=3s    File parsed & validated
        │ Preview shown
        ▼
t=5s    User enters keyword
        │
        ▼
t=6s    User clicks "Analyze"
        │
        ▼
t=7s    Models loading (if first time)
        │ (Transformers: +60s for download)
        ▼
t=10s   Analysis starts
        │
        │ ┌──────────────────┐
        │ │ Processing...    │
        │ │ Candidate 1/100  │
        │ └──────────────────┘
        ▼
t=12s   Candidate 1 done
        │
        ▼
...     Processing...
        │
        ▼
t=35s   Candidate 100 done
        │
        ▼
t=36s   Results aggregated
        │
        ▼
t=37s   UI updates with results
        │ - Summary stats
        │ - Table
        │ - Charts
        ▼
t=38s   User reviews
        │
        ▼
t=60s   User downloads Excel
        │
        ▼
t=61s   Done! 🎉
```

## 🎯 Decision Tree

```
                    Start Analysis
                         │
                         ▼
              ┌──────────────────────┐
              │ Mock Mode enabled?   │
              └─────┬──────────┬─────┘
                    │          │
               YES  │          │  NO
                    │          │
                    ▼          ▼
           ┌──────────┐  ┌──────────┐
           │  VADER   │  │  BERT    │
           │  TF-IDF  │  │  S.Trans │
           └────┬─────┘  └────┬─────┘
                │             │
                └──────┬──────┘
                       │
                       ▼
              ┌────────────────────┐
              │ Scraping enabled?  │
              └────┬─────────┬─────┘
                   │         │
              YES  │         │  NO
                   │         │
                   ▼         ▼
          ┌───────────┐  ┌──────────┐
          │Fetch posts│  │Fallback  │
          │from web   │  │text only │
          └─────┬─────┘  └────┬─────┘
                │             │
                └──────┬──────┘
                       │
                       ▼
              ┌────────────────────┐
              │ Social links exist?│
              └────┬─────────┬─────┘
                   │         │
              YES  │         │  NO
                   │         │
                   ▼         ▼
          ┌───────────┐  ┌──────────┐
          │Use from   │  │Search    │
          │file       │  │web       │
          └─────┬─────┘  └────┬─────┘
                │             │
                └──────┬──────┘
                       │
                       ▼
                   Analyze
                       │
                       ▼
                    Results
```

## 🎨 UI State Flow

```
INITIAL STATE
├─ File: None
├─ Keyword: ""
├─ Results: None
└─ Status: "Ready"

        │ User action
        ▼

FILE UPLOADED STATE
├─ File: ✅ sample_data.csv
├─ Keyword: ""
├─ Results: None
└─ Status: "File uploaded"

        │ User action
        ▼

READY TO ANALYZE STATE
├─ File: ✅ sample_data.csv
├─ Keyword: ✅ "lingkungan"
├─ Results: None
└─ Status: "Ready to analyze"

        │ User clicks button
        ▼

ANALYZING STATE
├─ File: ✅ sample_data.csv
├─ Keyword: ✅ "lingkungan"
├─ Results: None
├─ Progress: 45%
└─ Status: "Analyzing..."

        │ Process completes
        ▼

RESULTS READY STATE
├─ File: ✅ sample_data.csv
├─ Keyword: ✅ "lingkungan"
├─ Results: ✅ DataFrame(100 rows)
├─ Progress: 100%
└─ Status: "Complete"

        │ User action
        ▼

   ┌────────┴────────┐
   │                 │
   ▼                 ▼
DOWNLOAD        REANALYZE
 STATE            STATE
```

## 💡 Tips Visual Guide

```
┌───────────────────────────────────────────────────┐
│              PERFORMANCE TIPS                     │
├───────────────────────────────────────────────────┤
│                                                   │
│  Speed Hierarchy (Fast → Slow):                  │
│                                                   │
│  ⚡⚡⚡ Mock Mode + No Scraping                   │
│      ↓ (~3 sec/candidate)                        │
│                                                   │
│  ⚡⚡  Mock Mode + Scraping                       │
│      ↓ (~10 sec/candidate)                       │
│                                                   │
│  ⚡   Transformers + No Scraping                  │
│      ↓ (~12 sec/candidate)                       │
│                                                   │
│  🐢   Transformers + Scraping                     │
│       (~30 sec/candidate)                        │
│                                                   │
└───────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────┐
│              ACCURACY TIPS                        │
├───────────────────────────────────────────────────┤
│                                                   │
│  Accuracy Hierarchy (Low → High):                │
│                                                   │
│  📊   Mock Mode + No scraping + Short bios       │
│      ↓ (~70% accuracy)                           │
│                                                   │
│  📊📊 Mock Mode + Scraping                        │
│      ↓ (~75% accuracy)                           │
│                                                   │
│  📊📊📊 Transformers + No scraping               │
│      ↓ (~85% accuracy)                           │
│                                                   │
│  🎯   Transformers + Scraping + Rich data        │
│       (~90% accuracy)                            │
│                                                   │
└───────────────────────────────────────────────────┘
```

## 🎓 Learning Curve

```
Beginner                                    Expert
│                                              │
│  You are here                               │
▼                                              │
                                               │
Day 1: Install & run sample                   │
    ↓                                          │
Day 2: Upload own data                        │
    ↓                                          │
Day 3: Understand results                     │
    ↓                                          │
Week 2: Customize config                      │
    ↓                                          │
Week 3: Multiple use cases                    │
    ↓                                          │
Month 2: Integrate with workflow              │
    ↓                                          │
Month 3: Extend functionality                 │
    ↓                                          ▼
```

---

**Gunakan diagram ini untuk memahami workflow aplikasi! 🎨**

Untuk detail teknis, lihat: ARCHITECTURE.md  
Untuk contoh praktis, lihat: USAGE_EXAMPLES.md
