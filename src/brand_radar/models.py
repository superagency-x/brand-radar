"""Data models for Brand Radar marketing intelligence."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class AdCreative:
    brand: str
    ad_id: str
    platforms: list[str]
    format: str  # video, static_image, carousel, reel
    status: str  # active, inactive_historical
    first_seen_date: str
    last_seen_date: str
    flight_days: int
    headline: str
    body_copy: str
    hook_angle: str  # energy_savings, dual_zone_sync, healthy_low_fat, space_saving, easy_cleaning, price_cut
    target_sku: str
    cta_text: str
    landing_page_url: str
    destination_type: str  # d2c_shop, amazon, retailer_partner
    estimated_impressions_tier: str  # < 50k, 50k - 250k, 250k - 1M, > 1M
    estimated_spend_eur: float
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchFootprint:
    brand: str
    keyword: str
    search_type: str  # paid_text_ad, google_shopping_pla, organic_serp, featured_snippet
    status: str  # active, last_12m
    rank: int
    title: str
    snippet: str
    display_url: str
    target_url: str
    has_sitelinks: bool = False
    price_shown: Optional[float] = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class AffiliateDeal:
    brand: str
    deal_id: str
    title: str
    merchant: str
    deal_price_eur: float
    original_price_eur: float
    discount_pct: float
    temperature_deg: int
    voucher_code: Optional[str]
    deal_url: str
    affiliate_network: str
    date_posted: str
    status: str  # active, expired_historical
    comments_count: int = 0
    creator_collaborator: Optional[str] = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class PRRelease:
    brand: str
    release_id: str
    title: str
    summary: str
    publisher_source: str  # Presseportal, Firmenpresse, Stiftung Warentest, CHIP, FAZ
    category: str  # product_launch, award_test_win, corporate_expansion, campaign_launch
    date: str
    status: str  # active_campaign, historical_12m
    url: str
    key_spokesperson: Optional[str] = None
    sentiment: str = "positive"
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class RetailActivation:
    brand: str
    retailer: str  # MediaMarkt, Otto, Amazon, Saturn
    activation_type: str  # brand_store_hub, flyer_frontpage, bundle_deal, prime_day_spotlight, exclusive_color_sku
    title: str
    headline_claim: str
    status: str  # active, seasonal_flight_12m
    period: str
    details: str
    url: Optional[str] = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class MediaSpendSummary:
    brand: str
    timeframe: str  # currently_active, trailing_12m
    total_estimated_spend_eur: float
    spend_band_low_eur: float
    spend_band_high_eur: float
    channel_breakdown_pct: dict[str, float]  # {Meta: 42.0, Google_Search: 28.0, ...}
    monthly_trend: list[dict[str, Any]]
