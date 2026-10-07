"""Competitive intelligence aggregator and cross-brand benchmarking."""
from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any
from ..models import AdCreative, AffiliateDeal, PRRelease, RetailActivation, SearchFootprint
from .spend_model import estimate_brand_media_spend


def generate_competitive_dossier(
    brands_cfg: dict[str, Any],
    benchmarks: dict[str, Any],
    ads: list[AdCreative],
    searches: list[SearchFootprint],
    deals: list[AffiliateDeal],
    releases: list[PRRelease],
    activations: list[RetailActivation],
) -> dict[str, Any]:
    """Compile comprehensive cross-brand marketing intelligence dossier for Germany."""
    brand_keys = list(brands_cfg.keys())

    # 1. Spend modeling per brand
    spend_by_brand = {}
    for b in brand_keys:
        b_ads = [a for a in ads if a.brand == b]
        b_searches = [s for s in searches if s.brand == b]
        b_deals = [d for d in deals if d.brand == b]
        spend_by_brand[b] = estimate_brand_media_spend(b, b_ads, b_searches, b_deals, benchmarks)

    # 2. Meta Ads breakdown
    def analyze_ads(ad_list: list[AdCreative]):
        by_brand = defaultdict(list)
        for a in ad_list:
            by_brand[a.brand].append(a)

        formats_by_brand = {}
        hooks_by_brand = {}
        dest_by_brand = {}

        for b in brand_keys:
            items = by_brand[b]
            formats_by_brand[b] = dict(Counter(a.format for a in items))
            hooks_by_brand[b] = dict(Counter(a.hook_angle for a in items))
            dest_by_brand[b] = dict(Counter(a.destination_type for a in items))

        return {
            "total_count": len(ad_list),
            "formats_by_brand": formats_by_brand,
            "hooks_by_brand": hooks_by_brand,
            "destinations_by_brand": dest_by_brand,
        }

    ads_active = [a for a in ads if a.status == "active"]
    ads_12m = ads

    # 3. Search & SEO / Paid SEM breakdown
    search_by_brand = {}
    for b in brand_keys:
        b_items = [s for s in searches if s.brand == b]
        search_by_brand[b] = {
            "paid_ads_count": sum(1 for s in b_items if s.search_type == "paid_text_ad"),
            "shopping_pla_count": sum(1 for s in b_items if s.search_type == "google_shopping_pla"),
            "organic_top3_count": sum(1 for s in b_items if s.search_type == "organic_serp" and s.rank <= 3),
            "keywords": [s.keyword for s in b_items],
        }

    # 4. Affiliate community breakdown
    affiliates_by_brand = {}
    for b in brand_keys:
        b_deals = [d for d in deals if d.brand == b]
        active_deals = [d for d in b_deals if d.status == "active"]
        avg_temp = round(sum(d.temperature_deg for d in b_deals) / len(b_deals), 1) if b_deals else 0
        avg_disc = round(sum(d.discount_pct for d in b_deals) / len(b_deals), 1) if b_deals else 0
        vouchers = [d.voucher_code for d in b_deals if d.voucher_code]
        affiliates_by_brand[b] = {
            "active_deals_count": len(active_deals),
            "total_deals_12m": len(b_deals),
            "avg_temperature_deg": avg_temp,
            "avg_discount_pct": avg_disc,
            "top_vouchers": vouchers[:3],
            "merchants": list({d.merchant for d in b_deals}),
            "networks": list({d.affiliate_network for d in b_deals}),
        }

    # 5. PR & Editorial test coverage
    pr_by_brand = {}
    for b in brand_keys:
        b_prs = [r for r in releases if r.brand == b]
        pr_by_brand[b] = {
            "releases_count": len(b_prs),
            "categories": dict(Counter(r.category for r in b_prs)),
            "award_wins": sum(1 for r in b_prs if r.category == "award_test_win"),
            "latest_headline": b_prs[0].title if b_prs else "–",
        }

    # 6. Retail & E-Retailer activations
    retail_by_brand = {}
    for b in brand_keys:
        b_acts = [a for a in activations if a.brand == b]
        retail_by_brand[b] = {
            "activations_count": len(b_acts),
            "retailers": list({a.retailer for a in b_acts}),
            "types": dict(Counter(a.activation_type for a in b_acts)),
            "lead_campaign": b_acts[0].title if b_acts else "–",
        }

    # 7. Strategic Executive Insights
    insights = [
        {
            "brand": "ninja",
            "topic": "Strategy & Channels",
            "text": "SharkNinja leads creative velocity in Germany, aggressively pushing vertical space-saving (DoubleStack XL) and cross-channel D2C traffic with high-frequency Meta video and search conquesting.",
        },
        {
            "brand": "cosori",
            "topic": "Strategy & Channels",
            "text": "Cosori dominates Amazon e-retail media and tech-savvy digital native channels; heavy reliance on VeSync smart-app ecosystem and creator recipe reels over traditional retail PR.",
        },
        {
            "brand": "philips",
            "topic": "Strategy & Channels",
            "text": "Philips (Versuni) leverages deep Stiftung Warentest heritage and premium Combi 7000 thermoprobe tech; maintains heavy TVC-style digital investments and top-tier MediaMarkt Club co-ops.",
        },
        {
            "brand": "tefal",
            "topic": "Strategy & Channels",
            "text": "Tefal (Groupe SEB) owns the 2-in-1 'Grill & Airfry' position in Germany, leveraging cast-aluminum grill plate claims and strong promotional presence across Otto and MediaMarkt.",
        },
    ]

    return {
        "brands": brand_keys,
        "brands_metadata": brands_cfg,
        "media_spend": {
            b: {
                "currently_active": spend_by_brand[b]["currently_active"].__dict__,
                "trailing_12m": spend_by_brand[b]["trailing_12m"].__dict__,
            }
            for b in brand_keys
        },
        "meta_ads": {
            "active": analyze_ads(ads_active),
            "trailing_12m": analyze_ads(ads_12m),
            "raw_active": [a.__dict__ for a in ads_active],
            "raw_12m": [a.__dict__ for a in ads_12m],
        },
        "search_footprint": {
            "by_brand": search_by_brand,
            "raw": [s.__dict__ for s in searches],
        },
        "affiliates": {
            "by_brand": affiliates_by_brand,
            "raw": [d.__dict__ for d in deals],
        },
        "pr_coverage": {
            "by_brand": pr_by_brand,
            "raw": [r.__dict__ for r in releases],
        },
        "retail_activations": {
            "by_brand": retail_by_brand,
            "raw": [a.__dict__ for a in activations],
        },
        "insights": insights,
    }
