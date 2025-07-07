# Automatyczna Publikacja Artykułów

## Ustawienia
1. Stwórz repo na GitHub.
2. Dodaj Secret `HUGGINGFACE_TOKEN` w ustawieniach repo.

## Struktura
- `generate_content.py` — generuje pliki MD
- `content/` — katalog z wpisami
- `.github/workflows/deploy.yml` — CI uruchamiany o 08:00 UTC
- `config.yaml` — lista tematów artykułów

## Jak zacząć

### 1. Sklonuj swoje repozytorium
```bash
git clone https://github.com/<TwojaNazwa>/<TwojeRepo>.git
cd <TwojeRepo>
```

### 2. Dodaj pliki projektu
W folderze głównym repo utwórz (lub skopiuj) następującą strukturę:
```
.github/workflows/deploy.yml
config.yaml
generate_content.py
requirements.txt
README.md
content/        ← Puste na początek
```

### 3. Skonfiguruj tematykę
Edytuj `config.yaml`, podając swoje tematy artykułów:
```yaml
topics:
  - "Twój pierwszy temat"
  - "Kolejny temat"
```

### 4. Zainstaluj zależności lokalnie (opcjonalnie)
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Pierwsze ręczne uruchomienie (test)
```bash
python generate_content.py
```
Sprawdź, czy w katalogu `content/` pojawiły się nowe pliki markdown.

### 6. Commit i Push
```bash
git add .
git commit -m "Initial project setup"
git push origin main
```

Po `git push`, GitHub Actions automatycznie uruchomi workflow o 08:00 UTC i opublikuje nowe wpisy.
