# 🧠 Social Intelligence Scraper - Pain Points Hunter

> **Outil d'analyse sociale intelligent** : Trouve automatiquement les personnes ayant les pain points que ton produit résout en analysant leurs interactions sur les réseaux sociaux.

## 🎯 Concept

Au lieu de scraper aveuglément, cet outil **analyse les conversations** autour de ton produit/besoin pour identifier les comptes qui **montrent activement** les pain points que tu résous.

### 💡 Comment ça marche

```
1. Tu donnes une URL (produit/concurrent/article sur le pain point)
   ↓
2. L'IA analyse l'URL et extrait les pain points
   ↓  
3. Le scraper trouve les posts les plus engagés sur ces pain points
   ↓
4. Il lit TOUS les commentaires de ces posts
   ↓
5. Il qualifie chaque commentateur selon ton persona
   ↓
6. Export CSV avec leads ultra-qualifiés
```

## 🏗️ Architecture

```python
┌─────────────────────────────────────────────────┐
│  INPUT: URL du produit/besoin                   │
│  Ex: "https://finance4all.com"                  │
└────────────────┬────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────┐
│  MODULE 1: Pain Points Analyzer (IA)           │
│  • Scrape le contenu de l'URL                   │
│  • ChatGPT extrait les pain points              │
│  • Génère keywords de recherche                 │
└────────────────┬────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────┐
│  MODULE 2: Social Posts Finder                  │
│  • Recherche Instagram/Facebook hashtags        │
│  • Tri par engagement (likes + comments)        │
│  • Sélectionne top 50 posts                     │
└────────────────┬────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────┐
│  MODULE 3: Comments Scraper                     │
│  • Récupère TOUS les commentaires               │
│  • Extrait username, bio, follower count        │
│  • Sauvegarde texte du commentaire              │
└────────────────┬────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────┐
│  MODULE 4: Persona Matcher (IA)                │
│  • ChatGPT analyse chaque commentaire           │
│  • Score de matching avec persona (0-100)       │
│  • Qualification: Hot/Warm/Cold                 │
└────────────────┬────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────┐
│  OUTPUT: leads_qualified.csv                    │
│  • Username, Bio, Followers, Email (si public)  │
│  • Pain point détecté, Score matching           │
│  • Lien vers profil, Prêt pour ESP             │
└─────────────────────────────────────────────────┘
```

## 📦 Stack Technique

```python
# Core
instaloader        # Instagram scraping (robuste)
facebook-scraper   # Facebook posts/comments
beautifulsoup4     # Parsing HTML/URL
openai             # Pain points analysis + matching

# Data
pandas             # CSV manipulation
python-dotenv      # Config

# Rate limiting
time, random       # Human-like delays
proxies-rotation   # Éviter les bans
```

## 🚀 Installation

```bash
git clone https://github.com/MMQR/social-leads-scraper
cd social-leads-scraper
pip install -r requirements.txt

# Config
cp .env.example .env
# Édite .env avec tes credentials
```

## ⚙️ Configuration (.env)

```env
# OpenAI (pour l'analyse IA)
OPENAI_API_KEY=sk-...

# Instagram (optionnel - améliore rate limits)
INSTA_USERNAME=your_username
INSTA_PASSWORD=your_password

# Facebook (via cookies)
FACEBOOK_COOKIES=path/to/cookies.json

# Persona cible (Finance4All exemple)
PERSONA_DESCRIPTION="Entrepreneur PME/TPE, problèmes de trésorerie ou marges, 25-55 ans, secteur retail/e-commerce/services, cherche formation finance accessible"

# Seuils de qualification
MIN_FOLLOWERS=100
MAX_FOLLOWERS=50000
MATCHING_SCORE_MIN=60
```

## 💻 Usage

### Mode Simple (URL unique)

```bash
python scraper.py --url "https://finance4all.com" --limit 200
```

### Mode Avancé (fichier URLs multiples)

```bash
# competitors.txt
https://pennylane.com
https://quickbooks.fr
https://agicap.com

python scraper.py --file competitors.txt --limit 500
```

### Options

```bash
python scraper.py \
  --url "https://finance4all.com" \
  --platforms "instagram,facebook" \
  --limit 300 \
  --min-engagement 50 \
  --output "leads_finance4all.csv" \
  --verbose
```

## 📊 Output CSV

```csv
username,platform,bio,followers,pain_point,matching_score,qualification,profile_url,email,phone,comment_text
jean_pme,instagram,"Entrepreneur e-commerce 🚀",2340,"Problèmes trésorerie",87,HOT,https://instagram.com/jean_pme,jean@...,+33...,"Moi aussi j'ai ce pb avec ma compta..."
marie_retail,facebook,"Gérante boutique Paris",580,"Marges faibles",72,WARM,...
```

## 🔧 Modules détaillés

### 1. `pain_points_analyzer.py`

```python
def analyze_url(url: str) -> dict:
    """
    Analyse une URL et extrait les pain points.
    
    Returns:
        {
            'pain_points': ['trésorerie', 'marges', ...],
            'keywords': ['#comptabilité', '#cashflow', ...],
            'target_accounts': ['@quickbooks', '@pennylane'],
            'persona': {...}
        }
    """
```

