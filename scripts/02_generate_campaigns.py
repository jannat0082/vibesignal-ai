"""
CreatorIQ — Synthetic Data Generator
Step 2: Generate brands, campaigns, campaign_creators.
"""

import random
import numpy as np
import pandas as pd
from faker import Faker
import os

fake = Faker()
random.seed(42)
np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

NUM_BRANDS    = 15
NUM_CAMPAIGNS = 70

OBJECTIVES = ["awareness", "engagement", "conversion", "retention"]
STATUSES   = ["draft", "active", "completed", "paused"]
INDUSTRIES = ["fashion", "tech", "beauty", "food & beverage", "fitness", "finance"]

FEE_RANGES = {
    "nano":  (50,     500),
    "micro": (500,    5_000),
    "macro": (5_000,  50_000),
    "mega":  (50_000, 500_000),
}


def generate_brands(n=NUM_BRANDS):
    rows = []
    for i in range(n):
        rows.append({
            "brand_id":       i + 1,
            "brand_name":     fake.company(),
            "industry":       random.choice(INDUSTRIES),
            "target_segment": random.choice([
                "Gen Z", "Millennials", "Urban professionals", "Parents"
            ]),
            "country": random.choice([
                "United States", "United Kingdom", "India", "Canada"
            ]),
        })
    return pd.DataFrame(rows)


def generate_campaigns(brands_df, n=NUM_CAMPAIGNS):
    rows = []
    for i in range(n):
        brand_id     = random.choice(brands_df["brand_id"].tolist())
        start        = fake.date_between(start_date="-1y", end_date="-1m")
        duration     = random.randint(14, 90)
        end          = start + pd.Timedelta(days=duration)

        rows.append({
            "campaign_id":   i + 1,
            "brand_id":      brand_id,
            "campaign_name": f"{fake.catch_phrase()} Campaign",
            "objective":     random.choice(OBJECTIVES),
            "start_date":    start,
            "end_date":      end,
            "total_budget":  round(random.uniform(5_000, 250_000), 2),
            "status":        random.choice(STATUSES),
        })
    return pd.DataFrame(rows)


def generate_campaign_creators(campaigns_df, creators_df):
    rows    = []
    cc_id   = 1
    creator_campaigns = {}

    for _, campaign in campaigns_df.iterrows():
        n_creators      = random.randint(3, 10)
        chosen_creators = creators_df.sample(n=n_creators, random_state=cc_id)

        for _, creator in chosen_creators.iterrows():
            tier    = creator["tier"]
            fee     = round(random.uniform(*FEE_RANGES[tier]), 2)

            if random.random() < 0.15:
                multiplier = random.uniform(5, 8)
            else:
                multiplier = random.uniform(0.5, 3)

            revenue      = round(fee * multiplier, 2)
            handle_clean = creator["handle"].replace("@", "").split("_")[0].upper()

            # cc_id is guaranteed unique — no collision possible
            promo_code = f"{handle_clean}{cc_id}"

            cid = int(creator["creator_id"])
            if cid not in creator_campaigns:
                creator_campaigns[cid] = []
            creator_campaigns[cid].append(int(campaign["campaign_id"]))

            rows.append({
                "cc_id":                  cc_id,
                "campaign_id":            campaign["campaign_id"],
                "creator_id":             creator["creator_id"],
                "creator_fee":            fee,
                "revenue_attributed":     revenue,
                "impressions_delivered":  int(creator["follower_count"]
                                             * random.uniform(0.3, 1.2)),
                "promo_code":             promo_code,
                "status":                 random.choice([
                    "confirmed", "active", "completed"
                ]),
            })
            cc_id += 1

    return pd.DataFrame(rows), creator_campaigns


if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)

    creators_df = pd.read_csv(os.path.join(DATA_DIR, "creators.csv"))

    brands_df            = generate_brands()
    campaigns_df         = generate_campaigns(brands_df)
    campaign_creators_df, _ = generate_campaign_creators(campaigns_df, creators_df)

    # Referential integrity checks
    orphan_c = ~campaign_creators_df["creator_id"].isin(creators_df["creator_id"])
    orphan_p = ~campaign_creators_df["campaign_id"].isin(campaigns_df["campaign_id"])
    print("Orphan creator refs:", orphan_c.sum(), "(should be 0)")
    print("Orphan campaign refs:", orphan_p.sum(), "(should be 0)")
    print()
    print("campaign_creators shape:", campaign_creators_df.shape)
    print()

    # Duplicate promo_code check
    dupes = campaign_creators_df["promo_code"].duplicated().sum()
    print(f"Duplicate promo_codes: {dupes} (should be 0)")
    print()

    merged = campaign_creators_df.merge(
        creators_df[["creator_id", "tier"]], on="creator_id"
    )
    merged["roi_multiple"] = (merged["revenue_attributed"] / merged["creator_fee"])
    print("Avg ROI multiple by tier:")
    print(merged.groupby("tier")["roi_multiple"].mean()
               .reindex(["nano", "micro", "macro", "mega"]))

    brands_df.to_csv(os.path.join(DATA_DIR, "brands.csv"), index=False)
    campaigns_df.to_csv(os.path.join(DATA_DIR, "campaigns.csv"), index=False)
    campaign_creators_df.to_csv(
        os.path.join(DATA_DIR, "campaign_creators.csv"), index=False
    )
    print(f"\nSaved: brands.csv, campaigns.csv, campaign_creators.csv → {DATA_DIR}")