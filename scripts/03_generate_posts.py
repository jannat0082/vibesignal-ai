"""
CreatorIQ — Synthetic Data Generator
Step 3: Generate posts.
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

CONTENT_FORMATS = ["reel", "short", "story", "video", "image", "carousel"]

REACH_MULTIPLIER = {
    "instagram": (0.15, 0.40),
    "youtube":   (0.20, 0.60),
    "tiktok":    (0.30, 0.90),
    "twitter":   (0.10, 0.30),
}

POSTS_PER_CREATOR = (2, 6)


def generate_posts(creators_df, campaign_creators_df):
    rows    = []
    post_id = 1

    creator_campaigns = (
        campaign_creators_df
        .groupby("creator_id")["campaign_id"]
        .apply(list)
        .to_dict()
    )

    for _, creator in creators_df.iterrows():
        creator_id      = creator["creator_id"]
        platform        = creator["platform"]
        followers       = creator["follower_count"]
        engagement_rate = creator["avg_engagement_rate"] / 100

        num_posts = random.randint(*POSTS_PER_CREATOR)

        for _ in range(num_posts):
            lo, hi  = REACH_MULTIPLIER[platform]
            reach   = int(followers * random.uniform(lo, hi))
            views   = int(reach * random.uniform(0.8, 1.0))

            total_eng = int(reach * engagement_rate)
            likes     = int(total_eng * random.uniform(0.80, 0.90))
            comments  = int(total_eng * random.uniform(0.07, 0.13))
            shares    = max(total_eng - likes - comments, 0)
            clicks    = int(likes * random.uniform(0.05, 0.15))

            campaigns_for_creator = creator_campaigns.get(int(creator_id), [])
            if campaigns_for_creator and random.random() < 0.70:
                campaign_id = random.choice(campaigns_for_creator)
            else:
                campaign_id = None

            rows.append({
                "post_id":        post_id,
                "creator_id":     creator_id,
                "campaign_id":    campaign_id,
                "platform":       platform,
                "content_format": random.choice(CONTENT_FORMATS),
                "likes":          likes,
                "comments":       comments,
                "shares":         shares,
                "views":          views,
                "clicks":         clicks,
                "reach":          reach,
                "posted_at":      fake.date_time_between(
                                      start_date="-1y", end_date="now"
                                  ),
            })
            post_id += 1

    return pd.DataFrame(rows)


if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)

    creators_df          = pd.read_csv(os.path.join(DATA_DIR, "creators.csv"))
    campaign_creators_df = pd.read_csv(os.path.join(DATA_DIR, "campaign_creators.csv"))

    posts_df = generate_posts(creators_df, campaign_creators_df)

    print("Shape:", posts_df.shape)
    print()

    orphan_c = ~posts_df["creator_id"].isin(creators_df["creator_id"])
    print("Orphan creator refs:", orphan_c.sum(), "(should be 0)")

    valid_ids   = set(campaign_creators_df["campaign_id"].unique())
    has_camp    = posts_df["campaign_id"].notna()
    orphan_camp = has_camp & ~posts_df.loc[has_camp, "campaign_id"].isin(valid_ids)
    print("Orphan campaign refs:", orphan_camp.sum(), "(should be 0)")
    print()

    pct_organic = posts_df["campaign_id"].isna().mean() * 100
    print(f"Organic posts: {pct_organic:.1f}%")
    print()

    posts_df["computed_er"] = (
        (posts_df["likes"] + posts_df["comments"] + posts_df["shares"])
        / posts_df["reach"] * 100
    )
    merged = posts_df.merge(
        creators_df[["creator_id", "avg_engagement_rate"]], on="creator_id"
    )
    comparison = merged.groupby("creator_id").agg(
        stated_er=("avg_engagement_rate", "first"),
        actual_er=("computed_er", "mean"),
    ).head(5)
    print("Stated vs actual engagement rate (first 5 creators):")
    print(comparison)

    posts_df = posts_df.drop(columns=["computed_er"])
    posts_df["campaign_id"] = posts_df["campaign_id"].astype("Int64")
    out = os.path.join(DATA_DIR, "posts.csv")
    posts_df.to_csv(out, index=False)
    print(f"\nSaved to {out}")