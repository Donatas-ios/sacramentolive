"""Generates docs/restaurants.html — Sacramento restaurants by cuisine."""
from __future__ import annotations
from pathlib import Path
from restaurants_data import CUISINES, MAPS_LINK

_DEFAULT_OUTPUT = Path(__file__).parent / "docs" / "restaurants.html"
_MAX_PER_GROUP = 15


def _stars(rating: float) -> str:
    """Return filled/half/empty star HTML for a rating out of 5."""
    stars = ""
    for i in range(1, 6):
        if rating >= i:
            stars += '<span class="star full">★</span>'
        elif rating >= i - 0.5:
            stars += '<span class="star half">★</span>'
        else:
            stars += '<span class="star empty">★</span>'
    return stars


def _price_label(price: str) -> str:
    labels = {"$": "Budget", "$$": "Moderate", "$$$": "Upscale", "$$$$": "Fine Dining"}
    return labels.get(price, price)


def _restaurant_row(r: dict) -> str:
    stars_html = _stars(r["rating"])
    price_cls = "price-" + len(r["price"]) * "d"  # price-d, price-dd, etc.
    note_html = f'<span class="rest-note">{r["note"]}</span>' if r.get("note") else ""
    website_btn = (
        f'<a href="{r["website"]}" class="btn-web" target="_blank" rel="noopener">Website</a>'
        if r.get("website") else ""
    )
    return f"""
    <div class="rest-row">
      <div class="rest-main">
        <div class="rest-top">
          <span class="rest-name">
            <a href="{r['map']}" target="_blank" rel="noopener" class="rest-name-link">{r['name']}</a>
          </span>
          <span class="rest-rating-badge">
            <span class="rating-num">{r['rating']}</span>
            <span class="stars-wrap">{stars_html}</span>
          </span>
          <span class="rest-price" title="{_price_label(r['price'])}">{r['price']}</span>
        </div>
        <div class="rest-bottom">
          <a href="{r['map']}" class="rest-address" target="_blank" rel="noopener">📍 {r['address']}</a>
          {note_html}
        </div>
      </div>
      <div class="rest-actions">
        {website_btn}
        <a href="{r['map']}" class="btn-map" target="_blank" rel="noopener">Map</a>
      </div>
    </div>"""


def _cuisine_section(c: dict) -> str:
    restaurants = sorted(c["restaurants"], key=lambda r: r["rating"], reverse=True)[:_MAX_PER_GROUP]
    rows = "".join(_restaurant_row(r) for r in restaurants)
    avg = sum(r["rating"] for r in restaurants) / len(restaurants)
    count = len(restaurants)
    return f"""
<section class="cuisine-section" id="{c['id']}">
  <div class="cuisine-header" style="--color:{c['color']}">
    <span class="cuisine-emoji">{c['emoji']}</span>
    <div class="cuisine-title-block">
      <h2 class="cuisine-name">{c['label']}</h2>
      <p class="cuisine-meta">{count} restaurants · avg rating {avg:.1f} ⭐</p>
    </div>
  </div>
  <p class="cuisine-blurb">{c['blurb']}</p>
  <div class="rest-list">
    {rows}
  </div>
</section>"""


