"""Generates docs/trivia.html with a daily-rotating selection of facts and quiz questions."""
from __future__ import annotations
import random
from datetime import date
from pathlib import Path

from trivia_data import FACTS, QUIZ

_DEFAULT_OUTPUT = Path(__file__).parent / "docs" / "trivia.html"

# How many facts and quiz questions to show each day
_NUM_FACTS = 8
_NUM_QUIZ = 5


def _daily_selection(pool: list, n: int, today: date) -> list:
    """Pick n items from pool, seeded by date so it's stable within a day
    but rotates daily. Items can repeat across days but not within a day."""
    rng = random.Random(today.toordinal())
    return rng.sample(pool, min(n, len(pool)))


def generate_trivia(output_path: Path = _DEFAULT_OUTPUT, today: date | None = None) -> None:
    today = today or date.today()
    facts = _daily_selection(FACTS, _NUM_FACTS, today)
    quiz = _daily_selection(QUIZ, _NUM_QUIZ, today)

    fact_cards = ""
    for f in facts:
        fact_cards += f"""
    <div class="trivia-card" style="--color:{f['color']}">
      <div class="emoji">{f['emoji']}</div>
      <h3>{f['category']}</h3>
      <div class="fact">{f['fact']}</div>
      <div class="detail">{f['detail']}</div>
    </div>"""

    quiz_items = ""
    for i, q in enumerate(quiz, 1):
        opts = ""
        for j, opt in enumerate(q["options"]):
            is_correct = str(j == q["answer"]).lower()
            opts += f'        <button class="option" onclick="answer(this,\'q{i}\',{is_correct})">{chr(65+j)}. {opt}</button>\n'
        quiz_items += f"""
    <div class="question" id="q{i}">
      <p>{i}. {q['question']}</p>
      <div class="options">
{opts}      </div>
      <div class="explanation">{q['explanation']}</div>
    </div>"""

    date_str = today.strftime("%B %-d, %Y")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sacramento Trivia — Sacramento Live</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
           background: #f8f5f0; color: #222; }}

    .site-header {{ background: #fff; border-bottom: 3px solid #d4a017;
                   padding: 20px 24px; }}
    .site-header h1 {{ font-size: 2rem; font-weight: 800; color: #1a1a1a; }}
    .site-header p {{ color: #666; font-size: 0.95rem; margin-top: 4px; }}
    .site-nav {{ margin-top: 10px; }}
    .site-nav a {{ font-size: 0.85rem; color: #d4a017; font-weight: 600;
                  text-decoration: none; border: 1px solid #d4a017;
                  padding: 4px 12px; border-radius: 20px; }}
    .site-nav a:hover {{ background: #d4a017; color: #fff; }}

    .page {{ max-width: 900px; margin: 40px auto; padding: 0 16px; }}
    .page h2 {{ font-size: 1.6rem; font-weight: 800; color: #1a1a1a; margin-bottom: 6px; }}
    .page .subtitle {{ color: #666; margin-bottom: 32px; font-size: 0.9rem; }}

    .trivia-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }}
    @media (max-width: 640px) {{ .trivia-grid {{ grid-template-columns: 1fr; }} }}

    .trivia-card {{ background: #fff; border-radius: 10px;
                   box-shadow: 0 1px 4px rgba(0,0,0,.08);
                   padding: 20px; border-left: 5px solid var(--color); }}
    .trivia-card .emoji {{ font-size: 2rem; margin-bottom: 8px; }}
    .trivia-card h3 {{ font-size: 0.75rem; font-weight: 700; color: var(--color);
                      text-transform: uppercase; letter-spacing: .04em; margin-bottom: 6px; }}
    .trivia-card .fact {{ font-size: 1rem; font-weight: 600; color: #1a1a1a;
                         line-height: 1.4; margin-bottom: 6px; }}
    .trivia-card .detail {{ font-size: 0.85rem; color: #666; line-height: 1.5; }}

    .quiz-section {{ margin-top: 48px; }}
    .quiz-section h2 {{ font-size: 1.4rem; font-weight: 800; margin-bottom: 20px; }}
    .question {{ background: #fff; border-radius: 10px; padding: 20px;
                box-shadow: 0 1px 4px rgba(0,0,0,.08); margin-bottom: 16px; }}
    .question p {{ font-weight: 600; margin-bottom: 12px; font-size: 1rem; }}
    .options {{ display: flex; flex-direction: column; gap: 8px; }}
    .option {{ padding: 10px 14px; border: 1px solid #ddd; border-radius: 6px;
              cursor: pointer; font-size: 0.9rem; background: #fff;
              text-align: left; transition: background .15s; }}
    .option:hover {{ background: #f5f5f5; }}
    .option.correct {{ background: #e8f5e9; border-color: #4CAF50; color: #1b5e20; font-weight: 600; }}
    .option.wrong {{ background: #ffebee; border-color: #f44336; color: #b71c1c; }}
    .explanation {{ margin-top: 10px; font-size: 0.85rem; color: #555;
                   background: #f9f9f9; padding: 10px 12px; border-radius: 6px;
                   display: none; }}

    footer {{ text-align: center; padding: 32px 16px; color: #999;
             font-size: 0.8rem; border-top: 1px solid #e0dbd3; margin-top: 40px; }}
  </style>
</head>
<body>

<header class="site-header">
  <h1>Sacramento Live</h1>
  <p>What's happening in Sacramento, CA — next 14 days</p>
  <nav class="site-nav">
    <a href="index.html">← Back to Events</a>
  </nav>
</header>

<main class="page">
  <h2>🎲 Sacramento Trivia</h2>
  <p class="subtitle">Daily selection of fun facts about California's capital · Updated {date_str}</p>

  <div class="trivia-grid">
{fact_cards}
  </div>

  <div class="quiz-section">
    <h2>🧠 Test Your Knowledge</h2>
{quiz_items}
  </div>
</main>

<footer>
  <p>Sacramento Live · <a href="index.html" style="color:#d4a017">Back to Events</a> · New trivia every day</p>
</footer>

<script>
  function answer(btn, questionId, isCorrect) {{
    const q = document.getElementById(questionId);
    q.querySelectorAll('.option').forEach(b => {{
      b.disabled = true;
      b.style.cursor = 'default';
    }});
    btn.classList.add(isCorrect ? 'correct' : 'wrong');
    if (!isCorrect) {{
      q.querySelectorAll('.option').forEach(b => {{
        if (b.onclick.toString().includes(',true)')) b.classList.add('correct');
      }});
    }}
    q.querySelector('.explanation').style.display = 'block';
  }}
</script>

</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
