"""Generates docs/museums.html — Sacramento museums directory."""
from __future__ import annotations
from pathlib import Path
from museums_data import MUSEUMS, MAPS_LINK

_DEFAULT_OUTPUT = Path(__file__).parent / "docs" / "museums.html"


def _hours_html(hours: list) -> str:
    rows = ""
    for label, time in hours:
        rows += f"<tr><td>{label}</td><td>{time}</td></tr>\n"
    return f"<table class='hours-table'>{rows}</table>"


def _admission_html(admission: list, free_note: str | None) -> str:
    if len(admission) == 1 and admission[0][1].lower() == "free":
        return f"<p class='price-free'>🎟️ Always Free</p>"
    rows = ""
    for label, price in admission:
        cls = "price-free-row" if price in ("Free", "$0") else ""
        rows += f"<tr class='{cls}'><td>{label}</td><td>{price}</td></tr>\n"
    html = f"<table class='price-table'>{rows}</table>"
    if free_note:
        html += f"<p class='free-note'>✨ {free_note}</p>"
    return html


def _card_html(m: dict) -> str:
    highlights = "".join(f"<li>{h}</li>" for h in m["highlights"])
    hours = _hours_html(m["hours"])
    admission = _admission_html(m["admission"], m.get("free_note"))
    return f"""
<article class="museum-card" style="--color:{m['color']}">
  <div class="card-header">
    <span class="museum-emoji">{m['emoji']}</span>
    <div class="card-title-block">
      <span class="cat-tag">{m['category']}</span>
      <h2 class="museum-name">
        <a href="{m['website']}" target="_blank" rel="noopener">{m['name']}</a>
      </h2>
      <p class="museum-address">
        <a href="{m['map']}" target="_blank" rel="noopener" class="map-link">📍 {m['address']}</a>
      </p>
    </div>
  </div>
  <p class="museum-desc">{m['description']}</p>
  <div class="card-grid">
    <div class="card-section">
      <h3>⏰ Hours</h3>
      {hours}
    </div>
    <div class="card-section">
      <h3>🎟️ Admission</h3>
      {admission}
    </div>
    <div class="card-section">
      <h3>⭐ Highlights</h3>
      <ul class="highlights-list">{highlights}</ul>
    </div>
  </div>
  <div class="card-footer">
    <a href="{m['website']}" class="btn-website" target="_blank" rel="noopener">Visit Website →</a>
    <a href="{m['map']}" class="btn-map" target="_blank" rel="noopener">📍 Map</a>
  </div>
</article>"""