def generate_restaurants(output_path: Path = _DEFAULT_OUTPUT) -> None:
    sections = "".join(_cuisine_section(c) for c in CUISINES)
    total = sum(
        min(len(c["restaurants"]), _MAX_PER_GROUP) for c in CUISINES
    )

    # Build jump-nav pills
    nav_pills = "".join(
        f'<a href="#{c["id"]}" class="nav-pill" style="--color:{c["color"]}">'
        f'{c["emoji"]} {c["label"]}</a>'
        for c in CUISINES
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sacramento Restaurants — Sacramento Live</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
           background: #f8f5f0; color: #222; }}

    /* ── Header ── */
    .site-header {{ background: #fff; border-bottom: 3px solid #d4a017;
                   padding: 24px 24px 18px; text-align: center; }}
    .header-title {{ display: inline-flex; align-items: center; gap: 14px; justify-content: center; }}
    .capitol-icon {{ width: 52px; height: 52px; flex-shrink: 0; }}
    .site-header h1 {{ font-size: 2.2rem; font-weight: 800; color: #1a1a1a; }}
    .site-header p {{ color: #666; font-size: 0.95rem; margin-top: 6px; }}
    .site-nav {{ margin-top: 10px; display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; }}
    .site-nav a {{ font-size: 0.85rem; color: #d4a017; font-weight: 600;
                  text-decoration: none; border: 1px solid #d4a017;
                  padding: 4px 12px; border-radius: 20px; }}
    .site-nav a:hover {{ background: #d4a017; color: #fff; }}

    /* ── Page ── */
    .page {{ max-width: 960px; margin: 36px auto; padding: 0 16px; }}
    .page-hero {{ margin-bottom: 24px; }}
    .page-hero h2 {{ font-size: 1.7rem; font-weight: 800; color: #1a1a1a; }}
    .page-hero p {{ color: #666; font-size: 0.95rem; margin-top: 6px; line-height: 1.5; }}

    /* ── Map banner ── */
    .map-banner {{ display: flex; align-items: center; gap: 12px;
                  background: #fff; border: 1px solid #e0dbd3; border-radius: 10px;
                  padding: 14px 18px; margin-bottom: 24px;
                  box-shadow: 0 1px 4px rgba(0,0,0,.06); }}
    .map-banner-text {{ flex: 1; }}
    .map-banner-text strong {{ font-size: 1rem; color: #1a1a1a; }}
    .map-banner-text span {{ display: block; font-size: 0.85rem; color: #666; margin-top: 2px; }}
    .btn-map-all {{ background: #d4a017; color: #fff; font-weight: 700;
                   font-size: 0.85rem; padding: 9px 18px; border-radius: 8px;
                   text-decoration: none; white-space: nowrap; }}
    .btn-map-all:hover {{ background: #b8860b; }}

    /* ── Stats ── */
    .stats {{ display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }}
    .stat {{ background: #fff; border-radius: 8px; padding: 12px 20px;
             border-left: 4px solid #d4a017;
             box-shadow: 0 1px 4px rgba(0,0,0,.06); }}
    .stat-num {{ font-size: 1.6rem; font-weight: 800; color: #d4a017; }}
    .stat-lbl {{ font-size: 0.78rem; color: #777; margin-top: 2px; }}

    /* ── Jump nav ── */
    .jump-nav {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 32px; }}
    .nav-pill {{ font-size: 0.8rem; font-weight: 600; padding: 6px 14px;
               border-radius: 20px; text-decoration: none;
               background: #fff; color: var(--color);
               border: 1.5px solid var(--color);
               transition: background .15s; white-space: nowrap; }}
    .nav-pill:hover {{ background: var(--color); color: #fff; }}

    /* ── Cuisine section ── */
    .cuisine-section {{ margin-bottom: 40px; }}
    .cuisine-header {{ display: flex; align-items: center; gap: 12px;
                      background: #fff; border-radius: 10px 10px 0 0;
                      border-left: 6px solid var(--color);
                      padding: 16px 20px;
                      box-shadow: 0 1px 4px rgba(0,0,0,.06); }}
    .cuisine-emoji {{ font-size: 2rem; line-height: 1; }}
    .cuisine-name {{ font-size: 1.25rem; font-weight: 800; color: #1a1a1a; }}
    .cuisine-meta {{ font-size: 0.8rem; color: #888; margin-top: 3px; }}
    .cuisine-blurb {{ font-size: 0.88rem; color: #555; line-height: 1.6;
                     background: #faf7f2; padding: 12px 20px;
                     border-left: 6px solid var(--color, #d4a017);
                     margin-bottom: 2px; }}

    /* ── Restaurant list ── */
    .rest-list {{ background: #fff; border-radius: 0 0 10px 10px;
                 box-shadow: 0 2px 8px rgba(0,0,0,.07); overflow: hidden; }}
    .rest-row {{ display: flex; align-items: center; justify-content: space-between;
               padding: 13px 18px; border-bottom: 1px solid #f2ece4;
               gap: 12px; }}
    .rest-row:last-child {{ border-bottom: none; }}
    .rest-row:hover {{ background: #fdfaf6; }}
    .rest-main {{ flex: 1; min-width: 0; }}
    .rest-top {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
    .rest-name-link {{ font-size: 1rem; font-weight: 700; color: #1a1a1a;
                      text-decoration: none; }}
    .rest-name-link:hover {{ color: #d4a017; text-decoration: underline; }}
    .rest-rating-badge {{ display: inline-flex; align-items: center; gap: 4px; }}
    .rating-num {{ font-size: 0.82rem; font-weight: 700; color: #d4a017; }}
    .stars-wrap {{ font-size: 0.8rem; line-height: 1; white-space: nowrap; }}
    .star.full  {{ color: #d4a017; }}
    .star.half  {{ color: #d4a017; opacity: 0.55; }}
    .star.empty {{ color: #ddd; }}
    .rest-price {{ font-size: 0.78rem; font-weight: 700; color: #888;
                  background: #f4f0ea; padding: 2px 7px; border-radius: 10px; }}
    .rest-bottom {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
                   margin-top: 4px; }}
    .rest-address {{ font-size: 0.78rem; color: #888; text-decoration: none; }}
    .rest-address:hover {{ color: #d4a017; text-decoration: underline; }}
    .rest-note {{ font-size: 0.78rem; color: #777; font-style: italic; }}
    .rest-note::before {{ content: '· '; }}
    .rest-actions {{ display: flex; gap: 6px; flex-shrink: 0; }}
    .btn-web {{ font-size: 0.75rem; font-weight: 600; padding: 5px 11px;
               border-radius: 6px; text-decoration: none;
               background: #d4a017; color: #fff; }}
    .btn-web:hover {{ background: #b8860b; }}
    .btn-map {{ font-size: 0.75rem; font-weight: 600; padding: 5px 11px;
               border-radius: 6px; text-decoration: none;
               background: #f4f0ea; color: #555; }}
    .btn-map:hover {{ background: #e8e2d8; }}

    /* ── Footer ── */
    footer {{ text-align: center; padding: 32px 16px; color: #999;
             font-size: 0.8rem; border-top: 1px solid #e0dbd3; margin-top: 20px; }}
    footer a {{ color: #d4a017; text-decoration: none; }}
    @media (max-width: 600px) {{
      .rest-row {{ flex-direction: column; align-items: flex-start; }}
      .rest-actions {{ width: 100%; justify-content: flex-start; }}
      .cuisine-blurb {{ display: none; }}
    }}
  </style>
</head>
<body>

<header class="site-header">
  <div class="header-title">
    <svg class="capitol-icon" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <ellipse cx="50" cy="38" rx="11" ry="5" fill="#d4a017" opacity="0.18"/>
      <path d="M39 38 Q39 18 50 14 Q61 18 61 38Z" fill="#d4a017"/>
      <rect x="42" y="36" width="16" height="7" fill="#d4a017"/>
      <rect x="47" y="8" width="6" height="7" rx="1" fill="#d4a017"/>
      <rect x="48.5" y="4" width="3" height="5" rx="1" fill="#d4a017"/>
      <rect x="22" y="43" width="56" height="30" fill="#d4a017"/>
      <rect x="30" y="43" width="3" height="20" fill="#b8860b"/>
      <rect x="37" y="43" width="3" height="20" fill="#b8860b"/>
      <rect x="60" y="43" width="3" height="20" fill="#b8860b"/>
      <rect x="67" y="43" width="3" height="20" fill="#b8860b"/>
      <rect x="27" y="43" width="46" height="4" fill="#c69214"/>
      <rect x="18" y="73" width="64" height="4" rx="1" fill="#d4a017"/>
      <rect x="12" y="77" width="76" height="4" rx="1" fill="#c69214"/>
      <rect x="6"  y="81" width="88" height="4" rx="1" fill="#d4a017"/>
      <rect x="46" y="56" width="8" height="17" rx="1" fill="#fff" opacity="0.55"/>
    </svg>
    <h1>Sacramento Live</h1>
  </div>
  <p>What's happening in Sacramento, CA</p>
  <nav class="site-nav">
    <a href="index.html">← Events</a>
    <a href="trivia.html">🎲 Trivia</a>
    <a href="museums.html">🏛️ Museums</a>
    <a href="restaurants.html">🍽️ Restaurants</a>
  </nav>
</header>

<main class="page">
  <div class="page-hero">
    <h2>🍽️ Sacramento Restaurants</h2>
    <p>Sacramento is America's Farm-to-Fork Capital — {total}+ top-rated restaurants across {len(CUISINES)} cuisines, sorted by Google Maps rating. Tap any name or address to open in Google Maps.</p>
  </div>

  <div class="map-banner">
    <div style="font-size:2rem">🗺️</div>
    <div class="map-banner-text">
      <strong>View All Restaurants on a Map</strong>
      <span>Explore Sacramento's dining scene in Google Maps</span>
    </div>
    <a href="{MAPS_LINK}" target="_blank" rel="noopener" class="btn-map-all">Open Map →</a>
  </div>

  <div class="stats">
    <div class="stat">
      <div class="stat-num">{total}+</div>
      <div class="stat-lbl">Restaurants listed</div>
    </div>
    <div class="stat">
      <div class="stat-num">{len(CUISINES)}</div>
      <div class="stat-lbl">Cuisine types</div>
    </div>
    <div class="stat">
      <div class="stat-num">4.3</div>
      <div class="stat-lbl">Average rating</div>
    </div>
  </div>

  <div class="jump-nav">
    {nav_pills}
  </div>

{sections}
</main>

<footer>
  <p>Ratings sourced from Google Maps and may change over time — always check before visiting.<br>
  <a href="index.html">← Back to Events</a> · <a href="museums.html">Museums</a> · <a href="trivia.html">Trivia</a> · Sacramento Live</p>
</footer>

</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
