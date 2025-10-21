# ✅ GitHub Upload Checklist

## 🔒 SIKKERHED - Tjek FØR Upload!

### 1. API Nøgler (KRITISK!)

**✅ Sikker:**
- `.env` fil er i `.gitignore` ✓
- `.env.template` har INGEN rigtig API key ✓

**❌ FARLIGT - Tjek disse:**
- [ ] Ingen API nøgler i kode filer
- [ ] Ingen passwords eller tokens
- [ ] `.env` fil er IKKE inkluderet

**Hvordan tjekker du:**
```bash
# Søg efter API keys i koden
findstr /s "AIza" *.py
# Hvis den finder noget → FJERN DET!
```

### 2. Personlige Data

**Beskyttet i .gitignore:**
- `knowledge_base/` - Dine print erfaringer ✓
- `generated_profiles/` - Dine genererede profiler ✓
- `chroma_db/` - Vector database ✓
- `elegoo_default_settings.json` - Dine Elegoo settings ✓
- `*.3mf`, `*.stl`, `*.obj` - Dine 3D modeller ✓

### 3. Test og Debug Filer

**Automatisk ignoreret:**
- `test_*.py`
- `debug_*.py`
- `compare_*.py`
- `check_*.py`
- Alle debug scripts ✓

### 4. Hvad SKAL Uploades

**✅ Disse filer er sikre at dele:**
- [ ] `*.py` (alle Python source filer)
- [ ] `requirements.txt`
- [ ] `README.md` og andre .md filer
- [ ] `.gitignore`
- [ ] `.env.template` (template, IKKE .env!)
- [ ] `config.py` (ingen API keys her)

## 🧹 Cleanup FØR Upload

### Trin 1: Fjern Sensitive Filer

Kør dette script for at rydde op:

```bash
# Lav en ny terminal og kør:
python cleanup_for_github.py
```

### Trin 2: Tjek for API Keys

```bash
# Søg efter "GOOGLE_API_KEY" i filer
findstr /s "GOOGLE_API_KEY.*=" *.py

# Skal kun findes i:
# - config.py (loader fra env)
# - Ikke hardcoded værdier!
```

### Trin 3: Verificer .gitignore

Sikker dig at `.gitignore` eksisterer og indeholder:
- `.env`
- `knowledge_base/`
- `generated_profiles/`
- `chroma_db/`
- `elegoo_default_settings.json`
- `*.3mf`

## 📋 Upload Steps

### 1. Init Git Repository (hvis ikke gjort)

```bash
git init
git add .
git commit -m "Initial commit: AI 3D Print Profile Generator for Elegoo"
```

### 2. Opret Repository på GitHub

1. Gå til github.com
2. Click "New repository"
3. Navn: "ai-elegoo-slicer-profile-generator"
4. Description: "AI-powered 3D print profile generator for Elegoo Orca Slicer"
5. **Vælg Public eller Private**
6. **IKKE** check "Add README" (vi har allerede)
7. Click "Create repository"

### 3. Push til GitHub

```bash
git remote add origin https://github.com/DIT_BRUGERNAVN/ai-elegoo-slicer-profile-generator.git
git branch -M main
git push -u origin main
```

## ⚠️ ADVARSEL: Tjek ALTID Før Push!

**KØR DETTE FØR HVER PUSH:**

```bash
# Tjek hvilke filer der vil uploades
git status

# Se ændringer
git diff

# Tjek for API keys
findstr /s "AIza" *.py
```

## 🔐 Hvis Du Ved Et Uheld Uploader API Key

**OMGÅENDE:**
1. Gå til https://makersuite.google.com/app/apikey
2. Slet den kompromitterede API key
3. Generer en ny
4. Opdater din lokale `.env` fil
5. Fjern API key fra GitHub history (eller slet repository og start forfra)

## ✅ Final Checklist

Før upload, verificer:

- [ ] `.env` fil findes IKKE i upload
- [ ] `elegoo_default_settings.json` findes IKKE i upload
- [ ] Ingen `.3mf` modeller i upload
- [ ] Ingen personlige data i `knowledge_base/`
- [ ] `.gitignore` filen er inkluderet
- [ ] `.env.template` findes (UDEN rigtig API key)
- [ ] README.md forklarer hvordan man får API key
- [ ] Koden virker lokalt

## 📄 Anbefalede GitHub Filer

Inkluder disse i din README.md:

```markdown
## Setup
1. Clone repository
2. pip install -r requirements.txt
3. Copy .env.template to .env
4. Add your Google Gemini API key to .env
5. python app.py

## License
MIT

## Disclaimer
This is a community tool. Not affiliated with Elegoo.
```

## 🎯 Klar til Upload?

Når du har tjekket ALT ovenstående:

1. ✅ Ingen API keys i koden
2. ✅ .gitignore beskytter sensitive filer
3. ✅ .env.template er sikker
4. ✅ Test filer er ignoreret

**Du er klar til at uploade!** 🚀

