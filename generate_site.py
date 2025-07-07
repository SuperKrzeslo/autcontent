import os
import markdown
from datetime import datetime

ARTICLES_DIR = "articles"
OUTPUT_DIR = "site"
ARTICLE_HTML_DIR = os.path.join(OUTPUT_DIR, "articles")

os.makedirs(ARTICLE_HTML_DIR, exist_ok=True)

article_links = []

for filename in sorted(os.listdir(ARTICLES_DIR), reverse=True):
    if filename.endswith(".md"):
        with open(os.path.join(ARTICLES_DIR, filename), "r", encoding="utf-8") as f:
            md = f.read()

        html = markdown.markdown(md)
        html_filename = filename.replace(".md", ".html")
        html_path = os.path.join(ARTICLE_HTML_DIR, html_filename)

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>{filename}</title></head>
<body>
  <a href="../index.html">← Powrót</a>
  {html}
</body>
</html>""")

        article_links.append(f"<li><a href='articles/{html_filename}'>{filename}</a></li>")

with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>AI Articles</title></head>
<body>
  <h1>🧠 Artykuły AI</h1>
  <ul>
    {''.join(article_links)}
  </ul>
</body>
</html>""")
