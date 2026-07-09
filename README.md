# VibeSignal AI 🌻
VibeSignal AI is a budget-first creator intelligence prototype built for Indian D2C brands and marketing agencies. It helps brands decide — before they spend — whether to work with nano creators, micro creators, or a mixed strategy, and recommends specific creators and budget allocations for a given INR campaign budget.

## ✶ Problem Statement
Most influencer marketing tools show you which creators performed best
after a campaign ends. That's useful, but it's too late. VibeSignal AI helps brands make the decision before spending — by analyzing creator data, scoring each creator with VibeScore, and recommending a budget allocation strategy based on campaign goals. Built specifically for Indian D2C brands where budgets are tight and every rupee of creator spend needs to be justified.


## ✶ Key Features
- **VibeScore** — composite creator ranking across 5 weighted dimensions
- **Budget Allocator** — splits a fixed INR budget across recommended creators
- **Scenario Comparison** — nano vs micro vs mixed strategy side by side
- **Engagement Authenticity Risk Indicator** — flags possible risk signals
- **EDA Notebook** — 5 charts surfacing real patterns in the data
- **Excel Report** — auto-generated campaign KPI report

## ✶ Core Insight
Nano creators drive far higher engagement rates (up to ~8x vs mega creators), but large creators convert substantially better (observed ~44x higher conversion). Measuring engagement alone can mislead ROI-focused campaigns — VibeSignal aims to close that gap by prioritizing conversion-aligned signals and budget efficiency.

## ✶ VibeScore Framework
VibeScore is a transparent creator scoring framework that rates each creator from 0 to 100 across five dimensions.

| Dimension          | Weight | Purpose                                                                 |
| ------------------ | ------ | ----------------------------------------------------------------------- |
| Audience Fit       | 30%    | Measures how well the creator reaches the intended audience.            |
| Engagement Quality | 25%    | Evaluates whether followers are genuinely interacting with the content. |
| Content Relevance  | 20%    | Assesses how closely the content aligns with the brand category.        |
| Cost Efficiency    | 15%    | Measures value delivered per rupee spent.                               |
| Authenticity Risk  | 10%    | Flags possible signs of fake or low-quality engagement.                 |

Score Bands
- **75-100**: Scale — increase investment.
- **50-74**: Watch — monitor closely.
- **25-49**: Improve — refine the partnership strategy.
- **0-24**: Stop — exit the partnership.

VibeScore is a prototype decision framework, not a production-grade scoring system. The weights are configurable and intentionally transparent.

## ✶ Tech Stack

| What | Tool |
|---|---|
| Database | PostgreSQL on Supabase |
| Data scripts | Python (Faker, Pandas, NumPy) |
| Analysis | Jupyter notebook, Matplotlib, Seaborn |
| Scoring model | Python weighted algorithm |
| Risk indicator | Rule-based signal detection |
| Excel reports | openpyxl |
| Dashboard | Power BI |
| Web app | Streamlit |

---

## ✶ Data & Schema 
Database: PostgreSQL on Supabase
Rows: 5,165 across 7 tables

| Table | Rows | What it stores |
|---|---|---|
| brands | 15 | D2C brand profiles |
| creators | 200 | Creator profiles with tier and engagement data |
| campaigns | 70 | Campaign budgets, objectives, dates |
| campaign_creators | 460 | Who worked in which campaign, for what fee |
| posts | 783 | Content metrics — likes, views, clicks, reach |
| conversions | 2,437 | Actual purchases with promo codes |
| audience_demographics | 1,200 | Creator audience breakdown |

## ✶ Project Structure


```bash
vibesignal-ai
├── sql
│   └── schema.sql
├── data/                    # gitignored — generated via scripts
├── scripts
│   ├── 01_generate_creators.py
│   ├── 02_generate_campaigns.py
│   ├── 03_generate_posts.py
│   ├── 04_generate_conversions.py
│   ├── 05_generate_audience_demographics.py
│   ├── 06_generate_excel_report.py
│   └── 07_vibescore_model.py
├── notebooks
│   ├── 01_eda_analysis.ipynb
│   └── charts/              # 5 PNG files
├── dashboards/
├── docs
│   ├── data_methodology.md
│   └── learning_journal.md
├── README.md
└── .gitignore
```

## ✶ Getting Started

```bash
git clone https://github.com/jannat0082/vibesignal-ai.git
cd vibesignal-ai
pip install faker pandas numpy matplotlib seaborn scikit-learn openpyxl
python scripts/01_generate_creators.py
python scripts/02_generate_campaigns.py
python scripts/03_generate_posts.py
python scripts/04_generate_conversions.py
python scripts/05_generate_audience_demographics.py
```


## ✶ Challenges & Fixes

**Promo code collision** — used `random.randint(10,99)` which only
has 90 possible values. Got 18 duplicate codes across 462 rows.
Fixed by using `cc_id` instead — a guaranteed unique counter.

**The 68.0 problem** — pandas saves nullable integers as float64.
So `68` became `68.0` and Supabase rejected it. Fixed by casting
to `Int64` before saving.

**Too many organic posts** — 37.5% of creators had zero campaign
history because 40 campaigns wasn't enough. Fixed by increasing
to 70 campaigns.


## ✶ Data Disclaimer

This project is a portfolio prototype built using benchmark-grounded
synthetic data. Engagement rate ranges are sourced from Influencer
Marketing Hub and Qoruz 2025-2026 reports. Recommendations and
estimates demonstrate decision-support logic and are not guaranteed
real-world outcomes.
Real campaign data, creator consent, and platform-compliant data
access would be required for production use.


## ✶ Progress

|  | Module | Focus | Status |
|---|---|---|---|
| 1 | Database | 7-table PostgreSQL schema | Complete |
| 2 | Data Generation | 5 Python generators, 5165 rows |  Complete |
| 3 | EDA | Jupyter notebook, 5 charts |  Complete |
| 4 | Excel Report | Auto-generated KPI report |  Complete |
| 5 | VibeScore Model | Creator scoring algorithm |  In Progress |
| 6 | Budget Allocator | INR budget split tool | Upcoming |
| 7 | Scenario Comparison | Nano vs micro vs mixed |  Upcoming |
| 8 | Risk Indicator | Authenticity risk flagging |  Upcoming |
| 9 | Power BI | Executive dashboard |  Upcoming |
| 10 | Streamlit | Live deployed app |  Upcoming |


