"""Command-line interface for Brand Radar."""
from __future__ import annotations

import argparse
import http.server
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
import yaml

from .analytics.competitive import generate_competitive_dossier
from .export import export_bundle
from .scrapers.affiliates import collect_affiliate_deals
from .scrapers.google_sem import collect_search_footprint
from .scrapers.meta_ads import collect_meta_ads
from .scrapers.pr_news import collect_pr_releases
from .scrapers.retail_collabs import collect_retail_activations
from .store import BrandStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("brand_radar")


def load_config(cfg_path: Path) -> dict:
    return yaml.safe_load(cfg_path.read_text(encoding="utf-8"))


def cmd_run(args, cfg: dict) -> int:
    """Execute complete marketing intelligence retrieval across all 6 pillars."""
    data_dir = Path(args.data_dir)
    site_dir = Path(args.site_dir)
    store = BrandStore(data_dir / "radar.sqlite")

    started = datetime.now(timezone.utc)
    run_id = started.strftime("%Y%m%d-%H%M%S")
    snapshot_date = started.date().isoformat()
    store.start_run(run_id, snapshot_date, started.isoformat())

    print(f"\n▶ Executing Brand Radar Marketing Intelligence Pipeline (Run {run_id})")
    print(f"  Target Country: Germany (DE)")
    print(f"  Target Brands:  {', '.join(b['name'] for b in cfg['brands'].values())}\n")

    # 1. Meta Ad Library
    print("→ Scraping Meta Ad Library (Facebook & Instagram in Germany)...")
    ads = collect_meta_ads(cfg["brands"])
    store.save_meta_ads(run_id, ads)
    print(f"  ✔ {len(ads)} ad creatives catalogued (Active + Trailing 12M)")

    # 2. Google Search (Paid SEM & Organic SERPs)
    print("→ Scraping Google Germany (Paid Ads, Shopping PLAs & Organic Rankings)...")
    searches = collect_search_footprint(cfg["brands"])
    store.save_search(run_id, searches)
    print(f"  ✔ {len(searches)} search footprint data points captured")

    # 3. Affiliate & Deal Communities (MyDealz, Awin)
    print("→ Scraping German deal communities & affiliate networks (MyDealz, Awin)...")
    deals = collect_affiliate_deals(cfg["brands"])
    store.save_affiliates(run_id, deals)
    print(f"  ✔ {len(deals)} affiliate promotions & creator activations recorded")

    # 4. PR & Press Release Wires
    print("→ Scraping PR wires & certified editorial tests (Presseportal, Stiftung Warentest)...")
    releases = collect_pr_releases(cfg["brands"])
    store.save_pr(run_id, releases)
    print(f"  ✔ {len(releases)} press distributions & test awards indexed")

    # 5. E-Retailer Activations (MediaMarkt, Otto, Amazon)
    print("→ Scraping retail collaborations & brand store activations (MediaMarkt, Otto, Amazon)...")
    activations = collect_retail_activations(cfg["brands"])
    store.save_retail(run_id, activations)
    print(f"  ✔ {len(activations)} retail co-ops & brand store hubs verified")

    # 6. Analytics & Modeling
    print("\n→ Modeling DACH media spend investments & compiling competitive dossier...")
    benchmarks = cfg.get("dach_benchmarks", {})
    dossier = generate_competitive_dossier(
        brands_cfg=cfg["brands"],
        benchmarks=benchmarks,
        ads=ads,
        searches=searches,
        deals=deals,
        releases=releases,
        activations=activations,
    )

    counts = {
        "ads": len(ads),
        "search": len(searches),
        "affiliates": len(deals),
        "pr": len(releases),
        "retail": len(activations),
    }
    store.finish_run(run_id, datetime.now(timezone.utc).isoformat(), counts)
    store.close()

    # 7. Export outputs
    json_p, md_p, html_p = export_bundle(dossier, site_dir, data_dir / "exports")
    print(f"\n✔ Brand intelligence dossier successfully generated:")
    print(f"  Dashboard JSON  → {json_p}")
    print(f"  Executive Brief → {md_p}")
    print(f"  Printable HTML  → {html_p}\n")
    return 0


def cmd_report(args, cfg: dict) -> int:
    """Print the executive dossier to console and show file locations."""
    data_dir = Path(args.data_dir)
    site_dir = Path(args.site_dir)
    json_p = site_dir / "data" / "radar.json"
    if not json_p.exists():
        print("No exported dataset found. Running pipeline first...")
        cmd_run(args, cfg)

    dossier = json.loads(json_p.read_text(encoding="utf-8"))
    _, md_p, html_p = export_bundle(dossier, site_dir, data_dir / "exports")
    print(md_p.read_text(encoding="utf-8"))
    print(f"\n[Dossier Artifacts: {md_p} | {html_p}]")
    return 0


def cmd_serve(args, cfg: dict) -> int:
    """Serve the interactive dashboard locally."""
    site_dir = Path(args.site_dir)
    port = int(args.port)
    os.chdir(str(site_dir))
    handler = http.server.SimpleHTTPRequestHandler
    print(f"Brand Radar Server running at http://localhost:{port} (Press Ctrl+C to stop)")
    with http.server.HTTPServer(("127.0.0.1", port), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="brand-radar", description="Brand Marketing Intelligence Scraper")
    parser.add_argument("--config", default="config/brands.yaml", help="Path to brands YAML configuration")
    parser.add_argument("--data-dir", default="data", help="Directory for database and exports")
    parser.add_argument("--site-dir", default="site", help="Directory for dashboard assets")

    sub = parser.add_subparsers(dest="cmd", required=True)

    # run
    p_run = sub.add_parser("run", help="Execute complete marketing intelligence scraper")
    # report
    p_rep = sub.add_parser("report", help="Display executive marketing intelligence report")
    # serve
    p_srv = sub.add_parser("serve", help="Launch interactive web dashboard")
    p_srv.add_argument("--port", default=8000, help="Port to listen on (default: 8000)")

    args = parser.parse_args(argv)
    cfg = load_config(Path(args.config))

    if args.cmd == "run":
        return cmd_run(args, cfg)
    elif args.cmd == "report":
        return cmd_report(args, cfg)
    elif args.cmd == "serve":
        return cmd_serve(args, cfg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
