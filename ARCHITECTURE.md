# 🏗️ Arsitektur Aplikasi Sentivize

## 📐 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         STREAMLIT WEB UI                            │
│                           (app.py)                                  │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ File Upload  │  │   Keyword    │  │ Config Panel │             │
│  │   Widget     │  │    Input     │  │   (Sidebar)  │             │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
│         │                  │                  │                      │
│         └──────────────────┴──────────────────┘                      │
│                            │                                         │
└────────────────────────────┼─────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      SERVICES LAYER                                 │
│                      (services.py)                                  │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐          │
│  │  read_any_file()        - File parsing               │          │
│  │  detect_columns()       - Column detection           │          │
│  │  find_social_media()    - Web search                 │          │
│  │  fetch_posts()          - Web scraping               │          │
│  │  clean_text()           - Text preprocessing         │          │
│  └────────────────────┬─────────────────────────────────┘          │
└───────────────────────┼─────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    ANALYZER PIPELINE                                │
│                     (analyzer.py)                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  analyze_candidates()                                               │
│    ├─ Load & validate data                                         │
│    ├─ Detect columns                                               │
│    ├─ For each candidate:                                          │
│    │    ├─ Extract info (name, position, unit)                     │
│    │    ├─ Get/search social media links                           │
│    │    ├─ Collect texts (bio, posts, fallback)                    │
│    │    ├─ Call AI Analyzer ──────┐                                │
│    │    │   - Sentiment analysis   │                               │
│    │    │   - Relevance scoring    │                               │
│    │    └─ Compile results         │                               │
│    └─ Sort & return DataFrame      │                               │
│                                     │                               │
└─────────────────────────────────────┼───────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       AI ANALYZER                                   │
│                    (ai_analyzer.py)                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────┐         ┌────────────────────┐            │
│  │  TRANSFORMERS MODE │         │     MOCK MODE      │            │
│  ├────────────────────┤         ├────────────────────┤            │
│  │ - IndoBERT         │         │ - VADER Sentiment  │            │
│  │ - Multilingual     │         │ - TF-IDF           │            │
│  │   BERT             │   OR    │ - Cosine Sim       │            │
│  │ - Sentence         │         │ - Simple Rules     │            │
│  │   Transformers     │         │                    │            │
│  │ - Cosine Sim       │         │                    │            │
│  └────────────────────┘         └────────────────────┘            │
│           │                               │                         │
│           └───────────┬───────────────────┘                         │
│                       │                                             │
│  ┌────────────────────▼──────────────────────┐                     │
│  │  analyze_sentiment()                      │                     │
│  │    → (label, score)                       │                     │
│  │                                            │                     │
│  │  calculate_relevance()                    │                     │
│  │    → score                                │                     │
│  └───────────────────────────────────────────┘                     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ Results
                                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     OUTPUT GENERATION                               │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │   DataFrame      │  │  Excel File      │  │  Visualizations  │ │
│  │   (Results)      │  │  (2 sheets)      │  │  (Plotly Charts) │ │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Diagram

```
┌─────────────┐
│  User File  │ (CSV/XLSX/JSON)
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│  services.read_any_file()           │
│  - Parse file                       │
│  - Normalize columns                │
│  - Validate structure               │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  services.detect_columns()          │
│  - Name column                      │
│  - Social media column              │
│  - Bio/text column                  │
│  - Position, Unit columns           │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  FOR EACH CANDIDATE:                │
│                                     │
│  1. Extract basic info              │
│     ├─ Name (required)              │
│     ├─ Position (optional)          │
│     └─ Unit (optional)              │
│                                     │
│  2. Get social media                │
│     ├─ From file (if exists)        │
│     └─ OR search web                │
│        └─ services.find_social_     │
│           media_links()             │
│                                     │
│  3. Collect texts                   │
│     ├─ From bio column              │
│     ├─ From scraped posts           │
│     │  └─ services.fetch_posts()    │
│     └─ OR generate fallback         │
│        └─ services.create_fallback_ │
│           text()                    │
│                                     │
│  4. AI Analysis                     │
│     ├─ ai_analyzer.analyze_         │
│     │  sentiment(texts)             │
│     │  → (label, score)             │
│     │                               │
│     └─ ai_analyzer.calculate_       │
│        relevance(texts, keyword)    │
│        → score                      │
│                                     │
│  5. Compile result                  │
│     └─ {name, position, social,     │
│        sentiment, relevance, ...}   │
│                                     │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Aggregate Results                  │
│  - Convert to DataFrame             │
│  - Sort by relevance                │
│  - Calculate summary stats          │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Output to User                     │
│  ├─ Display in UI                   │
│  ├─ Generate visualizations         │
│  └─ Export to Excel                 │
└─────────────────────────────────────┘
```