### 2. `social_finder.py`

```python
def find_engaged_posts(keywords: list, platform: str) -> list:
    """
    Trouve les posts les plus engagés.
    
    Args:
        keywords: Liste de hashtags/mots-clés
        platform: 'instagram' ou 'facebook'
    
    Returns:
        [{'post_id': '...', 'engagement': 450, 'url': '...'}, ...]
    """
```

### 3. `comments_scraper.py`

```python
def scrape_comments(post_url: str) -> list:
    """
    Récupère tous les commentaires d'un post.
    
    Returns:
        [
            {
                'username': 'jean_pme',
                'text': 'Moi aussi j'ai ce problème...',
                'likes': 12,
                'replies': 3,
                'profile_data': {...}
            },
            ...
        ]
    """
```

### 4. `persona_matcher.py`

```python
def match_persona(comment_data: dict, persona: dict) -> dict:
    """
    Utilise ChatGPT pour scorer le matching.
    
    Returns:
        {
            'score': 87,
            'qualification': 'HOT',
            'pain_point_detected': 'Problèmes trésorerie',
            'reasoning': 'Mentionne explicitement...'
        }
    """
```

## 🎯 Exemple concret Finance4All

```bash
# Input
python scraper.py --url "https://agicap.com/fr/blog/problemes-tresorerie"

# Le programme va:
# 1. Lire l'article sur les problèmes de trésorerie
# 2. Extraire pain points: "trésorerie négative", "prévisions imprécises", etc.
# 3. Chercher posts Instagram/Facebook avec #trésorerie #comptabilité #pme
# 4. Lire commentaires où les gens disent "moi aussi j'ai ce pb"
# 5. Qualifier les commentateurs (entrepreneurs? secteur? taille?)
# 6. Exporter uniquement ceux qui matchent ton persona Finance4All

# Output: 150 leads ultra-qualifiés qui ont ACTIVEMENT dit avoir ton pain point
```

## 🛡️ Rate Limiting & Sécurité

```python
# Delays humains
MIN_DELAY = 2  # secondes entre requêtes
MAX_DELAY = 8
COMMENTS_DELAY = 10  # pause après chaque post

# Rotation proxies (optionnel)
PROXY_LIST = ['proxy1:port', 'proxy2:port']

# Max requests/heure
MAX_REQUESTS_PER_HOUR = 200
```

## ⚠️ Limitations légales

- ✅ **Lecture publique** : Les posts/commentaires publics sont scrapables (zone grise)
- ⚠️ **Rate limits** : Respecte les délais pour éviter les bans
- ❌ **Données privées** : N'accède JAMAIS aux contenus privés
- ⚠️ **RGPD** : Les données collectées doivent être utilisées conformément au RGPD

## 📈 Résultats attendus

| Metric | Valeur |
|--------|--------|
| Posts analysés | 50-100 |
| Commentaires scrapés | 2000-5000 |
| Leads qualifiés (score >60) | 150-300 |
| Hot leads (score >80) | 30-50 |
| Taux de conversion estimé | 5-10% |
| Coût par lead | 0€ (vs 2-5€ Lead Ads) |

## 🚀 Prochaines features

- [ ] TikTok scraping (commentaires vidéos)
- [ ] LinkedIn posts (via API)
- [ ] Auto-DM warm leads (avec templates)
- [ ] Dashboard Notion (sync auto)
- [ ] Webhook vers MailerLite

## 🤝 Contribution

Ce repo est open source (MIT). PRs bienvenues !

## 📄 Licence

MIT © 2025 Finance4All


## 🐍 Utilisation Python

Le code Python implémente la logique "scanner les posts Instagram et ne garder que ceux qui expriment le pain point ciblé, sur la base d'une liste de mots-clés et d'expressions définie par l'utilisateur".

### Installation

```bash
git clone https://github.com/MMQR/social-leads-scraper.git
cd social-leads-scraper
```

### Utilisation

Lance le pipeline avec :

```bash
python -m src.main
```

Tu seras invité à :
1. Fournir l'URL de ton offre / page de vente
2. Le script analysera le contenu pour identifier les pain points
3. Recherchera les posts Instagram correspondants
4. Filtrera uniquement les posts qui expriment explicitement le pain point
5. Extraira les comptes cibles (auteurs des posts)
6. Proposera d'exporter les leads en CSV

### Architecture

```
src/
├── social_finder.py    # Module de recherche et filtrage des posts Instagram
├── scraper.py          # Pipeline principal (analyse offre + extraction leads)
└── main.py             # Point d'entrée CLI avec export CSV
```

### Prochaines étapes

1. **Brancher l'API de scraping Instagram** : Remplace `_fetch_instagram_posts_for_keywords()` dans `social_finder.py` par ton provider (Apify, Data365, etc.)
2. **Brancher l'analyseur de pain points** : Remplace `analyze_offer()` dans `scraper.py` par un appel à un LLM (OpenAI, etc.)
3. **Ajouter le scraping de commentaires** : Complète `extract_accounts_from_posts()` pour récupérer aussi les commentateurs


---

**Made with 🧠 by Finance4All Team** | Projet Jericho 2025
