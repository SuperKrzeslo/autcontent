from transformers import pipeline
from datetime import datetime
import os
from pathlib import Path

generator = pipeline("text-generation", model="gpt2")

prompt = "The future of artificial intelligence in everyday life"
result = generator(prompt, max_length=300, num_return_sequences=1)[0]["generated_text"]
today = datetime.now().strftime("%Y-%m-%d")
slug = today

os.makedirs("articles", exist_ok=True)
md_path = f"articles/article-{slug}.md"
html_path = f"site/articles/article-{slug}.html"

# Markdown
with open(md_path, "w", encoding="utf-8") as f:
    f.write(f"# AI Article ({today})\n\n")
    f.write(result)

# HTML
html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Article {today}</title>
    <style>
        body {{ font-family: sans-serif; max-width: 800px; margin: 40px auto; line-height: 1.6; padding: 20px; }}
        h1 {{ color: #333; }}
    </style>
</head>
<body>
    <h1>AI Article ({today})</h1>
    <p>{result.replace("\n", "<br>")}</p>
</body>
</html>
'''

os.makedirs("site/articles", exist_ok=True)
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)