## 🧩 Component Interaction Diagram

```
app.py (Streamlit UI)
  │
  ├─── Reads ───────────────────────► config.py
  │                                    (constants, settings)
  │
  ├─── Calls ───────────────────────► services.py
  │    │                               ├─ File handling
  │    │                               ├─ Column detection
  │    │                               └─ Web scraping
  │    │
  │    └─── Uses ───────────────────► External APIs
  │                                    ├─ DuckDuckGo Search
  │                                    ├─ Google Search
  │                                    └─ Web scraping
  │
  ├─── Calls ───────────────────────► analyzer.py
  │    │                               (Main pipeline)
  │    │
  │    └─── Calls ───────────────────► ai_analyzer.py
  │         │                          ├─ Sentiment analysis
  │         │                          └─ Relevance scoring
  │         │
  │         └─── Uses ───────────────► AI Models
  │                                    ├─ Transformers
  │                                    │  ├─ IndoBERT
  │                                    │  ├─ Multilingual BERT
  │                                    │  └─ Sentence-Transformers
  │                                    │
  │                                    └─ Mock Models
  │                                       ├─ VADER
  │                                       └─ TF-IDF
  │
  └─── Generates ───────────────────► Output
       ├─ DataFrames (pandas)
       ├─ Visualizations (plotly)
       └─ Excel files (openpyxl)
```

## 🔐 Security & Privacy Flow

```
┌──────────────┐
│  User Data   │
│  (Local PC)  │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────┐
│  Streamlit App (Local Server)    │
│  ├─ File processed locally       │
│  ├─ No data sent to cloud        │
│  └─ Results stored locally       │
└──────┬───────────────────────────┘
       │
       ├─── AI Models (Local)
       │    ├─ Load from cache
       │    └─ Run on CPU/GPU
       │
       └─── Web Search (External) ⚠️
            ├─ Name sent to search API
            ├─ Rate limited
            └─ Optional feature
```

## 📊 Processing Pipeline Detail

```
Input File → Parse → Validate → Detect Columns
                                      │
                                      ▼
                              ┌───────────────┐
                              │ For Each Row  │
                              └───────┬───────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
                    ▼                                   ▼
            ┌───────────────┐                  ┌───────────────┐
            │ Extract Info  │                  │ Get Text Data │
            ├───────────────┤                  ├───────────────┤
            │ - Name        │                  │ - From file   │
            │ - Position    │                  │ - From web    │
            │ - Unit        │                  │ - Fallback    │
            └───────┬───────┘                  └───────┬───────┘
                    │                                   │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
                            ┌──────────────────┐
                            │   AI Analysis    │
                            ├──────────────────┤
                            │ 1. Sentiment     │
                            │    - Preprocess  │
                            │    - Tokenize    │
                            │    - Predict     │
                            │    - Aggregate   │
                            │                  │
                            │ 2. Relevance     │
                            │    - Embed text  │
                            │    - Embed kw    │
                            │    - Calculate   │
                            │      similarity  │
                            └──────────┬───────┘
                                      │
                                      ▼
                            ┌──────────────────┐
                            │ Compile Result   │
                            ├──────────────────┤
                            │ {                │
                            │   name: ...,     │
                            │   sentiment: ...,│
                            │   relevance: ... │
                            │ }                │
                            └──────────┬───────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │ Next Candidate│
                              └───────────────┘
                                      │
                                      ▼
                              All candidates done
                                      │
                                      ▼
                              ┌───────────────┐
                              │ Sort & Output │
                              └───────────────┘
```

## 🎨 UI Component Structure

