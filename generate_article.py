import os
import datetime
from transformers import pipeline

def main():
    generator = pipeline("text-generation", model="gpt2")
    prompt = "Najnowsze trendy technologiczne w 2025 roku"
    result = generator(prompt, max_length=300, num_return_sequences=1)[0]["generated_text"]

    today = datetime.date.today().strftime("%Y-%m-%d")
    os.makedirs("articles", exist_ok=True)
    filename = f"articles/article-{today}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# AI Article – {today}\n\n")
        f.write(result)

    print(f"🔍 ✔ Artykuł zapisany: {filename}")

if __name__ == "__main__":
    main()
