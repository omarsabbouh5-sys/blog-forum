from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/create', methods=('GET', 'POST'))
def create():
    conn = get_db_connection()
    if request.method == 'POST':
        # Extraction des données envoyées par le formulaire HTML
        titre = request.form['titre']
        contenu = request.form['contenu']
        categorie_id = request.form['categorie_id']
        conn.execute('''
            INSERT INTO articles (titre, contenu, utilisateur_id, categorie_id)
            VALUES (?, ?, 1, ?)
        ''', (titre, contenu, categorie_id))
        conn.commit()
        conn.close()
        return redirect(url_for('accueil'))
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return render_template('create.html', categories=categories)
if __name__ == '__main__':
    app.run(debug=True)