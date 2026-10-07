# Brand Radar: German Airfryer Marketing Intelligence

An automated competitive intelligence suite and GTM marketing mix analyzer tracking the German small domestic appliances (SDA) airfryer category across **SharkNinja**, **Cosori**, **Philips**, and **Tefal**.

Designed as a high-signal marketing portfolio project demonstrating end-to-end category understanding, multi-channel intelligence ingestion, and econometric media modeling for the German / DACH market.

---

## 🧭 The 6 Marketing Intelligence Vectors

Brand Radar unifies fragmented competitor signals across two distinct temporal horizons: **Currently Active Flights** and **Trailing 12-Month Historical Archive**.

| Vector | Focus Areas | German Market Nuance |
| :--- | :--- | :--- |
| **Meta Ad Library** | Video hooks, Reels (9:16), Carousels, Static copy | Hooks: *Platzsparend*, *Zwei Zonen*, *Strom sparen*. Destination: D2C vs. Retail vs. Amazon |
| **Google SEM & SERP** | Paid text ads, Google Shopping (PLA) bids, Organic category rankings | High-intent queries: `heißluftfritteuse test`, `airfryer doppelkammer`, conquesting bids |
| **Affiliate & Community** | Deal heat ratings (°), historical *Bestpreis* records, voucher codes | MyDealz community heat, Awin affiliate networks, Amazon Associates tags |
| **Modeled Media Spend** | Multi-channel media investment breakdown & 12-month seasonality curves | Modeled DACH CPM/CPC econometric proxies; seasonality curves (Black Week, IFA Berlin, Easter) |
| **PR & Editorial Tests** | Press wire distributions & independent German testing accolades | *Stiftung Warentest* (*GUT* ratings), *ETM Testmagazin*, *Presseportal.de* releases |
| **E-Retailer Co-Ops** | Brand Store takeovers, flyer circular frontpages, exclusive SKUs | *MediaMarkt / Saturn* Club Days, *Otto.de* Tech Flyer & Otto Up perks, Amazon Prime Day |

---

## 🏗️ Architecture & Project Structure

```
brand-radar/
├── config/
│   └── brands.yaml             # Target brand metadata, SKUs, and DACH benchmark constants
├── src/brand_radar/
│   ├── scrapers/               # Intelligence collectors across 6 marketing pillars
│   │   ├── meta_ads.py         # Meta Ad Library creative analyzer
│   │   ├── google_sem.py       # Google Search & Shopping PLA footprint
│   │   ├── affiliates.py       # MyDealz deal heat & voucher tracker
│   │   ├── pr_news.py          # Presseportal & Stiftung Warentest indexer
│   │   └── retail_collabs.py   # MediaMarkt, Otto & Amazon retail co-ops
│   ├── analytics/
│   │   ├── spend_model.py      # DACH econometric media spend model
│   │   └── competitive.py      # Cross-brand benchmarking & GTM insights
│   ├── store.py                # SQLite database persistence layer
│   ├── models.py               # Pydantic / dataclass intelligence models
│   ├── export.py               # Markdown executive brief & HTML report generator
│   └── cli.py                  # CLI engine (`run`, `report`, `serve`)
├── site/                       # Interactive web dashboard (HTML5 / Vanilla CSS / Chart.js)
│   ├── index.html              # Filter by Brand & Horizon (Active vs. 1-Year)
│   ├── app.js                  # Dynamic charts & data rendering
│   └── data/radar.json         # Compiled pipeline intelligence feed
└── scripts/
    ├── run_radar.command       # One-click interactive runner for macOS Terminal
    └── make_icon.py            # Native macOS Retina AppIcon generator
```

---

## ⚡ Quickstart

### Prerequisites
- Python 3.12+ (or [uv](https://github.com/astral-sh/uv))

### Installation & Execution

```bash
# Clone the repository
git clone https://github.com/superagency-x/brand-radar.git
cd brand-radar

# 1. Run full scraper pipeline & compile intelligence dossier
uv run brand-radar run

# 2. View executive C-level briefing in terminal
uv run brand-radar report

# 3. Launch interactive web dashboard
uv run brand-radar serve --port 8080
```

### macOS Desktop Application
The project includes a ready-to-run native desktop bundle:
- Double-click `Brand Radar.app` or `Run Brand Radar.command` on macOS to execute the intelligence pipeline and automatically open the interactive dashboard in your browser.

---

## 📈 Methodology & Data Integrity
- **Media Spend Modeling**: In line with DACH media agency practice, media spend is calculated as an econometric proxy based on verified active flight volume, flight duration, and regional benchmark constants (DACH Video CPM €18–€26, SEM CPC €1.85, Retail Media CPM €32).
- **Independent Testing**: Certified German test awards strictly preserve authentic editorial assessments (*Stiftung Warentest*, *ETM Testmagazin*).
