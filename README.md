# CREATORIQ 🌻

An analytics platform I built to help brands figure out which creator 
partnerships are actually worth the money — not just which ones get the 
most likes.

**Problem Statement:** Most influencer marketing dashboards show you 
engagement metrics. Nobody tells you which creators actually drive sales. 
That gap is what this project tries to solve.

---

## ✶ Project Overview 

Brands spend millions on creator partnerships without knowing which ones 
convert. CreatorIQ analyzes creator data across 5 dimensions:

- Which creators give the best ROI (not just the most reach)
- Which partnerships drive actual purchases vs just engagement
- Which audience segments respond and actually buy
- Which platforms and content formats perform best
- Which creators to scale, fix, or drop entirely

---

## ✶ Key Findings

The biggest insight surprised me. Nano creators (under 10K followers) 
get **8x more engagement** than mega creators. But when I looked at 
actual conversion rates, mega creators convert **44x better**.

So brands paying for engagement are measuring the wrong thing. That's 
the whole point of this project.

Other findings:
- Twitter leads engagement at 6.14% (not Instagram, which most people 
  assume)
- Video content outperforms reels and stories at 6.08%
- 70% of purchases happen on mobile
- Average order value from creator-driven sales: $66

---

## ✶ Tech stack

| What | Tool |
|---|---|
| Database | PostgreSQL on Supabase |
| Data scripts | Python (Faker, Pandas, NumPy) |
| Analysis | Jupyter notebook, Matplotlib, Seaborn |
| AI model | scikit-learn, VADER sentiment  |
| Excel reports | openpyxl |
| Dashboard | Power BI  |
| Web app | Streamlit |

---

## ✶ Database — 7 tables, 5,165 rows

I designed the schema from scratch starting with business questions, 
not from a tutorial. Every table exists because a specific business 
question needed it.

| Table | Rows | What it stores |
|---|---|---|
| brands | 15 | Companies running campaigns |
| creators | 200 | Creator profiles, tiers, engagement rates |
| campaigns | 70 | Campaign budgets, objectives, dates |
| campaign_creators | 460 | Who worked in which campaign, for what fee |
| posts | 783 | Content metrics — likes, views, clicks, reach |
| conversions | 2,437 | Actual purchases with promo codes and demographics |
| audience_demographics | 1,200 | Creator audience breakdown by age and gender |

---

## ✶ Project structure

```
  creatoriq
│
├── 📂 sql
│   └── 📄 schema.sql                         
│
├── 📂 data   # gitignored — run scripts to generate                     
│
├── 📂 scripts                                
│   ├──  01_generate_creators.py             
│   ├──  02_generate_campaigns.py            
│   ├──  03_generate_posts.py               
│   ├──  04_generate_conversions.py          
│   └──  05_generate_audience_demographics.py 
│
├── 📂 notebooks                              
│   ├──  01_eda_analysis.ipynb              
│   ├──  chart_01_tier_analysis.png
│   ├──  chart_02_vanity_metrics.png
│   ├──  chart_03_platform_format.png
│   ├──  chart_04_roi_analysis.png
│   └──  chart_05_revenue_summary.png
│
├── 📂 dashboards                              
│
├── 📂 docs
│   └── 📄 data_methodology.md                
├── 📄 README.md
└── 📄 .gitignore
```
---

## ✶ Getting Started

```bash
git clone https://github.com/jannat0082/creatoriq.git
cd creatoriq
pip install faker pandas numpy matplotlib seaborn scikit-learn openpyxl
python scripts/01_generate_creators.py
python scripts/02_generate_campaigns.py
python scripts/03_generate_posts.py
python scripts/04_generate_conversions.py
python scripts/05_generate_audience_demographics.py
```

---

## ✶ Challenges & Fixes

These aren't made up. These happened.

**Promo code collision** — I generated unique promo codes using 
`random.randint(10,99)`. Turns out that's only 90 possible values. 
With common first names like "John" appearing on multiple creators, 
I got 18 duplicate codes across 462 rows. Fixed by using `cc_id` 
instead — a counter that's guaranteed unique.

**The 68.0 problem** — Pandas saves integer columns as float when 
they contain NULL values. So `68` became `68.0` in the CSV, and 
Supabase rejected it because the column type is integer. Fixed by 
casting to `Int64` (pandas nullable integer) before saving.

**Too many organic posts** — 37.5% of my creators had zero campaign 
history because 40 campaigns wasn't enough to reach 200 creators. 
Their posts were all forced organic. Fixed by increasing campaigns 
from 40 to 70.

**Path errors** — My scripts were saving CSVs to the wrong folder 
because I was running them from different directories. Fixed by using 
`os.path.abspath(__file__)` to build paths relative to the script 
location, not wherever I ran it from.

---

## ✶ Data Methodology

Real campaign data is confidential. Agencies don't publish creator 
ROI numbers. Scraping Instagram violates their ToS.

So I built synthetic data that follows real industry patterns. The 
engagement rate ranges come from Influencer Marketing Hub and Qoruz 
2025-2026 benchmark reports. The individual rows are fake. The 
patterns are real.

Full details in `docs/data_methodology.md`.

---

## ✶ Progress


|  | Module | Focus | Deliverables | Status |
|---|---|---|---|---|
| 1 | Foundation | SQL schema + database setup | 7-table PostgreSQL schema, ERD, data dictionary |  Complete |
| 2 | Data Generation | Python synthetic data pipeline | 5 scripts, 5,165 rows, 7 tables populated |  Complete |
| 3 | Python EDA | Exploratory data analysis | 8-cell Jupyter notebook, 5 charts, key insights |  Complete |
| 4 | Excel Reporting | Automated KPI reports | Auto-generated .xlsx campaign report |  In Progress |
| 5 | AI / ML Model | Creator Scoring model | Weighted model, sentiment analysis, fake engagement detector | Upcoming |
| 6 | Power BI | Executive dashboard | 3-page interactive dashboard with DAX measures |  Upcoming |
| 7 | Streamlit | Live web application | Deployed app with shareable URL | Upcoming |