def generate_museums(output_path: Path = _DEFAULT_OUTPUT) -> None:
    cards = "".join(_card_html(m) for m in MUSEUMS)
    free_count = sum(
        1 for m in MUSEUMS
        if any(v.lower() == "free" for _, v in m["admission"])
           or m.get("free_note")
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sacramento Museums — Sacramento Live</title>
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

    /* ── Page layout ── */
    .page {{ max-width: 960px; margin: 36px auto; padding: 0 16px; }}
    .page-hero {{ margin-bottom: 28px; }}
    .page-hero h2 {{ font-size: 1.7rem; font-weight: 800; color: #1a1a1a; }}
    .page-hero p {{ color: #666; font-size: 0.95rem; margin-top: 6px; line-height: 1.5; }}

    /* ── Map banner ── */
    .map-banner {{ display: flex; align-items: center; gap: 12px;
                  background: #fff; border: 1px solid #e0dbd3; border-radius: 10px;
                  padding: 14px 18px; margin-bottom: 32px;
                  box-shadow: 0 1px 4px rgba(0,0,0,.06); }}
    .map-banner-text {{ flex: 1; }}
    .map-banner-text strong {{ font-size: 1rem; color: #1a1a1a; }}
    .map-banner-text span {{ display: block; font-size: 0.85rem; color: #666; margin-top: 2px; }}
    .btn-map-all {{ background: #d4a017; color: #fff; font-weight: 700;
                   font-size: 0.85rem; padding: 9px 18px; border-radius: 8px;
                   text-decoration: none; white-space: nowrap; }}
    .btn-map-all:hover {{ background: #b8860b; }}

    /* ── Stats row ── */
    .stats {{ display: flex; gap: 16px; margin-bottom: 28px; flex-wrap: wrap; }}
    .stat {{ background: #fff; border-radius: 8px; padding: 12px 20px;
             border-left: 4px solid #d4a017;
             box-shadow: 0 1px 4px rgba(0,0,0,.06); }}
    .stat-num {{ font-size: 1.6rem; font-weight: 800; color: #d4a017; }}
    .stat-lbl {{ font-size: 0.78rem; color: #777; margin-top: 2px; }}

    /* ── Museum card ── */
    .museum-card {{ background: #fff; border-radius: 12px;
                   box-shadow: 0 2px 8px rgba(0,0,0,.08);
                   border-top: 5px solid var(--color);
                   padding: 22px; margin-bottom: 22px; }}
    .card-header {{ display: flex; align-items: flex-start; gap: 14px; margin-bottom: 12px; }}
    .museum-emoji {{ font-size: 2.4rem; line-height: 1; flex-shrink: 0; }}
    .card-title-block {{ flex: 1; }}
    .cat-tag {{ font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
               letter-spacing: .05em; color: var(--color); }}
    .museum-name {{ font-size: 1.3rem; font-weight: 800; margin: 4px 0; }}
    .museum-name a {{ color: #1a1a1a; text-decoration: none; }}
    .museum-name a:hover {{ color: var(--color); text-decoration: underline; }}
    .map-link {{ font-size: 0.82rem; color: #666; text-decoration: none; }}
    .map-link:hover {{ color: var(--color); text-decoration: underline; }}
    .museum-desc {{ font-size: 0.9rem; color: #555; line-height: 1.6;
                   margin-bottom: 16px; }}

    /* ── 3-column info grid ── */
    .card-grid {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 16px;
                 margin-bottom: 16px; }}
    @media (max-width: 680px) {{ .card-grid {{ grid-template-columns: 1fr; }} }}
    .card-section h3 {{ font-size: 0.8rem; font-weight: 700; color: #444;
                       margin-bottom: 8px; }}
    .hours-table, .price-table {{ width: 100%; font-size: 0.82rem; border-collapse: collapse; }}
    .hours-table td, .price-table td {{ padding: 3px 0; vertical-align: top; }}
    .hours-table td:first-child, .price-table td:first-child {{ color: #555; padding-right: 10px; white-space: nowrap; }}
    .hours-table td:last-child, .price-table td:last-child {{ font-weight: 600; color: #1a1a1a; }}
    .price-free {{ font-size: 0.9rem; font-weight: 700; color: #2e7d32; }}
    .price-free-row td {{ color: #2e7d32 !important; font-weight: 600 !important; }}
    .free-note {{ font-size: 0.78rem; color: #2e7d32; margin-top: 6px; font-style: italic; }}
    .highlights-list {{ list-style: none; }}
    .highlights-list li {{ font-size: 0.82rem; color: #555; padding: 3px 0;
                          padding-left: 14px; position: relative; }}
    .highlights-list li::before {{ content: '→'; position: absolute; left: 0; color: var(--color); }}

    /* ── Card footer ── */
    .card-footer {{ display: flex; gap: 10px; padding-top: 14px;
                   border-top: 1px solid #f0ece5; }}
    .btn-website {{ background: var(--color); color: #fff; font-size: 0.82rem;
                   font-weight: 700; padding: 7px 16px; border-radius: 7px;
                   text-decoration: none; }}
    .btn-website:hover {{ opacity: .88; }}
    .btn-map {{ background: #f4f0ea; color: #555; font-size: 0.82rem;
               font-weight: 600; padding: 7px 14px; border-radius: 7px;
               text-decoration: none; }}
    .btn-map:hover {{ background: #e8e2d8; }}

    /* ── Footer ── */
    footer {{ text-align: center; padding: 32px 16px; color: #999;
             font-size: 0.8rem; border-top: 1px solid #e0dbd3; margin-top: 20px; }}
    footer a {{ color: #d4a017; text-decoration: none; }}
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
    <h2>🏛️ Sacramento Museums</h2>
    <p>From Gold Rush history to world-class art — Sacramento's museums span centuries of California's story. Hours and prices are subject to change; always confirm before visiting.</p>
  </div>

  <div class="map-banner">
    <div style="font-size:2rem">🗺️</div>
    <div class="map-banner-text">
      <strong>View All Museums on a Map</strong>
      <span>See every museum location in Sacramento at a glance</span>
    </div>
    <a href="{MAPS_LINK}" target="_blank" rel="noopener" class="btn-map-all">Open Map →</a>
  </div>

  <div class="stats">
    <div class="stat">
      <div class="stat-num">{len(MUSEUMS)}</div>
      <div class="stat-lbl">Museums listed</div>
    </div>
    <div class="stat">
      <div class="stat-num">{free_count}</div>
      <div class="stat-lbl">With free admission options</div>
    </div>
    <div class="stat">
      <div class="stat-num">2</div>
      <div class="stat-lbl">Always free</div>
    </div>
  </div>

{cards}
</main>

<footer>
  <p>Hours and prices may change — always verify on the museum's website before visiting.<br>
  <a href="index.html">← Back to Events</a> · <a href="trivia.html">Sacramento Trivia</a> · Sacramento Live</p>
</footer>

</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
