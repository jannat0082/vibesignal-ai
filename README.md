# CreatorIQ — AI-Powered Creator Marketing Analytics Platform

An end-to-end analytics platform that helps brands identify which creator
partnerships drive real ROI — going beyond vanity metrics to measure actual
business outcomes.

## The problem this solves

Most brands waste marketing budget on creators who look good on paper
(high likes, high followers) but generate zero actual sales. CreatorIQ
uses data and AI to separate real performers from vanity metrics.

## The 5 business questions this project answers

1. Which creators generate the highest ROI and revenue?
2. Which partnerships drive real conversions vs only engagement?
3. Which audience segments respond best to creator campaigns?
4. Which platforms, categories and content formats perform best?
5. Which creators should we scale, improve, or stop?

## Tech stack

| Layer | Tool | Purpose |
|---|---|---|
| Database | PostgreSQL (Supabase) | 7-table schema, cloud-hosted |
| Data generation | Python + Faker | 5,330 rows of synthetic data |
| Analysis | Pandas, NumPy, Jupyter | EDA and feature engineering |
| AI scoring | scikit-learn, VADER | CreatorScore model + sentiment |
| Reporting | Excel (openpyxl) | Auto-generated KPI reports |
| Dashboard | Power BI | 3-page executive dashboard |
| Web app | Streamlit | Live deployed analytics app |
| Version control | Git + GitHub | Documented commit history |

## Database schema — 7 tables

| Table | Rows | Purpose |
|---|---|---|
| brands | 15 | Companies running campaigns |
| creators | 200 | Influencer profiles |
| campaigns | 70 | Marketing campaigns |
| campaign_creators | 460 | Creator-campaign partnerships |
| posts | 783 | Published content metrics |
| conversions | 2,437 | Actual sales and purchases |
| audience_demographics | 1,200 | Creator audience breakdowns |

## Project structure

creatoriq/
├── sql/              # PostgreSQL schema
├── data/             # Generated datasets (gitignored)
├── scripts/          # Data generation pipeline
├── notebooks/        # Python EDA and ML modeling
├── dashboards/       # Power BI files
└── docs/             # ERD, methodology, write-ups

## How to reproduce the dataset locally

git clone https://github.com/jannat0082/creatoriq.git
cd creatoriq
pip install faker pandas numpy scikit-learn
python scripts/01_generate_creators.py
python scripts/02_generate_campaigns.py
python scripts/03_generate_posts.py
python scripts/04_generate_conversions.py
python scripts/05_generate_audience_demographics.py

## Data methodology

This project uses synthetic data engineered to match published
2025-2026 industry benchmarks — not arbitrary random numbers.
See docs/data_methodology.md for full sourcing and citations.