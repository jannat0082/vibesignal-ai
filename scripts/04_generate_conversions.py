"""
CreatorIQ — Synthetic Data Generator
Step 4: Generate conversions.

Three creator types deliberately engineered:
  - Vanity Creator:   high engagement, low conversion rate
  - Silent Converter: low/mid engagement, high conversion rate
  - True Performer:   high engagement, high conversion rate
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

CREATOR_TYPE_WEIGHTS = {
    "vanity":    0.45,
    "converter": 0.35,
    "performer": 0.20,
}

CONVERSION_RATE_BY_TYPE = {
    "vanity":    (0.001, 0.008),
    "converter": (0.025, 0.080),
    "performer": (0.015, 0.045),
}

ORDER_VALUE_MEAN = 65
ORDER_VALUE_MIN  = 12
ORDER_VALUE_MAX  = 800

AGE_GROUPS     = ["13-17", "18-24", "25-34", "35-44", "45-54", "55+"]
GENDERS        = ["male", "female", "non-binary"]
DEVICE_TYPES   = ["mobile", "desktop", "tablet"]
DEVICE_WEIGHTS = [0.70, 0.22, 0.08]
LOCATIONS      = [
    "United States", "United Kingdom", "India",
    "Canada", "Australia", "Germany"
]


def assign_creator_types(creators_df):
    types = random.choices(
        population=list(CREATOR_TYPE_WEIGHTS.keys()),
        weights=list(CREATOR_TYPE_WEIGHTS.values()),
        k=len(creators_df),
    )
    return dict(zip(creators_df["creator_id"].tolist(), types))


def generate_order_value():
    value = np.random.exponential(ORDER_VALUE_MEAN)
    value = max(ORDER_VALUE_MIN, min(ORDER_VALUE_MAX, value))
    return round(value, 2)


def generate_conversions(posts_df, creators_df, campaign_creators_df):
    creator_types = assign_creator_types(creators_df)

    promo_lookup = dict(
        zip(
            campaign_creators_df["creator_id"].tolist(),
            campaign_creators_df["promo_code"].tolist(),
        )
    )

    rows          = []
    conversion_id = 1

    for _, post in posts_df.iterrows():
        creator_id  = int(post["creator_id"])
        campaign_id = post["campaign_id"]
        post_id     = int(post["post_id"])
        clicks      = int(post["clicks"])
        posted_at   = pd.to_datetime(post["posted_at"])

        if clicks == 0:
            continue

        creator_type    = creator_types.get(creator_id, "vanity")
        cvr_range       = CONVERSION_RATE_BY_TYPE[creator_type]
        cvr             = random.uniform(*cvr_range)
        num_conversions = max(0, int(clicks * cvr))

        if pd.isna(campaign_id):
            num_conversions = int(num_conversions * 0.60)
            clean_campaign_id = pd.NA
        else:
            clean_campaign_id = int(campaign_id)

        for _ in range(num_conversions):
            days_after   = random.randint(0, 14)
            converted_at = posted_at + pd.Timedelta(days=days_after)

            rows.append({
                "conversion_id": conversion_id,
                "post_id":       post_id,
                "campaign_id":   clean_campaign_id,
                "order_value":   generate_order_value(),
                "promo_code":    promo_lookup.get(creator_id),
                "age_group":     random.choice(AGE_GROUPS),
                "gender":        random.choice(GENDERS),
                "location":      random.choice(LOCATIONS),
                "device_type":   random.choices(
                                     DEVICE_TYPES,
                                     weights=DEVICE_WEIGHTS,
                                     k=1
                                 )[0],
                "converted_at":  converted_at,
            })
            conversion_id += 1

    return pd.DataFrame(rows), creator_types


if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)

    creators_df          = pd.read_csv(os.path.join(DATA_DIR, "creators.csv"))
    posts_df             = pd.read_csv(os.path.join(DATA_DIR, "posts.csv"))
    campaign_creators_df = pd.read_csv(os.path.join(DATA_DIR, "campaign_creators.csv"))

    conversions_df, creator_types = generate_conversions(
        posts_df, creators_df, campaign_creators_df
    )

    # Fix integer columns BEFORE saving
    # pandas uses float64 when NULLs exist -- Int64 keeps integers clean
    conversions_df["campaign_id"] = conversions_df["campaign_id"].astype("Int64")
    conversions_df["post_id"]     = conversions_df["post_id"].astype("Int64")

    print("Shape:", conversions_df.shape)
    print()

    # Validation 1: Revenue check
    total_revenue = conversions_df["order_value"].sum()
    avg_order     = conversions_df["order_value"].mean()
    print(f"Total revenue:       ${total_revenue:,.2f}")
    print(f"Average order value: ${avg_order:.2f}  (target ~$65)")
    print()

    # Validation 2: Device split
    print("Device split (mobile should be ~70%):")
    print(conversions_df["device_type"]
          .value_counts(normalize=True)
          .mul(100).round(1))
    print()

    # Validation 3: Core insight check
    posts_df["creator_type"] = posts_df["creator_id"].map(creator_types)
    conv_by_post = (
        conversions_df.groupby("post_id")
        .size()
        .reset_index(name="conversions")
    )
    posts_merged = posts_df.merge(conv_by_post, on="post_id", how="left")
    posts_merged["conversions"] = posts_merged["conversions"].fillna(0)
    posts_merged["cvr"] = (
        posts_merged["conversions"] /
        posts_merged["clicks"].replace(0, np.nan)
    )
    print("Average CVR by creator type:")
    print("(vanity LOWEST, converter HIGHEST)")
    print(posts_merged.groupby("creator_type")["cvr"]
          .mean().mul(100).round(3))
    print()

    # Validation 4: No float integers in output
    print("campaign_id dtype (must be Int64, not float64):")
    print(conversions_df["campaign_id"].dtype)
    print("Sample values:")
    print(conversions_df["campaign_id"].head(5).to_string())
    print()

    # Validation 5: Orphan check
    orphan_posts = ~conversions_df["post_id"].isin(posts_df["post_id"])
    print(f"Orphan post references: {orphan_posts.sum()} (should be 0)")
    print()

    out = os.path.join(DATA_DIR, "conversions.csv")
    conversions_df.to_csv(out, index=False)
    print(f"Saved to {out}")