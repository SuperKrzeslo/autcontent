import os
import markdown
from datetime import datetime

ARTICLES_DIR = "articles"
OUTPUT_DIR = "site"
ARTICLE_HTML_DIR = os.path.join(OUTPUT_DIR, "articles")

os.makedirs(ARTICLE_HTML_DIR, exist_ok=True)

article_links = []

# Przetwarzanie wszystkich plików .md
for md_file in sorted(os.listdir(ARTICLES_DIR), reverse=True):
    if md_file.endswith(".md"):
        with open(os.path.join(ARTICLES_DIR, md_file), "r", encoding="utf-8") as f:
            md_content = f.read()
            html_content = markdown.markdown(md_content)

        base_name = md_file.replace(".md", ".html")
        output_path = os.path.join(ARTICLE_HTML_DIR, base_name)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{md_file}</title>
</head>
<body>
  <a href="../index.html">← Powrót</a>
  {html_content}
</body>
</html>
""")
        article_links.append(f"<li><a href='articles/{base_name}'>{md_file}</a></li>")

# Generuj index.html
with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>AI Articles</title>
</head>
<body>
  <h1>🧠 Artykuły AI</h1>
  <ul>
    {''.join(article_links)}
  </ul>
</body>
</html>
""")
