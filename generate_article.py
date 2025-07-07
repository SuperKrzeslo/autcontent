from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from datetime import datetime
import os
import re
import random
import torch

# === Konfiguracja ===
SITE_DIR = "site"
ARTICLES_DIR = os.path.join(SITE_DIR, "articles")
os.makedirs(ARTICLES_DIR, exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")
seed = random.randint(1000, 9999)
prompt = f"Nowości w świecie technologii na dzień {today}. Napisz profesjonalny artykuł w stylu magazynu naukowego."

# === Generator tekstu ===
model_name = "mistralai/Mistral-7B-Instruct-v0.2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)

generator = pipeline("text-generation", model=model, tokenizer=tokenizer, seed=seed)

result = generator(
    prompt,
    max_new_tokens=512,
    do_sample=True,
    temperature=0.9,
    top_k=50,
    top_p=0.95,
    num_return_sequences=1
)[0]["generated_text"]

# === Sanitizacja ===
def sanitize(text):
    return re.sub(r'[^\w\s-]', '', text).strip()

title = sanitize(result.strip().split('.')[0])[:60]
lead = result.strip().split('.')[0] + "."

filename = f"article-{today}-{seed}.html"
filepath = os.path.join(ARTICLES_DIR, filename)

# === HTML pełnego artykułu ===
article_html = f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <div class="container">
        <a href="../index.html" class="back-link">← Powrót do strony głównej</a>
        <h1>{title}</h1>
        <p>{result}</p>
    </div>
</body>
</html>
"""

with open(filepath, "w", encoding="utf-8") as f:
    f.write(article_html)

# === Miniaturka do index.html ===
thumbnail_html = f"""
<div class="card">
    <img src="https://source.unsplash.com/400x200/?technology,ai" alt="AI Image">
    <div class="card-content">
        <h3>{title}</h3>
        <p>{lead[:120]}...</p>
        <a class="button" href="articles/{filename}">Czytaj więcej →</a>
    </div>
</div>
"""

# === Aktualizacja index.html ===
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
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    updated_html = html.replace("</main>", f"{thumbnail_html}\n</main>")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(updated_html)

# === Styl CSS (tylko raz) ===
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

print(f"✅ Wygenerowano nowy artykuł: {filename} i dodano do index.html")
