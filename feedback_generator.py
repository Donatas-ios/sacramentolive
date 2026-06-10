"""Generates docs/feedback.html — contact / feedback form.

The form submits to Formspree (https://formspree.io), a free service
that forwards submissions to sacamentolive@sacramentolive.net.

Setup (one-time):
  1. Go to https://formspree.io and sign up (free).
  2. Create a new form, set the recipient to sacamentolive@sacramentolive.net.
  3. Copy your form endpoint ID (looks like: xpzgkwqr).
  4. Set it as a GitHub Secret named FORMSPREE_ID.
  5. The workflow will inject it at build time via the env var below.

If FORMSPREE_ID is not set the form still renders but shows a warning.
"""
from __future__ import annotations
import os
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
    formspree_id = os.environ.get("FORMSPREE_ID", "")
    if formspree_id:
        action = f"https://formspree.io/f/{formspree_id}"
        setup_warning = ""
    else:
        action = "#"
        setup_warning = """
      <div class="setup-notice">
        ⚙️ <strong>Admin note:</strong> Formspree is not yet configured.
        Set the <code>FORMSPREE_ID</code> GitHub Secret to enable email delivery.
        <a href="https://formspree.io" target="_blank" rel="noopener">Sign up at formspree.io →</a>
      </div>"""

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
    .page {{ max-width: 640px; margin: 44px auto; padding: 0 16px 60px; }}

    .page-hero {{ margin-bottom: 32px; text-align: center; }}
    .page-hero .icon {{ font-size: 3rem; margin-bottom: 10px; }}
    .page-hero h2 {{ font-size: 1.8rem; font-weight: 800; color: #1a1a1a; }}
    .page-hero p {{ color: #666; font-size: 0.95rem; margin-top: 8px; line-height: 1.6; }}

    /* ── Setup notice (admin only) ── */
    .setup-notice {{ background: #fff8e1; border: 1px solid #f9a825; border-radius: 8px;
                    padding: 12px 16px; font-size: 0.85rem; color: #5d4037;
                    margin-bottom: 24px; line-height: 1.5; }}
    .setup-notice a {{ color: #d4a017; font-weight: 600; }}
    .setup-notice code {{ background: #ffe082; padding: 1px 5px; border-radius: 3px; font-size: 0.82rem; }}

    /* ── Form card ── */
    .form-card {{ background: #fff; border-radius: 14px;
                 box-shadow: 0 4px 20px rgba(0,0,0,.09);
                 padding: 36px 40px; }}
    @media (max-width: 520px) {{ .form-card {{ padding: 24px 20px; }} }}

    .form-group {{ margin-bottom: 22px; }}
    label {{ display: block; font-size: 0.85rem; font-weight: 700; color: #333;
             margin-bottom: 6px; }}
    label .required {{ color: #d4a017; margin-left: 2px; }}
    input[type="text"],
    input[type="email"],
    select,
    textarea {{
      width: 100%; padding: 11px 14px; border: 1.5px solid #ddd;
      border-radius: 8px; font-size: 0.95rem; font-family: inherit;
      color: #222; background: #fff;
      transition: border-color .15s, box-shadow .15s;
      outline: none;
    }}
    input:focus, select:focus, textarea:focus {{
      border-color: #d4a017;
      box-shadow: 0 0 0 3px rgba(212,160,23,.12);
    }}
    textarea {{ resize: vertical; min-height: 130px; line-height: 1.5; }}

    /* Rating stars */
    .star-row {{ display: flex; gap: 8px; }}
    .star-btn {{ background: none; border: none; font-size: 2rem;
                cursor: pointer; color: #ddd; transition: color .1s; padding: 0; }}
    .star-btn.on {{ color: #d4a017; }}
    .star-btn:hover {{ color: #d4a017; }}
    input[name="rating"] {{ display: none; }}

    /* Submit */
    .btn-submit {{ width: 100%; padding: 14px; background: #d4a017; color: #fff;
                  font-size: 1rem; font-weight: 700; border: none; border-radius: 9px;
                  cursor: pointer; transition: background .15s; margin-top: 8px; }}
    .btn-submit:hover {{ background: #b8860b; }}
    .btn-submit:disabled {{ background: #ccc; cursor: not-allowed; }}

    .form-note {{ font-size: 0.75rem; color: #999; text-align: center;
                 margin-top: 14px; line-height: 1.5; }}
    .form-note a {{ color: #d4a017; }}

    /* ── Thank-you state ── */
    .thankyou {{ display: none; text-align: center; padding: 40px 20px; }}
    .thankyou .ty-icon {{ font-size: 4rem; margin-bottom: 16px; }}
    .thankyou h3 {{ font-size: 1.4rem; font-weight: 800; color: #1a1a1a; margin-bottom: 8px; }}
    .thankyou p {{ color: #666; font-size: 0.95rem; line-height: 1.6; }}
    .thankyou a {{ color: #d4a017; font-weight: 600; text-decoration: none; }}

    /* ── Footer ── */
    footer {{ text-align: center; padding: 24px 16px; color: #999;
             font-size: 0.8rem; border-top: 1px solid #e0dbd3; margin-top: 0; }}
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
  <div class="page-hero">
    <div class="icon">✉️</div>
    <h2>Send Us Feedback</h2>
    <p>Have a suggestion, spotted a missing event, or just want to say hi?<br>
       We read every message and reply to questions within a day or two.</p>
  </div>

  {setup_warning}

  <div class="form-card" id="form-wrap">
    <form id="feedback-form"
          action="{action}"
          method="POST"
          novalidate>

      <!-- Formspree honeypot anti-spam -->
      <input type="text" name="_gotcha" style="display:none">
      <!-- Redirect back to thank-you state instead of Formspree page -->
      <input type="hidden" name="_next" value="https://sacramentolive.net/feedback.html?sent=1">
      <input type="hidden" name="_subject" value="SacramentoLive Feedback">

      <div class="form-group">
        <label for="name">Your name <span class="required">*</span></label>
        <input type="text" id="name" name="name" placeholder="Jane Smith" required autocomplete="name">
      </div>

      <div class="form-group">
        <label for="email">Email address <span class="required">*</span></label>
        <input type="email" id="email" name="email" placeholder="jane@example.com" required autocomplete="email">
        <p style="font-size:0.75rem;color:#999;margin-top:4px">We'll only use this to reply to your message.</p>
      </div>

      <div class="form-group">
        <label for="topic">Topic</label>
        <select id="topic" name="topic">
          <option value="">— Select a topic —</option>
          <option value="missing-event">Missing or wrong event</option>
          <option value="suggestion">Feature suggestion</option>
          <option value="bug">Something broken on the site</option>
          <option value="restaurant">Restaurant suggestion</option>
          <option value="museum">Museum / attraction suggestion</option>
          <option value="compliment">Just saying hi 👋</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div class="form-group">
        <label>Overall rating <span style="font-weight:400;color:#999">(optional)</span></label>
        <div class="star-row" id="star-row">
          <button type="button" class="star-btn" data-v="1">★</button>
          <button type="button" class="star-btn" data-v="2">★</button>
          <button type="button" class="star-btn" data-v="3">★</button>
          <button type="button" class="star-btn" data-v="4">★</button>
          <button type="button" class="star-btn" data-v="5">★</button>
        </div>
        <input type="hidden" name="rating" id="rating-input" value="">
      </div>

      <div class="form-group">
        <label for="message">Message <span class="required">*</span></label>
        <textarea id="message" name="message"
                  placeholder="Tell us what's on your mind…"
                  required minlength="10"></textarea>
      </div>

      <button type="submit" class="btn-submit" id="submit-btn">Send Feedback →</button>
      <p class="form-note">
        Your email will only be used to respond to this message.<br>
        Questions? Email us at
        <a href="mailto:sacamentolive@sacramentolive.net">sacamentolive@sacramentolive.net</a>
      </p>
    </form>

    <div class="thankyou" id="thankyou">
      <div class="ty-icon">🎉</div>
      <h3>Thanks for the feedback!</h3>
      <p>We got your message and will get back to you soon.<br>
         <a href="index.html">← Back to Events</a></p>
    </div>
  </div>
</main>

<footer>
  <p><a href="index.html">← Events</a> · <a href="museums.html">Museums</a> ·
     <a href="restaurants.html">Restaurants</a> · Sacramento Live</p>
</footer>

<script>
  /* ── Star rating ── */
  const stars = document.querySelectorAll('.star-btn');
  const ratingInput = document.getElementById('rating-input');
  stars.forEach(s => {{
    s.addEventListener('click', () => {{
      const v = +s.dataset.v;
      ratingInput.value = v;
      stars.forEach(b => b.classList.toggle('on', +b.dataset.v <= v));
    }});
  }});

  /* ── Show thank-you if redirected back with ?sent=1 ── */
  if (new URLSearchParams(location.search).get('sent') === '1') {{
    document.getElementById('feedback-form').style.display = 'none';
    document.getElementById('thankyou').style.display = 'block';
    history.replaceState(null, '', location.pathname);
  }}

  /* ── AJAX submit (keeps user on page, no Formspree redirect needed) ── */
  const form = document.getElementById('feedback-form');
  const btn  = document.getElementById('submit-btn');
  form.addEventListener('submit', async (e) => {{
    e.preventDefault();
    if (!form.checkValidity()) {{ form.reportValidity(); return; }}
    btn.disabled = true;
    btn.textContent = 'Sending…';
    try {{
      const res = await fetch(form.action, {{
        method: 'POST',
        body: new FormData(form),
        headers: {{ 'Accept': 'application/json' }}
      }});
      if (res.ok) {{
        form.style.display = 'none';
        document.getElementById('thankyou').style.display = 'block';
      }} else {{
        btn.disabled = false;
        btn.textContent = 'Send Feedback →';
        alert('Something went wrong. Please try again or email us directly.');
      }}
    }} catch (err) {{
      btn.disabled = false;
      btn.textContent = 'Send Feedback →';
      alert('Network error. Please check your connection and try again.');
    }}
  }});
</script>

</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
