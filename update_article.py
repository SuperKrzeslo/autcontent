import requests
import os
from datetime import datetime

token = os.getenv("HUGGINGFACE_TOKEN")
headers = {"Authorization": f"Bearer {token}"}
API_URL = "https://api-inference.huggingface.co/models/gpt2"

def generate_article():
    prompt = "Napisz ciekawy akapit na bloga o nowych technologiach:"
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    response.raise_for_status()
    text = response.json()[0]["generated_text"]
    return text.strip()

def append_to_html(text):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("index.html", "a", encoding="utf-8") as f:
        f.write(f"\n<hr><p><strong>{now}:</strong> {text}</p>")

if __name__ == "__main__":
    article = generate_article()
    append_to_html(article)
