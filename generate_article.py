from transformers import pipeline
from datetime import datetime
import os

generator = pipeline("text-generation", model="gpt2")

prompt = "The future of artificial intelligence in everyday life"

result = generator(prompt, max_length=300, num_return_sequences=1)[0]["generated_text"]

# Zapisz do pliku
today = datetime.now().strftime("%Y-%m-%d")
os.makedirs("articles", exist_ok=True)
with open(f"articles/article-{today}.md", "w", encoding="utf-8") as f:
    f.write(f"# AI Article ({today})\n\n")
    f.write(result)
