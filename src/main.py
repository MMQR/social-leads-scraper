"""
main.py

Point d'entrée principal pour lancer le pipeline de collecte de leads Instagram.

Utilisation :
    python -m src.main

Tu seras invité à fournir l'URL de ton offre (page de vente, site, etc.)
et le script exécutera le pipeline complet.
"""

from scraper import run_social_leads_pipeline
import csv
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def export_leads_to_csv(leads, filename="leads.csv"):
    """
    Exporte la liste de leads vers un fichier CSV.
    """
    if not leads:
        logger.warning("Aucun lead à exporter.")
        return

    keys = leads[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(leads)
    
    logger.info(f"Leads exportés dans {filename}")


def main():
    """
    Lance le pipeline de collecte de leads.
    """
    print("\n" + "="*60)
    print(" Social Leads Scraper - Pain Points Hunter")
    print("="*60 + "\n")
    
    offer_url = input("🔗 URL de ton offre / page de vente : ").strip()
    
    if not offer_url:
        logger.error("❌ URL requise pour lancer le pipeline.")
        return
    
    print("\n🚀 Démarrage du pipeline...\n")
    
    leads = run_social_leads_pipeline(offer_url)
    
    print("\n" + "="*60)
    print(f" ✅ {len(leads)} leads trouvés")
    print("="*60 + "\n")
    
    if leads:
        # Affiche quelques exemples
        print("👀 Aperçu des premiers leads :\n")
        for i, lead in enumerate(leads[:5], 1):
            print(f"{i}. @{lead['username']} - {lead['source_type']}")
            print(f"   Post: {lead['source_post_url']}")
            print()
        
        # Export CSV
        export_choice = input("💾 Exporter les leads en CSV ? (o/n) : ").strip().lower()
        if export_choice == 'o':
            export_leads_to_csv(leads)
    else:
        print("⚠️ Aucun lead trouvé. Vérifie les mots-clés et pain points définis.")


if __name__ == "__main__":
    main()
