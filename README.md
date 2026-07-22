# VibeSignal AI 🌼

VibeSignal AI is a budget-first creator intelligence system designed for Indian D2C brands and marketing agencies. It supports pre-campaign decision-making by evaluating creators, estimating budget allocation options, and recommending nano, micro, or mixed creator strategies based on campaign objectives and fixed INR budgets.

## ✶ Overview

Influencer marketing tools often report creator performance after a campaign has ended. That approach is useful for post-campaign analysis, but it does not support early-stage budget decisions. VibeSignal AI addresses this gap by analyzing creator-level data in advance, assigning a VibeScore to each creator, and recommending budget allocation strategies aligned with campaign goals.

The project is built for budget-sensitive teams that need transparent, data-backed creator selection rather than intuition-led decisions.

## ✶ Business Objective

VibeSignal AI was designed to improve campaign planning for Indian D2C brands and marketing agencies operating with fixed creator budgets. The objective is to identify which creators are most likely to deliver value, how the budget should be allocated, and whether a nano, micro, or mixed strategy is best suited to the campaign goal.

## ✶ Problem Statement

Most influencer platforms focus on reporting results after the campaign is complete. While this helps with retrospective analysis, it does not solve the more important question faced by brands before launch: which creators should receive budget, and how much?

VibeSignal AI addresses this by combining creator scoring, campaign-level analysis, and budget allocation logic into a decision-support framework.

## ✶ Solution

VibeSignal AI provides a structured workflow for evaluating creators before a campaign begins:

- **VibeScore** ranks creators using a transparent weighted model.
- **Budget Allocator** distributes a fixed INR budget across recommended creators.
- **Scenario Comparison** evaluates nano, micro, and mixed strategies side by side.
- **Engagement Authenticity Risk Indicator** flags potential low-quality engagement signals.
- **EDA Notebook** surfaces patterns in creator performance, engagement, and conversion behavior.
- **Excel Report** generates a campaign-ready KPI summary.

## ✶ Methodology

The project follows a structured analytics pipeline. Creator, campaign, post, conversion, and audience data are generated and stored in PostgreSQL, then analyzed in Python using Pandas, NumPy, Matplotlib, and Seaborn.

A weighted scoring model assigns each creator a VibeScore based on five dimensions: audience fit, engagement quality, content relevance, cost efficiency, and authenticity risk. The EDA notebook and supporting reports are used to validate patterns, compare creator tiers, and support budget allocation logic.

## ✶ Core Insight

The analysis shows that nano creators can generate significantly higher engagement, while larger creators may deliver stronger conversion performance. This makes engagement-only evaluation insufficient for ROI-focused campaigns.

VibeSignal AI is designed to support more balanced creator selection by considering both engagement quality and conversion potential.

## ✶ VibeScore Framework

VibeScore assigns each creator a score from 0 to 100 across five dimensions.

| Dimension | Weight | Purpose |
|---|---:|---|
| Audience Fit | 30% | Measures how well the creator reaches the intended audience. |
| Engagement Quality | 25% | Evaluates whether followers are genuinely interacting with the content. |
| Content Relevance | 20% | Assesses how closely the content aligns with the brand category. |
| Cost Efficiency | 15% | Measures value delivered per rupee spent. |
| Authenticity Risk | 10% | Flags possible signs of fake or low-quality engagement. |

### ✶ Score Bands
- **75–100**: Scale — increase investment.
- **50–74**: Watch — monitor closely.
- **25–49**: Improve — refine the partnership strategy.
- **0–24**: Stop — exit the partnership.

> VibeScore is a prototype decision framework. Weights are configurable and intentionally transparent.

## ✶ Tech Stack

| Component | Technology |
|---|---|
| Database | PostgreSQL on Supabase |
| Data Generation | Python, Faker, Pandas, NumPy |
| Analysis | Jupyter Notebook, Matplotlib, Seaborn |
| Scoring Model | Python-based weighted algorithm |
| Risk Indicator | Rule-based signal detection |
| Reporting | openpyxl |
| Dashboard | Power BI |
| Web App | Streamlit |

## ✶ Data & Schema

The database contains 5,165 rows across 7 tables.

| Table | Rows | Description |
|---|---:|---|
| brands | 15 | D2C brand profiles |
| creators | 200 | Creator profiles with tier and engagement data |
| campaigns | 70 | Campaign budgets, objectives, and dates |
| campaign_creators | 460 | Creator assignments and fees |
| posts | 783 | Content metrics such as likes, views, clicks, and reach |
| conversions | 2,437 | Purchases attributed to promo codes |
| audience_demographics | 1,200 | Audience breakdown by creator |

## ✶ Results

VibeSignal AI produced a structured creator selection and budget-planning workflow for Indian D2C campaigns. The analysis showed that engagement and conversion do not always move together, which reinforces the need for a multi-factor scoring approach rather than relying on reach or engagement alone.

The project also surfaced clear patterns in creator performance, audience behavior, and content format effectiveness through EDA. These findings informed the VibeScore framework, the budget allocation logic, and the scenario comparison approach used to evaluate nano, micro, and mixed creator strategies.

From an implementation standpoint, the repository includes reproducible data generation scripts, a scoring model, an Excel report, and an analysis notebook with supporting visualizations. This makes the project easy to review, test, and extend as a decision-support system.

## ✶ Repository Structure

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

## ✶ Setup

### Prerequisites
- Python 3.10 or later
- Git
- A local virtual environment is recommended

### Installation
```bash
git clone https://github.com/jannat0082/vibesignal-ai.git
cd vibesignal-ai
python -m venv .venv
# Windows:
# .venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate
pip install --upgrade pip
pip install faker pandas numpy matplotlib seaborn scikit-learn openpyxl
```

### Run the Project
```bash
python scripts/01_generate_creators.py
python scripts/02_generate_campaigns.py
python scripts/03_generate_posts.py
python scripts/04_generate_conversions.py
python scripts/05_generate_audience_demographics.py
python scripts/06_generate_excel_report.py
python scripts/07_vibescore_model.py
```

### Notes
- The `data/` directory is gitignored because it contains generated outputs.
- The scripts are intended to be executed in sequence.
- Additional analysis is available in `notebooks/01_eda_analysis.ipynb`.

## ✶ Challenges and Resolutions

- **Promo code collisions** were caused by a limited random number range. This was resolved by using `cc_id` as a unique identifier.
- **Nullable integer export issues** occurred because pandas converted integers to float values such as `68.0`. This was resolved by casting fields to `Int64` before export.
- **Limited campaign history** reduced creator coverage. This was improved by increasing the number of campaigns from 40 to 70.

## ✶ Data Disclaimer

This project uses benchmark-informed synthetic data for demonstration and evaluation purposes. Engagement assumptions are based on public industry reports, and the recommendations are intended to illustrate decision-support logic rather than guarantee real-world outcomes. Production deployment would require real campaign data, creator consent, and platform-compliant access.

## ✶ Project Status

| Module | Status |
|---|---|
| Database | Complete |
| Data Generation | Complete |
| EDA | Complete |
| Excel Report | Complete |
| VibeScore Model | In Progress |
| Budget Allocator | Upcoming |
| Scenario Comparison | Upcoming |
| Risk Indicator | Upcoming |
| Power BI | Upcoming |
| Streamlit | Upcoming |

## ✶ Live Preview

- Repository: [VibeSignal AI](https://github.com/jannat0082/vibesignal-ai)
