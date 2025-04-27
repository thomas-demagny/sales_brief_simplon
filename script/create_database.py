import sqlite3

connect = sqlite3.connect('data/analyse_des_ventes.db')
cursor = connect.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS produits (
    id_produit INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    id_reference_produit TEXT NOT NULL UNIQUE,
    prix REAL NOT NULL,
    stock INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS magasins (
    id_magasin INTEGER PRIMARY KEY,
    ville TEXT NOT NULL,
    nombre_de_salaries INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ventes (
    id_vente INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    id_reference_produit TEXT NOT NULL,
    quantite INTEGER NOT NULL,
    id_magasin INTEGER NOT NULL,
    FOREIGN KEY (id_reference_produit) REFERENCES produits(id_reference_produit) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_magasin) REFERENCES magasins(id_magasin) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE(date, id_reference_produit, id_magasin)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS analyses_resultats (
    id_resultat INTEGER PRIMARY KEY AUTOINCREMENT,
    type_analyse TEXT NOT NULL,
    valeur REAL NOT NULL,
    produit TEXT NOT NULL,
    region TEXT NOT NULL,
    date_analyse TEXT NOT NULL
)
''')

connect.commit()
connect.close()

print("La base de données et les tables ont été créées.")