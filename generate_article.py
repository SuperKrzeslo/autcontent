import os
import requests
from datetime import datetime

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

PROMPT = "Napisz artykuł blogowy po polsku na temat najnowszych trendów technologicznych."

def query(prompt):
    response = requests.post(API_URL, headers=HEADERS, json={ "inputs": prompt })
    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        print("Błąd Hugging Face:", response.text)
        return "Nie udało się wygenerować artykułu."

def save_article(content):
    today = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("articles", exist_ok=True)
    with open(f"articles/{today}.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    article = query(PROMPT)
    save_article(article)
    print("Artykuł zapisany.")