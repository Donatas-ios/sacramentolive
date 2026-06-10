"""Generates docs/feedback.html — simple email contact page."""
from __future__ import annotations
from pathlib import Path
from capitol_svg import CAPITOL_SVG, TREE_SVG

_DEFAULT_OUTPUT = Path(__file__).parent / "docs" / "feedback.html"

_NAV = """
    <a href="index.html">← Events</a>
    <a href="trivia.html">🎲 Trivia</a>
    <a href="museums.html">🏛️ Museums</a>
    <a href="restaurants.html">🍽️ Restaurants</a>
    <a href="feedback.html">✉️ Feedback</a>
"""


def generate_feedback(output_path: Path = _DEFAULT_OUTPUT) -> None:
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Feedback — Sacramento Live</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
           background: #f8f5f0; color: #222; }}

    /* ── Header ── */
    .site-header {{ background: #fff; border-bottom: 3px solid #d4a017;
                   padding: 24px 24px 18px; text-align: center; }}
    .header-title {{ display: inline-flex; align-items: center; gap: 14px; justify-content: center; }}
    .capitol-icon {{ width: 58px; height: 67px; flex-shrink: 0; }}
    .tree-icon    {{ width: 72px; height: 63px; flex-shrink: 0; }}
    .site-header h1 {{ font-size: 2.2rem; font-weight: 800; color: #1a1a1a; }}
    .site-header p {{ color: #666; font-size: 0.95rem; margin-top: 6px; }}
    .site-nav {{ margin-top: 10px; display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; }}
    .site-nav a {{ font-size: 0.85rem; color: #d4a017; font-weight: 600;
                  text-decoration: none; border: 1px solid #d4a017;
                  padding: 4px 12px; border-radius: 20px; }}
    .site-nav a:hover {{ background: #d4a017; color: #fff; }}

    /* ── Page ── */
    .page {{ max-width: 640px; margin: 60px auto; padding: 0 16px 80px;
            text-align: center; }}

    .page .icon {{ font-size: 3.5rem; margin-bottom: 16px; }}
    .page h2 {{ font-size: 1.9rem; font-weight: 800; color: #1a1a1a; margin-bottom: 12px; }}
    .page .lead {{ color: #555; font-size: 1rem; line-height: 1.7; margin-bottom: 36px; }}

    .email-card {{ display: inline-block; background: #fff;
                  border-radius: 14px; box-shadow: 0 4px 20px rgba(0,0,0,.09);
                  padding: 32px 44px; }}
    .email-card p {{ font-size: 0.9rem; color: #888; margin-bottom: 14px; }}
    .email-link {{ font-size: 1.15rem; font-weight: 700; color: #d4a017;
                  text-decoration: none; word-break: break-all; }}
    .email-link:hover {{ text-decoration: underline; color: #b8860b; }}

    /* ── Footer ── */
    footer {{ text-align: center; padding: 24px 16px; color: #999;
             font-size: 0.8rem; border-top: 1px solid #e0dbd3; }}
    footer a {{ color: #d4a017; text-decoration: none; }}
  </style>
</head>
<body>

<header class="site-header">
  <div class="header-title">
    {CAPITOL_SVG}
    <h1>Sacramento Live</h1>
    {TREE_SVG}
  </div>
  <p>What's happening in Sacramento, CA</p>
  <nav class="site-nav">
    {_NAV}
  </nav>
</header>

<main class="page">
  <div class="icon">✉️</div>
  <h2>Send Us Feedback</h2>
  <p class="lead">Have a suggestion, spotted a missing event, or just want to say hi?<br>
     Drop us an email — we read every message.</p>

  <div class="email-card">
    <p>Reach us at</p>
    <a class="email-link"
       href="mailto:sacamentolive@sacramentolive.net">
      sacamentolive@sacramentolive.net
    </a>
  </div>
</main>

<footer>
  <p><a href="index.html">← Events</a> · <a href="museums.html">Museums</a> ·
     <a href="restaurants.html">Restaurants</a> · Sacramento Live</p>
</footer>

</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
