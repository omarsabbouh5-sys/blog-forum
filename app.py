from flask import Flask, render_template
from database import get_db_connection

app = Flask(__name__)

@app.route('/')
def accueil():
    conn = get_db_connection()
    articles = conn.execute('''
        SELECT articles.*, utilisateurs.nom_utilisateur, categories.nom AS categorie_nom
        FROM articles
        LEFT JOIN utilisateurs ON articles.utilisateur_id = utilisateurs.id
        LEFT JOIN categories ON articles.categorie_id = categories.id
        ORDER BY articles.date_creation DESC
    ''').fetchall()
    conn.close()
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)