```
┌─────────────────────────────────────────────────────────┐
│                    STREAMLIT APP                        │
├─────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────┐ │
│  │               HEADER & TITLE                      │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │            DISCLAIMER (Expandable)                │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌────────────────┐  ┌──────────────────────────────┐ │
│  │   SIDEBAR      │  │      MAIN CONTENT            │ │
│  ├────────────────┤  ├──────────────────────────────┤ │
│  │ ⚙️ Config      │  │  📁 File Uploader            │ │
│  │                │  │     └─ Preview               │ │
│  │ - Model Mode   │  │                              │ │
│  │ - Scraping     │  │  🔑 Keyword Input            │ │
│  │ - Limits       │  │                              │ │
│  │                │  │  🚀 Analyze Button           │ │
│  │ ℹ️ Info        │  │                              │ │
│  │                │  │  ⏳ Progress Bar             │ │
│  │ - Models       │  │                              │ │
│  │ - Platforms    │  │  📊 Results Section          │ │
│  │ - Limits       │  │     ├─ Summary Stats        │ │
│  │                │  │     ├─ Table (interactive)  │ │
│  │                │  │     ├─ Visualizations       │ │
│  │                │  │     │  ├─ Bar chart         │ │
│  │                │  │     │  ├─ Pie chart         │ │
│  │                │  │     │  ├─ Scatter plot      │ │
│  │                │  │     │  └─ Histograms        │ │
│  │                │  │     └─ Download Button      │ │
│  └────────────────┘  └──────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 🗂️ File Organization

```
Sentivize/
│
├── Core Modules (Python)
│   ├── app.py          ─────► UI & orchestration
│   ├── config.py       ─────► Configuration
│   ├── services.py     ─────► Utilities
│   ├── ai_analyzer.py  ─────► AI models
│   └── analyzer.py     ─────► Main pipeline
│
├── Documentation (Markdown)
│   ├── README.md          ─────► Main docs
│   ├── QUICK_START.md     ─────► 5-min guide
│   ├── INSTALL.md         ─────► Installation
│   ├── USAGE_EXAMPLES.md  ─────► Examples
│   ├── PROJECT_SUMMARY.md ─────► Overview
│   ├── ARCHITECTURE.md    ─────► This file
│   └── CHECKLIST.md       ─────► Verification
│
├── Testing & Data
│   ├── test_simple.py     ─────► Test suite
│   └── sample_data.csv    ─────► Sample data
│
├── Development
│   ├── API_BLUEPRINT.py   ─────► FastAPI guide
│   └── requirements.txt   ─────► Dependencies
│
└── Configuration
    ├── .gitignore         ─────► Git config
    └── run.bat            ─────► Launcher
```

## 🔄 State Management

```
Streamlit Session State
│
├── results_df          ─────► Analysis results DataFrame
├── keyword             ─────► Current keyword
├── uploaded_file       ─────► Current file
└── analysis_status     ─────► Job status

(In production, consider Redis/Database for persistence)
```

## 🧠 AI Model Architecture

### Transformers Mode

```
Input Text
    │
    ▼
┌─────────────────────┐
│  Text Preprocessing │
│  - Clean            │
│  - Truncate         │
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     │           │
     ▼           ▼
┌─────────┐ ┌─────────┐
│ Sentiment│ │Relevance│
│ Pipeline │ │ Model   │
└──────┬───┘ └───┬─────┘
       │         │
       ▼         ▼
 ┌──────────┐ ┌──────────┐
 │IndoBERT  │ │Sentence  │
 │/MultiLing│ │Transform │
 │   BERT   │ │   MiniLM │
 └──────┬───┘ └───┬──────┘
        │         │
        ▼         ▼
    (label)   (embedding)
    (score)       │
                  ▼
            Cosine Similarity
                  │
                  ▼
              (score)
```

### Mock Mode

```
Input Text
    │
    ▼
┌─────────────────────┐
│  Text Processing    │
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     │           │
     ▼           ▼
┌─────────┐ ┌─────────┐
│  VADER  │ │ TF-IDF  │
└──────┬──┘ └───┬─────┘
       │        │
       ▼        ▼
   Sentiment  Vectors
   (label)      │
   (score)      ▼
          Cosine Sim
              │
              ▼
          (score)
```

## 📈 Scalability Considerations

```
Current: Single Process
┌──────────────┐
│ Streamlit    │
│ (1 instance) │
└──────┬───────┘
       │
       ▼
   [Process]

Future: Distributed
┌──────────────┐
│  Load Balancer│
└──────┬───────┘
       │
   ┌───┴───┬───────┐
   │       │       │
   ▼       ▼       ▼
[Worker] [Worker] [Worker]
   │       │       │
   └───┬───┴───┬───┘
       │       │
       ▼       ▼
   [Queue] [Cache]
   (Celery)(Redis)
```

---

**This architecture is modular and extensible!**

Each component can be:
- ✅ Tested independently
- ✅ Replaced with alternatives
- ✅ Scaled horizontally
- ✅ Deployed as microservice

For FastAPI conversion, see: `API_BLUEPRINT.py`
