"""
CreatorIQ — Synthetic Data Generator
Step 1: Generate the creators table.
"""

import random
import numpy as np
import pandas as pd
from faker import Faker
import os

fake = Faker()
random.seed(42)
np.random.seed(42)

# Build path relative to this script's location — works regardless of
# where you run the script from
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

NUM_CREATORS = 200

TIER_WEIGHTS = {
    "nano":  0.50,
    "micro": 0.30,
    "macro": 0.15,
    "mega":  0.05,
}

TIER_CONFIG = {
    "nano":  {"followers": (1_000, 10_000),        "engagement": (6.0, 10.0)},
    "micro": {"followers": (10_000, 100_000),      "engagement": (3.0, 6.0)},
    "macro": {"followers": (100_000, 1_000_000),   "engagement": (1.0, 3.0)},
    "mega":  {"followers": (1_000_000, 5_000_000), "engagement": (0.5, 1.5)},
}

PLATFORMS = ["instagram", "youtube", "tiktok", "twitter"]
NICHES    = ["fitness", "beauty", "gaming", "finance",
             "travel", "food", "fashion", "tech"]
COUNTRIES = ["United States", "United Kingdom", "India",
             "Canada", "Australia", "Germany"]


def generate_creators(n=NUM_CREATORS):
    rows = []
    tiers = random.choices(
        population=list(TIER_WEIGHTS.keys()),
        weights=list(TIER_WEIGHTS.values()),
        k=n,
    )

    for i in range(n):
        tier   = tiers[i]
        config = TIER_CONFIG[tier]

        follower_count      = random.randint(*config["followers"])
        avg_engagement_rate = round(random.uniform(*config["engagement"]), 2)

        name   = fake.name()
        handle = "@" + name.lower().replace(" ", "_") + str(random.randint(1, 999))

        rows.append({
            "creator_id":                  i + 1,
            "name":                        name,
            "handle":                      handle,
            "platform":                    random.choice(PLATFORMS),
            "niche":                       random.choice(NICHES),
            "tier":                        tier,
            "follower_count":              follower_count,
            "avg_engagement_rate":         avg_engagement_rate,
            "country":                     random.choice(COUNTRIES),
            "audience_authenticity_score": None,
            "joined_date":                 fake.date_between(start_date="-3y", end_date="-3m"),
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)

    df = generate_creators()

    print("Shape:", df.shape)
    print()
    print("Tier distribution:")
    print(df["tier"].value_counts())
    print()
    print("Engagement rate by tier -- should DECREASE as tier grows:")
    print(df.groupby("tier")["avg_engagement_rate"].mean()
            .reindex(["nano", "micro", "macro", "mega"]))
    print()
    print(df.head(5).to_string())

    out = os.path.join(DATA_DIR, "creators.csv")
    df.to_csv(out, index=False)
    print(f"\nSaved to {out}")