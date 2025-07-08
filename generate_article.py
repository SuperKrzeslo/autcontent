from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
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

# === Prompt ===
prompt = (
    f"Napisz zabawną, satyryczną historyjkę o Grzegorzu Braunie, pośle Konfederacji. "
    f"Uwzględnij najważniejsze wydarzenia z ostatnich dni (do {today}). "
    f"Tekst ma być humorystyczny, kreatywny i w języku polskim. "
    f"Nie pisz suchych faktów historycznych, tylko zabawną opowieść, jakbyś opowiadał ją znajomym przy kawie. "
    f"Nie wymieniaj listy książek, tylko skoncentruj się na zabawnych zdarzeniach z udziałem Brauna, np. gaszenie świec, wypowiedzi sejmowe, memiczne sytuacje."
)

# === Model: Mistral 7B Instruct ===
model_name = "mistralai/Mistral-7B-Instruct-v0.1"
hf_token = os.getenv("HUGGINGFACE_TOKEN")

tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto",
    token=hf_token
)

generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
)

# === Generowanie tekstu ===
generated = generator(
    prompt,
    max_new_tokens=700,
    do_sample=True,
    temperature=0.85,
    top_k=50,
    top_p=0.95,
    num_return_sequences=1
)[0]["generated_text"]

# === Czyszczenie tekstu ===
def clean_text(text):
    # usuń prompt jeśli nadal jest obecny
    cleaned = text.replace(prompt, "").strip()

    # usuń powtarzające się linijki
    lines = cleaned.split('\n')
    seen = set()
    unique_lines = []
    for line in lines:
        line = line.strip()
        if line and line not in seen:
            unique_lines.append(line)
            seen.add(line)
    cleaned = "\n".join(unique_lines)

    # sanity check
    if "Grzegorz Braun" not in cleaned:
        cleaned = "Nie udało się wygenerować sensownego tekstu. Spróbuj ponownie."
    return cleaned

response = clean_text(generated)

# === Tytuł i lead ===
def sanitize(text):
    return re.sub(r'[^\w\s-]', '', text).strip()

title = sanitize(response.split('.')[0])[:60]
lead = response.split('.')[0] + "."

filename = f"article-{today}-{seed}.html"
filepath = os.path.join(ARTICLES_DIR, filename)

# === HTML artykułu ===
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
        <p>{response}</p>
    </div>
</body>
</html>
"""

with open(filepath, "w", encoding="utf-8") as f:
    f.write(article_html)

# === Miniaturka na index.html ===
thumbnail_html = f"""
<div class="card">
    <img src="https://source.unsplash.com/400x200/?funny,politics" alt="Zabawne zdjęcie">
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
        <p>Codzienna dawka humoru politycznego</p>
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

# === Styl CSS jeśli brak ===
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

print(f"✅ Artykuł zapisany jako: {filename} i dodany do index.html")
