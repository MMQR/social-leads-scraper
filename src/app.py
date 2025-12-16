"""
app.py

Serveur Flask pour l'interface web Pain Points Hunter.
Lance une interface moderne accessible via navigateur.
"""

from flask import Flask, render_template, request, jsonify, send_file
from scraper import run_social_leads_pipeline
import webbrowser
import threading
import csv
import io
import os

app = Flask(__name__)

# Variable globale pour stocker les derniers résultats
last_leads = []

@app.route('/')
def index():
    """Page d'accueil avec interface utilisateur."""
    return render_template('index.html')

@app.route('/api/run_pipeline', methods=['POST'])
def run_pipeline():
    """
    Endpoint API pour lancer le pipeline de scraping.
    """
    global last_leads
    
    data = request.get_json()
    offer_url = data.get('offer_url')
    
    if not offer_url:
        return jsonify({
            'success': False,
            'error': 'URL de l\'offre requise'
        }), 400
    
    try:
        # Lance le pipeline
        leads = run_social_leads_pipeline(offer_url)
        last_leads = leads
        
        return jsonify({
            'success': True,
            'leads_count': len(leads),
            'leads': leads[:20]  # Premiers 20 pour affichage
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export_csv', methods=['GET'])
def export_csv():
    """
    Télécharge les leads en CSV.
    """
    global last_leads
    
    if not last_leads:
        return jsonify({
            'success': False,
            'error': 'Aucun lead à exporter'
        }), 400
    
    # Crée le CSV en mémoire
    output = io.StringIO()
    keys = last_leads[0].keys()
    writer = csv.DictWriter(output, fieldnames=keys)
    writer.writeheader()
    writer.writerows(last_leads)
    
    # Prépare le fichier pour téléchargement
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='leads_instagram.csv'
    )

def open_browser():
    """Ouvre automatiquement le navigateur après 1.5 secondes."""
    import time
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

def main():
    """Point d'entrée principal."""
    print("\n" + "="*60)
    print("🧠 Pain Points Hunter - Interface Web")
    print("="*60)
    print("\n🚀 Serveur démarré sur http://127.0.0.1:5000")
    print("🌐 Ouverture du navigateur...\n")
    
    # Ouvre le navigateur dans un thread séparé
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Lance le serveur Flask
    app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)

if __name__ == '__main__':
    main()
