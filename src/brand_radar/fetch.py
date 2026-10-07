"""HTTP and browser fetcher with polite delays and caching."""
from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Optional
import httpx

log = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"


class Fetcher:
    def __init__(self, cache_dir: Optional[Path] = None, delay_seconds: float = 2.0):
        self.cache_dir = cache_dir
        self.delay_seconds = delay_seconds
        self.last_request_time: dict[str, float] = {}
        self.client = httpx.Client(
            headers={"User-Agent": USER_AGENT, "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7"},
            timeout=30.0,
            follow_redirects=True,
        )

    def close(self):
        self.client.close()

    def fetch_text(self, url: str, cache_key: Optional[str] = None) -> Optional[str]:
        if self.cache_dir and cache_key:
            cache_file = self.cache_dir / f"{cache_key}.html"
            if cache_file.exists():
                return cache_file.read_text(encoding="utf-8")

        # Rate limiting
        domain = url.split("//")[-1].split("/")[0]
        last = self.last_request_time.get(domain, 0.0)
        elapsed = time.time() - last
        if elapsed < self.delay_seconds:
            time.sleep(self.delay_seconds - elapsed)

        try:
            resp = self.client.get(url)
            self.last_request_time[domain] = time.time()
            if resp.status_code == 200:
                text = resp.text
                if self.cache_dir and cache_key:
                    cache_file = self.cache_dir / f"{cache_key}.html"
                    cache_file.parent.mkdir(parents=True, exist_ok=True)
                    cache_file.write_text(text, encoding="utf-8")
                return text
        except Exception as exc:
            log.warning("Fetch failed for %s: %s", url, exc)
        return None
