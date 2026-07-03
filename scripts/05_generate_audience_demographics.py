"""
CreatorIQ — Synthetic Data Generator
Step 5: Generate audience_demographics.

One creator has MULTIPLE rows in this table -- one per age group.
All percentage_shares for a single creator MUST sum to 100.
This constraint is enforced in Python before touching the database.
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

AGE_GROUPS = ["13-17", "18-24", "25-34", "35-44", "45-54", "55+"]
GENDERS    = ["male", "female", "non-binary"]
COUNTRIES  = ["United States", "United Kingdom", "India",
              "Canada", "Australia", "Germany"]
INTERESTS  = ["fitness", "beauty", "gaming", "finance",
              "travel", "food", "fashion", "tech"]

# Age distribution varies by niche
# Gaming skews young, finance skews older, beauty peaks 18-34
NICHE_AGE_WEIGHTS = {
    "gaming":   [0.25, 0.35, 0.20, 0.10, 0.06, 0.04],
    "beauty":   [0.10, 0.30, 0.30, 0.15, 0.10, 0.05],
    "fitness":  [0.05, 0.25, 0.35, 0.20, 0.10, 0.05],
    "finance":  [0.02, 0.10, 0.30, 0.30, 0.18, 0.10],
    "travel":   [0.05, 0.20, 0.30, 0.25, 0.15, 0.05],
    "food":     [0.08, 0.22, 0.28, 0.22, 0.12, 0.08],
    "fashion":  [0.12, 0.32, 0.28, 0.15, 0.08, 0.05],
    "tech":     [0.08, 0.28, 0.32, 0.20, 0.08, 0.04],
}

DEFAULT_AGE_WEIGHTS = [0.10, 0.25, 0.28, 0.20, 0.12, 0.05]


def generate_age_percentages(niche):
    """
    Generate age group shares that sum to exactly 100.
    We add small noise to base weights then normalize --
    so every creator in the same niche looks slightly different
    but follows the same general age pattern.
    """
    base_weights = NICHE_AGE_WEIGHTS.get(niche, DEFAULT_AGE_WEIGHTS)

    noisy_weights = [
        max(0.01, w + random.uniform(-0.05, 0.05))
        for w in base_weights
    ]

    total       = sum(noisy_weights)
    percentages = [round((w / total) * 100, 2) for w in noisy_weights]

    # Fix any floating point rounding so sum is exactly 100
    diff           = round(100.0 - sum(percentages), 2)
    percentages[-1] = round(percentages[-1] + diff, 2)

    return percentages


def generate_audience_demographics(creators_df):
    """
    Generate audience demographics for every creator.
    200 creators x 6 age groups = 1,200 rows minimum.
    """
    rows    = []
    demo_id = 1

    for _, creator in creators_df.iterrows():
        creator_id = int(creator["creator_id"])
        niche      = creator["niche"]

        age_percentages = generate_age_percentages(niche)

        for i, age_group in enumerate(AGE_GROUPS):

            # Gender split varies by niche
            if niche in ["beauty", "fashion"]:
                gender_weights = [0.20, 0.72, 0.08]
            elif niche in ["gaming", "tech", "finance"]:
                gender_weights = [0.62, 0.30, 0.08]
            else:
                gender_weights = [0.45, 0.48, 0.07]

            rows.append({
                "demo_id":           demo_id,
                "creator_id":        creator_id,
                "age_group":         age_group,
                "gender":            random.choices(
                                         GENDERS,
                                         weights=gender_weights,
                                         k=1
                                     )[0],
                "country":           random.choice(COUNTRIES),
                "interest_category": niche,
                "percentage_share":  age_percentages[i],
                "recorded_at":       fake.date_between(
                                         start_date="-6m",
                                         end_date="today"
                                     ),
            })
            demo_id += 1

    return pd.DataFrame(rows)


if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)

    creators_df = pd.read_csv(os.path.join(DATA_DIR, "creators.csv"))
    demo_df     = generate_audience_demographics(creators_df)

    print("Shape:", demo_df.shape)
    print()

    # Validation 1: Every creator must have exactly 6 rows
    rows_per_creator = demo_df.groupby("creator_id").size()
    print("Rows per creator (all should be 6):")
    print(rows_per_creator.value_counts())
    print()

    # Validation 2: Percentage shares must sum to 100
    sums     = demo_df.groupby("creator_id")["percentage_share"].sum()
    not_100  = sums[abs(sums - 100) > 0.1]
    print(f"Creators with shares not summing to 100: {len(not_100)}")
    print("(should be 0)")
    print()

    # Validation 3: Age skew by niche
    creators_with_niche = demo_df.merge(
        creators_df[["creator_id", "niche"]], on="creator_id"
    )
    print("Average % for 18-24 age group by niche:")
    print("(gaming + beauty should be highest)")
    print(
        creators_with_niche[
            creators_with_niche["age_group"] == "18-24"
        ]
        .groupby("niche")["percentage_share"]
        .mean().round(1)
        .sort_values(ascending=False)
    )
    print()

    # Validation 4: Referential integrity
    orphans = ~demo_df["creator_id"].isin(creators_df["creator_id"])
    print(f"Orphan creator references: {orphans.sum()} (should be 0)")
    print()

    out = os.path.join(DATA_DIR, "audience_demographics.csv")
    demo_df.to_csv(out, index=False)
    print(f"Saved to {out}")