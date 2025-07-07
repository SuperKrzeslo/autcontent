
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "gpt2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1)

def generate_article(prompt, max_tokens=300):
    output = generator(prompt, max_length=max_tokens, do_sample=True, top_k=50, top_p=0.95, temperature=0.9)
    return output[0]['generated_text']

if __name__ == "__main__":
    prompt = "Najnowsze trendy w technologii AI na rok 2025"
    article = generate_article(prompt)
    with open("artykul.txt", "w", encoding="utf-8") as f:
        f.write(article)
