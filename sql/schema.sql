-- ============================================================
-- CreatorIQ — AI-Powered Creator Marketing Analytics Platform
-- Schema: schema.sql
-- Order matters: tables created in dependency order
-- ============================================================

CREATE TABLE brands (
  brand_id        SERIAL PRIMARY KEY,
  brand_name      VARCHAR(150) NOT NULL,
  industry        VARCHAR(100),
  target_segment  VARCHAR(100),
  country         VARCHAR(100),
  created_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE creators (
  creator_id           SERIAL PRIMARY KEY,
  name                 VARCHAR(200) NOT NULL,
  handle               VARCHAR(100) UNIQUE NOT NULL,
  platform             VARCHAR(50) CHECK (platform IN ('instagram','youtube','tiktok','twitter')),
  niche                VARCHAR(100),
  tier                 VARCHAR(20) CHECK (tier IN ('nano','micro','macro','mega')),
  follower_count       INTEGER DEFAULT 0,
  avg_engagement_rate  NUMERIC(5,2),
  country              VARCHAR(100),
  audience_authenticity_score NUMERIC(4,2),
  joined_date          DATE,
  created_at           TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_creators_platform ON creators(platform);
CREATE INDEX idx_creators_tier ON creators(tier);

CREATE TABLE campaigns (
  campaign_id    SERIAL PRIMARY KEY,
  brand_id       INTEGER NOT NULL REFERENCES brands(brand_id) ON DELETE CASCADE,
  campaign_name  VARCHAR(200) NOT NULL,
  objective      VARCHAR(50) CHECK (objective IN ('awareness','engagement','conversion','retention')),
  start_date     DATE NOT NULL,
  end_date       DATE NOT NULL,
  total_budget   NUMERIC(12,2) NOT NULL,
  status         VARCHAR(20) CHECK (status IN ('draft','active','completed','paused')),
  created_at     TIMESTAMP DEFAULT NOW(),
  CONSTRAINT chk_dates CHECK (end_date > start_date)
);

CREATE TABLE campaign_creators (
  cc_id                 SERIAL PRIMARY KEY,
  campaign_id           INTEGER NOT NULL REFERENCES campaigns(campaign_id) ON DELETE CASCADE,
  creator_id            INTEGER NOT NULL REFERENCES creators(creator_id) ON DELETE CASCADE,
  creator_fee           NUMERIC(10,2),
  revenue_attributed    NUMERIC(12,2) DEFAULT 0,
  impressions_delivered BIGINT DEFAULT 0,
  promo_code            VARCHAR(50) UNIQUE,
  status                VARCHAR(20) CHECK (status IN ('invited','confirmed','active','completed')),
  created_at            TIMESTAMP DEFAULT NOW(),
  CONSTRAINT uq_campaign_creator UNIQUE(campaign_id, creator_id)
);

CREATE TABLE posts (
  post_id        SERIAL PRIMARY KEY,
  creator_id     INTEGER NOT NULL REFERENCES creators(creator_id),
  campaign_id    INTEGER REFERENCES campaigns(campaign_id),
  platform       VARCHAR(50) CHECK (platform IN ('instagram','youtube','tiktok','twitter')),
  content_format VARCHAR(50) CHECK (content_format IN ('reel','short','story','video','image','carousel')),
  likes          INTEGER DEFAULT 0,
  comments       INTEGER DEFAULT 0,
  shares         INTEGER DEFAULT 0,
  views          BIGINT DEFAULT 0,
  clicks         INTEGER DEFAULT 0,
  reach          BIGINT DEFAULT 0,
  posted_at      TIMESTAMP NOT NULL,
  created_at     TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_posts_creator ON posts(creator_id);
CREATE INDEX idx_posts_campaign ON posts(campaign_id);
CREATE INDEX idx_posts_platform_format ON posts(platform, content_format);

CREATE TABLE conversions (
  conversion_id  SERIAL PRIMARY KEY,
  post_id        INTEGER REFERENCES posts(post_id),
  campaign_id    INTEGER REFERENCES campaigns(campaign_id),
  order_value    NUMERIC(10,2) NOT NULL CHECK (order_value > 0),
  promo_code     VARCHAR(50),
  age_group      VARCHAR(20) CHECK (age_group IN ('13-17','18-24','25-34','35-44','45-54','55+')),
  gender         VARCHAR(20),
  location       VARCHAR(100),
  device_type    VARCHAR(30) CHECK (device_type IN ('mobile','desktop','tablet')),
  converted_at   TIMESTAMP NOT NULL
);

CREATE INDEX idx_conv_campaign ON conversions(campaign_id);
CREATE INDEX idx_conv_promo ON conversions(promo_code);

CREATE TABLE audience_demographics (
  demo_id           SERIAL PRIMARY KEY,
  creator_id        INTEGER NOT NULL REFERENCES creators(creator_id) ON DELETE CASCADE,
  age_group         VARCHAR(20) CHECK (age_group IN ('13-17','18-24','25-34','35-44','45-54','55+')),
  gender            VARCHAR(20),
  country           VARCHAR(100),
  interest_category VARCHAR(100),
  percentage_share  NUMERIC(5,2) CHECK (percentage_share BETWEEN 0 AND 100),
  recorded_at       DATE NOT NULL
);

CREATE INDEX idx_demo_creator ON audience_demographics(creator_id);