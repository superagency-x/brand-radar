# Brand Radar: German Air Fryer Marketing Intelligence

Brutal marketing intelligence scraper & competitive analysis engine tracking **SharkNinja**, **Cosori**, **Philips**, and **Tefal** in Germany (DE).

## Intelligence Vectors
1. **Meta Ad Library**: Active and trailing 12-month ad creatives (video, reels, carousels, static), copy hooks, and target landing destinations (D2C vs. Amazon vs. Retailers).
2. **Google SEM & Search**: Paid text ads, Google Shopping (PLA) bids, and organic SERP rankings across high-intent category keywords.
3. **Affiliate & Deal Communities**: MyDealz deal heat ratings, voucher codes, discounts, and detected affiliate networks (Awin, Amazon Associates, Tradedoubler).
4. **Media Spend Modeling**: Modeled DACH media investments by channel (Meta, Google SEM, Retail Media, Affiliates) and 12-month seasonality trends.
5. **PR & Editorial Test Coverage**: Verified German press releases (Presseportal) and certified *Stiftung Warentest* / *ETM Testmagazin* awards.
6. **E-Retailer Activations**: Brand Store hubs, flyer frontpages, and exclusive bundle collaborations across MediaMarkt, Otto, and Amazon.

## Quickstart

```bash
# 1. Run full scraper pipeline & compile dossier
uv run brand-radar run

# 2. View executive report in terminal
uv run brand-radar report

# 3. Launch interactive web dashboard
uv run brand-radar serve --port 8000
```
