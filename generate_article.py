from transformers import pipeline
from datetime import datetime
import os
import re

# Prompt do generowania artykułu
PROMPT = "The future of artificial intelligence in everyday life"

# Nazwa katalogu na stronę
SITE_DIR = "site"
ARTICLES_DIR = os.path.join(SITE_DIR, "articles")
os.makedirs(ARTICLES_DIR, exist_ok=True)

# Ustaw pipeline
generator = pipeline("text-generation", model="gpt2")
result = generator(PROMPT, max_new_tokens=256, num_return_sequences=1)[0]["generated_text"]

# Wyczyść dziwne znaki
def sanitize(text):
    return re.sub(r'[^\w\s-]', '', text).strip()

# Tytuł i lead z tekstu
title = sanitize(result.strip().split('.')[0])[:60]
lead = result.strip().split('.')[0] + '.'

# Data pliku
today = datetime.now().strftime("%Y-%m-%d")
filename = f"article-{today}.html"
filepath = os.path.join(ARTICLES_DIR, filename)

# HTML artykułu (pełna strona)
article_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <div class="container">
        <a href="../index.html" class="back-link">← Back to main page</a>
        <h1>{title}</h1>
        <p>{result}</p>
    </div>
</body>
</html>
"""

# Zapisz pełny artykuł
with open(filepath, "w", encoding="utf-8") as f:
    f.write(article_html)

# Ścieżka miniaturki (link i skrót artykułu)
thumbnail_html = f"""
<div class="card">
    <img src="https://source.unsplash.com/400x200/?ai,technology" alt="AI Image">
    <div class="card-content">
        <h3>{title}</h3>
        <p>{lead[:120]}...</p>
        <a class="button" href="articles/{filename}">Czytaj więcej →</a>
    </div>
</div>
"""

# Wygeneruj/podmień wpisy w index.html
index_path = os.path.join(SITE_DIR, "index.html")
if not os.path.exists(index_path):
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>AutContent - Artykuły AI</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>AutContent - Artykuły generowane przez AI</h1>
        <p>Codzienna dawka wiedzy o sztucznej inteligencji</p>
    </header>
    <main id="articles">
        {thumbnail_html}
    </main>
</body>
</html>
""")
else:
    # Podmień treść w istniejącym pliku index.html
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    updated_html = html.replace("</main>", f"{thumbnail_html}\n</main>")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(updated_html)

# Zapisz styl CSS jeśli nie istnieje
style_path = os.path.join(SITE_DIR, "style.css")
if not os.path.exists(style_path):
    with open(style_path, "w", encoding="utf-8") as f:
        f.write("""
body {
    font-family: 'Segoe UI', sans-serif;
    margin: 0;
    padding: 0;
    background: #f5f5f5;
}
header {
    background: #111;
    color: #fff;
    padding: 40px 20px;
    text-align: center;
}
main {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    padding: 20px;
    justify-content: center;
}
.card {
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    width: 300px;
    overflow: hidden;
    transition: transform 0.2s;
}
.card:hover {
    transform: translateY(-5px);
}
.card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
}
.card-content {
    padding: 15px;
}
.card-content h3 {
    margin: 0 0 10px;
    font-size: 18px;
}
.card-content p {
    font-size: 14px;
    color: #555;
}
.button {
    display: inline-block;
    margin-top: 10px;
    background: #0070f3;
    color: #fff;
    padding: 8px 12px;
    text-decoration: none;
    border-radius: 4px;
}
.button:hover {
    background: #005dc1;
}
.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 40px 20px;
}
.back-link {
    display: inline-block;
    margin-bottom: 20px;
    color: #0070f3;
    text-decoration: none;
}
.back-link:hover {
    text-decoration: underline;
}
""")

print("✅ Artykuł wygenerowany i dodany do strony.")
