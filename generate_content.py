import os
import sys
import yaml
import frontmatter
from datetime import datetime
from huggingface_hub import InferenceApi

# === KONFIGURACJA ===
CFG_PATH = 'config.yaml'
CONTENT_DIR = 'content'
MODEL = 'google/flan-t5-small'
HF_TOKEN_ENV = 'HUGGINGFACE_TOKEN'
WORD_COUNT = 600

def load_config(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def generate_article(topic, api):
    prompt = (
        f"Napisz wyczerpujący artykuł o temacie: \"{topic}\" "
        f"długości około {WORD_COUNT} słów, z podtytułami i wprowadzeniem."
    )
    response = api(prompt)
    return response.get('generated_text')

def save_markdown(title, content):
    date_str = datetime.now().strftime('%Y-%m-%d')
    slug = title.lower().replace(' ', '-')
    filename = f"{date_str}-{slug}.md"
    post = frontmatter.Post(content)
    post['title'] = title
    post['date'] = datetime.now().isoformat()
    os.makedirs(CONTENT_DIR, exist_ok=True)
    path = os.path.join(CONTENT_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        frontmatter.dump(post, f)
    print(f"Saved article: {path}")

def main():
    cfg = load_config(CFG_PATH)
    token = os.getenv(HF_TOKEN_ENV)
    if not token:
        print(f"Error: Ustaw zmienną środowiskową {HF_TOKEN_ENV}.")
        sys.exit(1)

    api = InferenceApi(repo_id=MODEL, token=token)

    for topic in cfg['topics']:
        print(f"Generating for: {topic}")
        txt = generate_article(topic, api)
        save_markdown(topic, txt)

if __name__ == '__main__':
    main()
