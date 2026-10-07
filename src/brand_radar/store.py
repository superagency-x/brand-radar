"""SQLite storage layer for Brand Radar."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Iterable, Optional

from .models import AdCreative, AffiliateDeal, PRRelease, RetailActivation, SearchFootprint

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY,
    snapshot_date TEXT NOT NULL,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    counts_json TEXT
);

CREATE TABLE IF NOT EXISTS meta_ads (
    run_id TEXT NOT NULL,
    brand TEXT NOT NULL,
    ad_id TEXT NOT NULL,
    platforms TEXT NOT NULL,
    format TEXT NOT NULL,
    status TEXT NOT NULL,
    first_seen_date TEXT,
    last_seen_date TEXT,
    flight_days INTEGER,
    headline TEXT,
    body_copy TEXT,
    hook_angle TEXT,
    target_sku TEXT,
    cta_text TEXT,
    landing_page_url TEXT,
    destination_type TEXT,
    estimated_impressions_tier TEXT,
    estimated_spend_eur REAL,
    extra TEXT NOT NULL DEFAULT '{}',
    PRIMARY KEY (run_id, brand, ad_id)
);

CREATE TABLE IF NOT EXISTS search_footprint (
    run_id TEXT NOT NULL,
    brand TEXT NOT NULL,
    keyword TEXT NOT NULL,
    search_type TEXT NOT NULL,
    status TEXT NOT NULL,
    rank INTEGER,
    title TEXT,
    snippet TEXT,
    display_url TEXT,
    target_url TEXT,
    has_sitelinks INTEGER DEFAULT 0,
    price_shown REAL,
    extra TEXT NOT NULL DEFAULT '{}',
    PRIMARY KEY (run_id, brand, keyword, search_type, rank)
);

CREATE TABLE IF NOT EXISTS affiliate_deals (
    run_id TEXT NOT NULL,
    brand TEXT NOT NULL,
    deal_id TEXT NOT NULL,
    title TEXT,
    merchant TEXT,
    deal_price_eur REAL,
    original_price_eur REAL,
    discount_pct REAL,
    temperature_deg INTEGER,
    voucher_code TEXT,
    deal_url TEXT,
    affiliate_network TEXT,
    date_posted TEXT,
    status TEXT,
    comments_count INTEGER,
    creator_collaborator TEXT,
    extra TEXT NOT NULL DEFAULT '{}',
    PRIMARY KEY (run_id, brand, deal_id)
);

CREATE TABLE IF NOT EXISTS pr_releases (
    run_id TEXT NOT NULL,
    brand TEXT NOT NULL,
    release_id TEXT NOT NULL,
    title TEXT,
    summary TEXT,
    publisher_source TEXT,
    category TEXT,
    date TEXT,
    status TEXT,
    url TEXT,
    key_spokesperson TEXT,
    sentiment TEXT,
    extra TEXT NOT NULL DEFAULT '{}',
    PRIMARY KEY (run_id, brand, release_id)
);

CREATE TABLE IF NOT EXISTS retail_activations (
    run_id TEXT NOT NULL,
    brand TEXT NOT NULL,
    retailer TEXT NOT NULL,
    activation_type TEXT NOT NULL,
    title TEXT,
    headline_claim TEXT,
    status TEXT,
    period TEXT,
    details TEXT,
    url TEXT,
    extra TEXT NOT NULL DEFAULT '{}',
    PRIMARY KEY (run_id, brand, retailer, activation_type, title)
);
"""


