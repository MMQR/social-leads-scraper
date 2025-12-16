"""
social_finder.py

Module chargé d'interroger Instagram à partir d'une liste de mots-clés / hashtags
et de renvoyer une liste de posts publics pertinents.

Chaque post retourné contient :
- les métadonnées de base (id, url, auteur, date)
- le contenu texte analysable (légende + hashtags + éventuel texte OCR)
- des métriques d'engagement (likes, commentaires)

L'API de scraping réelle (Apify, Data365, lib custom, etc.) doit être branchée
dans la fonction `_fetch_instagram_posts_for_keywords`.
"""

from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _fetch_instagram_posts_for_keywords(keywords: List[str]) -> List[Dict[str, Any]]:
    """
    Point d'intégration unique avec ton outil de scraping Instagram.
    À adapter selon la stack (Apify Actor, API custom, Selenium, etc.).

    Args:
        keywords: Liste de hashtags / mots-clés à rechercher sur Instagram.

    Returns:
        Liste de posts bruts (structure dépend de ton provider).
    """
    # TODO: brancher ici la vraie source de données (Apify, Data365, etc.)
    # Exemple d'interface cible (à respecter dans la fonction de mapping plus bas) :
    # [
    #   {
    #       "id": "...",
    #       "url": "https://www.instagram.com/p/XXX/",
    #       "username": "compte_exemple",
    #       "caption": "Texte de la légende",
    #       "hashtags": ["#hashtag1", "#hashtag2"],
    #       "likes": 120,
    #       "comments_count": 15,
    #       "timestamp": "2025-12-16T19:45:00Z",
    #       "image_url": "https://...",
    #       "image_text": None  # si tu ajoutes un module OCR plus tard
    #   },
    #   ...
    # ]
    logger.warning(
        "⚠️ _fetch_instagram_posts_for_keywords doit être implémentée avec "
        "ta solution de scraping réelle."
    )
    return []


def _normalize_post(raw_post: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalise un post brut en un schéma stable utilisé par le reste de l'appli.
    """
    hashtags = raw_post.get("hashtags") or []
    if isinstance(hashtags, str):
        hashtags = [h.strip() for h in hashtags.split() if h.strip().startswith("#")]

    return {
        "post_id": raw_post.get("id"),
        "url": raw_post.get("url"),
        "username": raw_post.get("username"),
        "caption": raw_post.get("caption") or "",
        "hashtags": hashtags,
        "image_text": raw_post.get("image_text") or "",
        "likes": raw_post.get("likes") or 0,
        "comments_count": raw_post.get("comments_count") or 0,
        "timestamp": raw_post.get("timestamp"),
        "raw": raw_post,
    }


def find_engaged_posts_with_pain_point(
    search_keywords: List[str],
    pain_point_expressions: List[str],
    min_likes: int = 0,
    min_comments: int = 0,
) -> List[Dict[str, Any]]:
    """
    Trouve les posts Instagram qui :
    1) correspondent aux mots-clés / hashtags fournis (search_keywords)
    2) mentionnent explicitement le pain point ciblé
       (pain_point_expressions dans légende / hashtags / texte image)
    3) respectent les seuils d'engagement minimal.

    Args:
        search_keywords: Liste de mots-clés ou hashtags pour trouver des posts
                         dans la niche (ex: ['#pme', '#freelancecompta']).
        pain_point_expressions: Liste de formulations du pain point
                         (ex: ['problèmes de trésorerie', 'marge trop faible']).
        min_likes: Seuil minimal de likes pour filtrer les posts.
        min_comments: Seuil minimal de commentaires pour filtrer les posts.

    Returns:
        Liste de posts normalisés qui expriment le pain point ciblé.
    """
    logger.info(
        "Recherche de posts Instagram avec keywords=%s et pain_points=%s",
        search_keywords,
        pain_point_expressions,
    )

    raw_posts = _fetch_instagram_posts_for_keywords(search_keywords)
    normalized_posts = [_normalize_post(p) for p in raw_posts]

    pain_point_posts: List[Dict[str, Any]] = []

    lower_pain_points = [p.lower() for p in pain_point_expressions]

    for post in normalized_posts:
        text_blob = " ".join(
            [
                post.get("caption", ""),
                " ".join(post.get("hashtags", [])),
                post.get("image_text", ""),
            ]
        ).lower()

        # Filtre #1 : le post doit exprimer au moins une des expressions du pain point
        if not any(expr in text_blob for expr in lower_pain_points):
            continue

        # Filtre #2 : engagement minimal
        if post["likes"] < min_likes or post["comments_count"] < min_comments:
            continue

        pain_point_posts.append(post)

    logger.info("Posts sélectionnés (pain point détecté) : %d", len(pain_point_posts))
    return pain_point_posts
