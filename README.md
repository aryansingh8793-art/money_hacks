[README.md](https://github.com/user-attachments/files/35239058/README.md)
# money_hacks
Compare cosmetic prices across Nykaa, Purplle, Amazon India and Flipkart. A FastAPI + Playwright app that matches the same product across stores by brand, shade and size, and shows the cheapest first with price history.
# Cosmetic Price Tracker

Search a cosmetic product and compare its price across online stores. Listings from different stores are matched to the same product (brand, shade and size aware), then shown cheapest first. Every search is saved to SQLite so price history can be charted later.

## Run it

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Open http://127.0.0.1:8000 and try "Maybelline Fit Me". Run tests with `python -m pytest`.

## How it works

```
browser → FastAPI /api/search → scrapers (run in parallel) → matching → SQLite + JSON
```

- `backend/scrapers/` one file per store, all implementing `Scraper.search()`
- `backend/matching.py` groups listings: sizes must match, shade numbers must match, then fuzzy name similarity (rapidfuzz)
- `backend/db.py` stores every price seen; `/api/history?url=...` returns it
- Results are cached for 10 minutes so stores are not hit on every search

## Real stores (default) and demo mode

By default the app compares Nykaa, Purplle, Amazon India and Flipkart. Their pages are rendered by JavaScript, so it uses a headless browser (Playwright). One-time setup:

```bash
pip install -r requirements.txt
playwright install chromium
uvicorn backend.main:app --reload
```

Searches take 10 to 20 seconds the first time and are then cached for 10 minutes. For offline sample data, start with `DEMO=1 uvicorn backend.main:app --reload` (on Windows PowerShell: `$env:DEMO=1; uvicorn backend.main:app --reload`).

**If a store returns nothing:** open the `debug/` folder, which holds the HTML the browser received. Amazon in particular may show a CAPTCHA page to automated browsers. The parser looks for product-link patterns (`/dp/`, `/p/itm`, `/product/`) rather than CSS classes, so a store changing its layout rarely breaks it, but a changed URL pattern is edited in `backend/scrapers/__init__.py`.

**Use responsibly:** check each site's `robots.txt` and terms, keep the cache on, and treat this as a learning project. For anything public, use the stores' affiliate or partner APIs instead of scraping.

## Ideas to extend

- Price history chart using `/api/history`
- Price-drop alerts by email
- Embedding-based matching for harder product names
