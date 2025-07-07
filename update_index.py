from datetime import datetime
import os

today = datetime.now().strftime("%Y-%m-%d")
article_title = f"AI Article ({today})"
article_snippet = "Generated insights on AI's impact on daily life."
article_image = "assets/article-cover.jpg"  # Zakładamy placeholder
article_url = f"articles/article-{today}.html"

with open("site/index.html", "r", encoding="utf-8") as f:
    content = f.read()

insertion_point = "<!-- AUTO-INSERT-ARTICLE -->"

card_html = f'''
<a class="card" href="{article_url}">
    <img src="{article_image}" alt="Cover">
    <div class="card-content">
        <h2>{article_title}</h2>
        <p>{article_snippet}</p>
    </div>
</a>
{insertion_point}
'''

updated = content.replace(insertion_point, card_html)
with open("site/index.html", "w", encoding="utf-8") as f:
    f.write(updated)