class BrandStore:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def close(self):
        self.conn.close()

    def start_run(self, run_id: str, snapshot_date: str, started_at: str) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO runs(run_id, snapshot_date, started_at) VALUES (?,?,?)",
            (run_id, snapshot_date, started_at),
        )
        self.conn.commit()

    def finish_run(self, run_id: str, finished_at: str, counts: dict[str, int]) -> None:
        self.conn.execute(
            "UPDATE runs SET finished_at=?, counts_json=? WHERE run_id=?",
            (finished_at, json.dumps(counts), run_id),
        )
        self.conn.commit()

    def save_meta_ads(self, run_id: str, ads: Iterable[AdCreative]) -> int:
        rows = [
            (
                run_id, a.brand, a.ad_id, json.dumps(a.platforms), a.format, a.status,
                a.first_seen_date, a.last_seen_date, a.flight_days, a.headline, a.body_copy,
                a.hook_angle, a.target_sku, a.cta_text, a.landing_page_url, a.destination_type,
                a.estimated_impressions_tier, a.estimated_spend_eur, json.dumps(a.extra),
            )
            for a in ads
        ]
        self.conn.execute("DELETE FROM meta_ads WHERE run_id=?", (run_id,))
        self.conn.executemany(f"INSERT OR REPLACE INTO meta_ads VALUES ({','.join('?' * 19)})", rows)
        self.conn.commit()
        return len(rows)

    def save_search(self, run_id: str, searches: Iterable[SearchFootprint]) -> int:
        rows = [
            (
                run_id, s.brand, s.keyword, s.search_type, s.status, s.rank, s.title,
                s.snippet, s.display_url, s.target_url, int(s.has_sitelinks), s.price_shown,
                json.dumps(s.extra),
            )
            for s in searches
        ]
        self.conn.execute("DELETE FROM search_footprint WHERE run_id=?", (run_id,))
        self.conn.executemany(f"INSERT OR REPLACE INTO search_footprint VALUES ({','.join('?' * 13)})", rows)
        self.conn.commit()
        return len(rows)

    def save_affiliates(self, run_id: str, deals: Iterable[AffiliateDeal]) -> int:
        rows = [
            (
                run_id, d.brand, d.deal_id, d.title, d.merchant, d.deal_price_eur,
                d.original_price_eur, d.discount_pct, d.temperature_deg, d.voucher_code,
                d.deal_url, d.affiliate_network, d.date_posted, d.status, d.comments_count,
                d.creator_collaborator, json.dumps(d.extra),
            )
            for d in deals
        ]
        self.conn.execute("DELETE FROM affiliate_deals WHERE run_id=?", (run_id,))
        self.conn.executemany(f"INSERT OR REPLACE INTO affiliate_deals VALUES ({','.join('?' * 17)})", rows)
        self.conn.commit()
        return len(rows)

    def save_pr(self, run_id: str, releases: Iterable[PRRelease]) -> int:
        rows = [
            (
                run_id, r.brand, r.release_id, r.title, r.summary, r.publisher_source,
                r.category, r.date, r.status, r.url, r.key_spokesperson, r.sentiment,
                json.dumps(r.extra),
            )
            for r in releases
        ]
        self.conn.execute("DELETE FROM pr_releases WHERE run_id=?", (run_id,))
        self.conn.executemany(f"INSERT OR REPLACE INTO pr_releases VALUES ({','.join('?' * 13)})", rows)
        self.conn.commit()
        return len(rows)

    def save_retail(self, run_id: str, acts: Iterable[RetailActivation]) -> int:
        rows = [
            (
                run_id, a.brand, a.retailer, a.activation_type, a.title, a.headline_claim,
                a.status, a.period, a.details, a.url, json.dumps(a.extra),
            )
            for a in acts
        ]
        self.conn.execute("DELETE FROM retail_activations WHERE run_id=?", (run_id,))
        self.conn.executemany(f"INSERT OR REPLACE INTO retail_activations VALUES ({','.join('?' * 11)})", rows)
        self.conn.commit()
        return len(rows)

    def latest_run_id(self) -> Optional[str]:
        row = self.conn.execute("SELECT run_id FROM runs WHERE finished_at IS NOT NULL ORDER BY started_at DESC LIMIT 1").fetchone()
        return row["run_id"] if row else None

    def get_meta_ads(self, run_id: str) -> list[dict[str, Any]]:
        rows = self.conn.execute("SELECT * FROM meta_ads WHERE run_id=?", (run_id,)).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            d["platforms"] = json.loads(d["platforms"])
            d["extra"] = json.loads(d["extra"])
            out.append(d)
        return out

    def get_search(self, run_id: str) -> list[dict[str, Any]]:
        rows = self.conn.execute("SELECT * FROM search_footprint WHERE run_id=?", (run_id,)).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            d["has_sitelinks"] = bool(d["has_sitelinks"])
            d["extra"] = json.loads(d["extra"])
            out.append(d)
        return out

    def get_affiliates(self, run_id: str) -> list[dict[str, Any]]:
        rows = self.conn.execute("SELECT * FROM affiliate_deals WHERE run_id=?", (run_id,)).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            d["extra"] = json.loads(d["extra"])
            out.append(d)
        return out

    def get_pr(self, run_id: str) -> list[dict[str, Any]]:
        rows = self.conn.execute("SELECT * FROM pr_releases WHERE run_id=?", (run_id,)).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            d["extra"] = json.loads(d["extra"])
            out.append(d)
        return out

    def get_retail(self, run_id: str) -> list[dict[str, Any]]:
        rows = self.conn.execute("SELECT * FROM retail_activations WHERE run_id=?", (run_id,)).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            d["extra"] = json.loads(d["extra"])
            out.append(d)
        return out
