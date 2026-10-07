"""Export marketing intelligence bundles and C-level executive markdown reports."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def build_marketing_dossier_markdown(dossier: dict[str, Any]) -> str:
    """Generate professional executive markdown dossier for German market."""
    brands = dossier["brands_metadata"]
    spend = dossier["media_spend"]
    ads = dossier["meta_ads"]
    aff = dossier["affiliates"]["by_brand"]
    pr = dossier["pr_coverage"]["by_brand"]
    ret = dossier["retail_activations"]["by_brand"]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    lines = [
        "# German Air Fryer Brand Marketing Intelligence Dossier",
        "**Market**: Germany (DE) | **Focus Brands**: SharkNinja · Cosori · Philips · Tefal",
        f"**Snapshot Date**: {today} | **Scope**: Currently Active & Trailing 12-Month Performance",
        "",
        "---",
        "",
        "## 1. Executive Summary & GTM Positioning Takeaways",
        "",
    ]

    for ins in dossier.get("insights", []):
        b_name = brands.get(ins["brand"], {}).get("name", ins["brand"])
        lines.append(f"- **{b_name}**: {ins['text']}")

    lines.extend([
        "",
        "---",
        "",
        "## 2. Modeled Media Investments & Channel Mix (Germany)",
        "*Estimations based on verified ad flights, creative volume, active search bids, and DACH benchmarks*",
        "",
        "### Trailing 12-Month Investment Estimates (EUR)",
        "| Brand | Entity DACH | Est. 12M Media Spend | Range (Low – High) | Primary Channel Split |",
        "|---|---|---|---|---|",
    ])

    for b, data in spend.items():
        b_info = brands.get(b, {})
        t12 = data["trailing_12m"]
        split = ", ".join(f"{k}: {v}%" for k, v in list(t12["channel_breakdown_pct"].items())[:2])
        lines.append(
            f"| **{b_info.get('name', b)}** | {b_info.get('corporate_name', '–')} | "
            f"**€{t12['total_estimated_spend_eur']:,.0f}** | €{t12['spend_band_low_eur']:,.0f} – €{t12['spend_band_high_eur']:,.0f} | {split} |"
        )

    lines.extend([
        "",
        "### Currently Active Monthly Run-Rate (EUR)",
        "| Brand | Active Monthly Spend | Range (Low – High) | Active Ad Formats | Primary Hook Angle |",
        "|---|---|---|---|---|",
    ])

    for b, data in spend.items():
        b_info = brands.get(b, {})
        act = data["currently_active"]
        top_hook = "–"
        b_hooks = ads["active"]["hooks_by_brand"].get(b, {})
        if b_hooks:
            top_hook = max(b_hooks, key=b_hooks.get).replace("_", " ").title()
        formats = ", ".join(ads["active"]["formats_by_brand"].get(b, {}).keys()) or "–"
        lines.append(
            f"| **{b_info.get('name', b)}** | **€{act['total_estimated_spend_eur']:,.0f}** | "
            f"€{act['spend_band_low_eur']:,.0f} – €{act['spend_band_high_eur']:,.0f} | {formats} | `{top_hook}` |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 3. Meta Ad Library: Creative Strategy & Messaging Hooks",
        "",
        "### Active Ad Creative Breakdown (Facebook & Instagram in Germany)",
        "| Brand | Active Campaigns | Lead Creative Format | Core Value Proposition Hook | Target Destination |",
        "|---|---|---|---|---|",
    ])

    for b in brands:
        b_info = brands[b]
        b_raw = [a for a in ads["raw_active"] if a["brand"] == b]
        lead_fmt = b_raw[0]["format"].title() if b_raw else "–"
        lead_hook = b_raw[0]["hook_angle"].replace("_", " ").title() if b_raw else "–"
        lead_dest = b_raw[0]["destination_type"].replace("_", " ").title() if b_raw else "–"
        lines.append(
            f"| **{b_info['name']}** | {len(b_raw)} active ads | {lead_fmt} | `{lead_hook}` | {lead_dest} |"
        )

    lines.extend([
        "",
        "### Trailing 12-Month Creative Hooks & Angle Ownership",
        "- **SharkNinja**: Leads with *Space Saving* (DoubleStack XL vertical form factor) and *Dual-Zone Sync*. Heavy video & reel focus with direct CTA to D2C shop (`ninjakitchen.de`).",
        "- **Cosori**: Owns *Smart Ecosystem* & *360 ThermoIQ* (Dual Blaze). Leans heavily into recipe creators and Amazon D2C store checkout.",
        "- **Philips**: Anchors on *Healthy Low-Fat* (Rapid Air heritage) and *Precision Cooking* (Combi 7000 thermoprobe). Dual destination strategy (D2C + MediaMarkt retail co-op).",
        "- **Tefal**: Differentiates on *Cast-Aluminum Grill Plate* & *2-in-1 Versatility*. Heavy co-promotions with Otto.de and MediaMarkt.",
        "",
        "---",
        "",
        "## 4. Google Search & SEM Footprint in Germany",
        "",
        "| Brand | Paid Ads Presence | Shopping (PLA) Presence | Core Generic Intercepts | Top Organic Rankings |",
        "|---|---|---|---|---|",
    ])

    for b, b_data in dossier["search_footprint"]["by_brand"].items():
        b_info = brands.get(b, {})
        lines.append(
            f"| **{b_info.get('name', b)}** | {b_data['paid_ads_count']} active bids | {b_data['shopping_pla_count']} active PLAs | "
            f"`{', '.join(b_data['keywords'][:2])}` | {b_data['organic_top3_count']} top-3 positions |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 5. Affiliate, Community Deals & Creator Footprint",
        "",
        "| Brand | Deal Temperature (° Heat) | Avg Deal Discount % | Detected Affiliate Networks | Top Voucher Codes |",
        "|---|---|---|---|---|",
    ])

    for b, b_data in aff.items():
        b_info = brands.get(b, {})
        vouchers = ", ".join(f"`{v}`" for v in b_data["top_vouchers"]) if b_data["top_vouchers"] else "None"
        nets = ", ".join(b_data["networks"][:2])
        lines.append(
            f"| **{b_info.get('name', b)}** | **{b_data['avg_temperature_deg']}°** | "
            f"-{b_data['avg_discount_pct']}% | {nets} | {vouchers} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 6. PR, Editorial Testing & E-Retailer Activations",
        "",
        "### Key PR Wins & Certified Editorial Test Grades",
        "| Brand | Verified PR Releases | Certified Test Awards | Lead Press Angle | Primary German Media Source |",
        "|---|---|---|---|---|",
    ])

    for b, b_data in pr.items():
        b_info = brands.get(b, {})
        lead_prs = [r for r in dossier["pr_coverage"]["raw"] if r["brand"] == b]
        src = lead_prs[0]["publisher_source"] if lead_prs else "–"
        lines.append(
            f"| **{b_info.get('name', b)}** | {b_data['releases_count']} releases | "
            f"{b_data['award_wins']} test wins | {b_data['latest_headline'][:45]}... | {src} |"
        )

    lines.extend([
        "",
        "### Major E-Retailer Collaborations (MediaMarkt, Otto, Amazon)",
        "| Brand | Key E-Retailer Collaborations | Activation Formats | Highlight Campaign |",
        "|---|---|---|---|",
    ])

    for b, b_data in ret.items():
        b_info = brands.get(b, {})
        ret_list = ", ".join(b_data["retailers"])
        lines.append(
            f"| **{b_info.get('name', b)}** | {ret_list} | "
            f"Brand Stores, Bundle Packs, Prospekt Einbindungen | {b_data['lead_campaign'][:50]} |"
        )

    lines.extend([
        "",
        "---",
        f"*Generated automatically by Brand Radar v1.0.0 · Author: Berk Saraloğlu*",
    ])

    return "\n".join(lines)


def export_bundle(dossier: dict[str, Any], site_dir: Path, exports_dir: Path) -> tuple[Path, Path, Path]:
    """Write radar.json, markdown dossier, and HTML brief."""
    site_dir.mkdir(parents=True, exist_ok=True)
    exports_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 1. Dashboard JSON
    json_path = site_dir / "data" / "radar.json"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(dossier, indent=2, ensure_ascii=False), encoding="utf-8")

    # 2. Markdown Executive Dossier
    md_content = build_marketing_dossier_markdown(dossier)
    md_path = exports_dir / f"marketing_intel_{today}.md"
    md_path.write_text(md_content, encoding="utf-8")

    # 3. Standalone HTML Dossier
    html_content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Marketing Intelligence Dossier · Germany Air Fryer Category</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; max-width: 980px; margin: 40px auto; padding: 0 24px; color: #1c2024; background: #fff; }}
    h1 {{ color: #0f172a; border-bottom: 2px solid #2f6fed; padding-bottom: 8px; }}
    h2 {{ color: #1e293b; margin-top: 32px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; }}
    h3 {{ color: #334155; margin-top: 24px; }}
    table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; }}
    th, td {{ border: 1px solid #cbd5e1; padding: 8px 12px; text-align: left; }}
    th {{ background: #f8fafc; font-weight: 600; color: #334155; }}
    tr:nth-child(even) {{ background: #f8fafc; }}
    strong {{ color: #0f172a; }}
    hr {{ border: 0; border-top: 1px solid #e2e8f0; margin: 24px 0; }}
    code {{ background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 13px; font-family: ui-monospace, Menlo, monospace; }}
    @media print {{ body {{ max-width: 100%; margin: 0; padding: 12mm; }} }}
  </style>
</head>
<body>
<div style="background:#f1f5f9;border-left:4px solid #2f6fed;padding:12px 16px;margin-bottom:24px;">
  <strong>CONFIDENTIAL // FOR EXECUTIVE REVIEW:</strong> German Air Fryer Brand Intelligence Dossier (Ninja · Cosori · Philips · Tefal)
</div>
<pre style="white-space: pre-wrap; font-family: inherit;">{md_content}</pre>
</body>
</html>"""

    html_path = exports_dir / f"marketing_intel_{today}.html"
    html_path.write_text(html_content, encoding="utf-8")

    return json_path, md_path, html_path
