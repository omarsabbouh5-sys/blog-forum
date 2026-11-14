import sqlite3

def get_db_connection():
    conn = sqlite3.connect('blog_forum.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_utilisateur TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            mot_de_passe TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            contenu TEXT NOT NULL,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            utilisateur_id INTEGER,
            categorie_id INTEGER,
            FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs (id) ON DELETE CASCADE,
            FOREIGN KEY (categorie_id) REFERENCES categories (id) ON DELETE SET NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commentaires (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenu TEXT NOT NULL,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            utilisateur_id INTEGER,
            article_id INTEGER,
            FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs (id) ON DELETE CASCADE,
            FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE
        )
    ''')

    # Ajout de données de test pour avoir du contenu dès le démarrage
    cursor.execute("INSERT OR IGNORE INTO utilisateurs (id, nom_utilisateur, email, mot_de_passe) VALUES (1, 'Admin', 'admin@test.com', '1234')")
    cursor.execute("INSERT OR IGNORE INTO categories (id, nom) VALUES (1, 'Général')")
    cursor.execute("INSERT OR IGNORE INTO articles (id, titre, contenu, utilisateur_id, categorie_id) VALUES (1, 'Bienvenue sur le Forum', 'Ceci est notre tout premier article stocké dans SQLite !', 1, 1)")

    conn.commit()
    conn.close()
    print("Base de données créée et remplie avec succès !")

if __name__ == '__main__':
    init_db()