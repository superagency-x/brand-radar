"""DACH Media Spend Estimation Engine (Meta, Google SEM, Retail Media, Affiliates)."""
from __future__ import annotations

from typing import Any
from ..models import AdCreative, AffiliateDeal, MediaSpendSummary, SearchFootprint

# DACH Media economics modeling
MONTHS_12 = [
    "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04",
    "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10",
]

# Seasonality multipliers in Germany for small domestic appliances (Home & Kitchen)
# Peak in Nov/Dec (Black Week, Christmas), secondary peak in July (Prime Day), low in Feb/May.
SEASONALITY_WEIGHTS = {
    "2025-11": 2.2,  # Black Week
    "2025-12": 1.9,  # Christmas gift shopping
    "2026-01": 0.8,  # Post-holiday dip / New year fitness
    "2026-02": 0.6,
    "2026-03": 0.9,  # Spring / Easter deals
    "2026-04": 0.8,
    "2026-05": 0.7,
    "2026-06": 0.8,
    "2026-07": 1.4,  # Prime Day surge
    "2026-08": 0.9,  # Pre-IFA preparations
    "2026-09": 1.3,  # IFA Berlin product launches
    "2026-10": 1.5,  # Q4 ramp-up / Prime Big Deal Days
}


def estimate_brand_media_spend(
    brand_id: str,
    ads: list[AdCreative],
    searches: list[SearchFootprint],
    deals: list[AffiliateDeal],
    benchmarks: dict[str, Any],
) -> dict[str, MediaSpendSummary]:
    """Calculate modeled media investments for a brand (Currently Active vs Trailing 12 Months)."""
    # 1. Meta Ads spend
    active_meta = sum(a.estimated_spend_eur for a in ads if a.status == "active")
    total_meta_12m = sum(a.estimated_spend_eur for a in ads)

    # 2. Google Search & Shopping spend estimation
    brand_searches = [s for s in searches if s.brand == brand_id]
    cpc_search = float(benchmarks.get("google_search_cpc_eur", 1.45))
    cpc_pla = float(benchmarks.get("google_shopping_cpc_eur", 0.65))

    paid_keywords = [s for s in brand_searches if s.search_type == "paid_text_ad"]
    pla_keywords = [s for s in brand_searches if s.search_type == "google_shopping_pla"]

    # Active monthly Google search run-rate
    active_search_monthly = (len(paid_keywords) * 1800 * cpc_search) + (len(pla_keywords) * 2400 * cpc_pla)
    total_search_12m = active_search_monthly * 12 * 0.9  # Adjusted for seasonal flights

    # 3. Retail Media (Amazon Sponsored Ads / MediaMarkt Retail Media)
    # Scaled to brand size in the German market
    retail_media_mult = 1.35 if brand_id in ("ninja", "philips") else 1.15
    active_retail_media = (active_meta * 0.35 + active_search_monthly * 0.4) * retail_media_mult
    total_retail_media_12m = active_retail_media * 12 * 0.95

    # 4. Affiliate commissions & publisher incentives
    brand_deals = [d for d in deals if d.brand == brand_id]
    aff_active = sum(d.deal_price_eur * (d.temperature_deg / 100) * 0.065 for d in brand_deals if d.status == "active")
    aff_12m = sum(d.deal_price_eur * (d.temperature_deg / 100) * 0.065 for d in brand_deals)

    # Combine totals
    active_total = active_meta + active_search_monthly + active_retail_media + aff_active
    total_12m = total_meta_12m + total_search_12m + total_retail_media_12m + aff_12m

    # Channel breakdowns
    def calc_breakdown(meta: float, sem: float, ret: float, aff: float) -> dict[str, float]:
        tot = meta + sem + ret + aff
        if tot <= 0:
            return {"Meta Ads": 25.0, "Google Search": 25.0, "Retail Media": 25.0, "Affiliates": 25.0}
        return {
            "Meta Ads": round(100 * meta / tot, 1),
            "Google Search & Shopping": round(100 * sem / tot, 1),
            "Retail Media (Amazon/MMS)": round(100 * ret / tot, 1),
            "Affiliate & Deal Payouts": round(100 * aff / tot, 1),
        }

    active_breakdown = calc_breakdown(active_meta, active_search_monthly, active_retail_media, aff_active)
    total_breakdown = calc_breakdown(total_meta_12m, total_search_12m, total_retail_media_12m, aff_12m)

    # Monthly trends distribution for the last 12 months based on seasonality
    monthly_trend = []
    base_month = total_12m / sum(SEASONALITY_WEIGHTS.values())
    for ym in MONTHS_12:
        weight = SEASONALITY_WEIGHTS.get(ym, 1.0)
        m_spend = round(base_month * weight, 0)
        campaign = (
            "Black Week & Cyber Monday Offensive" if ym == "2025-11" else
            "Weihnachts-Geschenke Endspurt" if ym == "2025-12" else
            "Gesunder Jahresstart / Neujahrsvorsätze" if ym == "2026-01" else
            "Oster-Angebote & Frühlings-Backen" if ym in ("2026-03", "2026-04") else
            "Amazon Prime Day Spotlight" if ym == "2026-07" else
            "IFA Berlin Neuheiten-Präsentation" if ym == "2026-09" else
            "Q4 Kampagnen-Warmup" if ym == "2026-10" else
            "Alltägliches Performance Marketing"
        )
        monthly_trend.append({
            "month": ym,
            "estimated_spend_eur": m_spend,
            "campaign_focus": campaign,
        })

    return {
        "currently_active": MediaSpendSummary(
            brand=brand_id,
            timeframe="currently_active",
            total_estimated_spend_eur=round(active_total, 0),
            spend_band_low_eur=round(active_total * 0.85, 0),
            spend_band_high_eur=round(active_total * 1.20, 0),
            channel_breakdown_pct=active_breakdown,
            monthly_trend=[],
        ),
        "trailing_12m": MediaSpendSummary(
            brand=brand_id,
            timeframe="trailing_12m",
            total_estimated_spend_eur=round(total_12m, 0),
            spend_band_low_eur=round(total_12m * 0.85, 0),
            spend_band_high_eur=round(total_12m * 1.25, 0),
            channel_breakdown_pct=total_breakdown,
            monthly_trend=monthly_trend,
        ),
    }
