from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from datetime import datetime
import os
import torch
import random

# Setup
today = datetime.now().strftime("%Y-%m-%d")
prompt = f"Nowości w świecie technologii na dzień {today}. Napisz profesjonalny artykuł w stylu magazynu naukowego."

seed = random.randint(1000, 9999)
print(f"Using seed: {seed}")

tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.2",
    torch_dtype=torch.float16,
    device_map="auto"
)

generator = pipeline("text-generation", model=model, tokenizer=tokenizer, seed=seed)

result = generator(
    prompt,
    max_new_tokens=500,
    do_sample=True,
    top_k=50,
    top_p=0.95,
    temperature=0.9,
    num_return_sequences=1
)[0]["generated_text"]

# Zapis do pliku
filename = f"article-{today}-{seed}.md"
os.makedirs("articles", exist_ok=True)
with open(f"articles/{filename}", "w", encoding="utf-8") as f:
    f.write(f"# AI Article ({today})\n\n")
    f.write(result)
