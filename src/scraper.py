"""
scraper.py

Pipeline principal de collecte de leads Instagram :
1) Analyse de la page de vente / offre => extraction des pain points & mots-clés
2) Recherche de posts Instagram dans la niche
3) Filtre : ne garder que les posts qui expriment le pain point
4) Extraction des comptes (auteur du post, commentateurs, etc.)
5) Export CSV pour ta stratégie outbound / ESP.

Les parties "IA" (analyse de l'offre, matching persona) et "scraping brut"
peuvent être déportées dans d'autres modules.
"""

from typing import List, Dict, Any
import logging

from social_finder import find_engaged_posts_with_pain_point

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# ---------- 1. Analyse de l'offre / page de vente ----------

def analyze_offer(url: str) -> Dict[str, List[str]]:
    """
    Analyse l'URL de ton offre (page de vente, profil Notion, etc.)
    et renvoie :
    - des mots-clés / hashtags pour cibler la niche
    - des expressions de pain point à détecter dans les posts Instagram.

    En pratique, cette fonction sera propulsée par un LLM (OpenAI, etc.).
    Ici, c'est un stub à remplacer.
    """
    # TODO: brancher ton vrai "Pain Points Analyzer" ici
    # Exemple de structure retournée :
    return {
        "search_keywords": [
            "#independants",
            "#freelancefinance",
            "freelance comptable",
        ],
        "pain_points": [
            "problèmes de trésorerie",
            "ne comprend pas ses chiffres",
            "marge trop faible",
        ],
    }


# ---------- 2. Extraction de posts Instagram ----------

def get_pain_point_posts_for_offer(
    offer_url: str,
    min_likes: int = 0,
    min_comments: int = 0,
) -> List[Dict[str, Any]]:
    """
    Pour une offre donnée, récupère les posts Instagram qui expriment le pain point
    du persona ciblé.

    Étapes :
    - Analyse de l'offre => pain_points + search_keywords
    - Scraping Instagram => posts
    - Filtre : posts qui mentionnent explicitement le pain point
    """
    analysis = analyze_offer(offer_url)

    search_keywords = analysis["search_keywords"]
    pain_points = analysis["pain_points"]

    posts = find_engaged_posts_with_pain_point(
        search_keywords=search_keywords,
        pain_point_expressions=pain_points,
        min_likes=min_likes,
        min_comments=min_comments,
    )

    return posts


# ---------- 3. Extraction de comptes depuis les posts ----------

def extract_accounts_from_posts(posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    À partir des posts sélectionnés (qui expriment le pain point), construit
    une liste de comptes à contacter.

    À adapter selon ta stratégie :
    - uniquement l'auteur du post
    - auteur + commentateurs pertinents (via un autre module de scraping)
    """
    leads: List[Dict[str, Any]] = []

    for post in posts:
        # Auteur du post comme lead de base
        leads.append(
            {
                "username": post["username"],
                "source_post_url": post["url"],
                "source_type": "post_author",
                "context_caption": post["caption"],
            }
        )

        # TODO: ajouter ici la récupération des commentateurs
        # via un module du type `instagram_comments_scraper.get_comments(post["url"])`
        # et filtrer les comments qui expriment également le pain point.

    return leads


# ---------- 4. Pipeline complet ----------

def run_social_leads_pipeline(offer_url: str) -> List[Dict[str, Any]]:
    """
    Exécute le pipeline complet pour une offre donnée :
    - détecte les posts Instagram qui expriment le pain point
    - extrait les comptes cibles
    - renvoie une liste de leads structurés.
    """
    logger.info("Démarrage du pipeline de collecte de leads pour %s", offer_url)

    posts = get_pain_point_posts_for_offer(
        offer_url=offer_url,
        min_likes=0,
        min_comments=0,
    )

    logger.info("Nombre de posts avec pain point détecté : %d", len(posts))

    leads = extract_accounts_from_posts(posts)

    logger.info("Nombre de leads extraits : %d", len(leads))

    return leads
