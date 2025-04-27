import sqlite3
import os
import csv
import requests
from io import StringIO

# Chemin vers la base
DB_FILE = os.path.join(os.getcwd(), "data", "analyse_des_ventes.db")

def fetch_csv(url):
    response = requests.get(url)
    response.raise_for_status()
    return list(csv.reader(StringIO(response.text)))[1:]  # On saute l'en-tête


def insert_data(table, rows, insert_query):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Nombre de changements avant l'insertion
    initial_changes = conn.total_changes
    for row in rows:
        cursor.execute(insert_query, row)
    conn.commit()
    # Nombre de changements réels après commit
    inserted = conn.total_changes - initial_changes
    conn.close()
    print(f"{inserted} lignes insérées dans {table}.")


if __name__ == "__main__":
    # Produits
    insert_data(
        "produits",
        fetch_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv"),
        "INSERT OR IGNORE INTO produits (nom, id_reference_produit, prix, stock) VALUES (?, ?, ?, ?)"
    )

    # Magasins
    insert_data(
        "magasins",
        fetch_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv"),
        "INSERT OR IGNORE INTO magasins (id_magasin, ville, nombre_de_salaries) VALUES (?, ?, ?)"
    )

    # Ventes
    insert_data(
        "ventes",
        fetch_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv"),
        "INSERT OR IGNORE INTO ventes (date, id_reference_produit, quantite, id_magasin) VALUES (?, ?, ?, ?)"
    )

    print("L'importation des données est terminée")