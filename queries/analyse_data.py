import sqlite3, os

DB_FILE = os.path.join(os.getcwd(), "data", "analyse_des_ventes.db")


def store_analysis_result(type_analyse, valeur, produit, region, date_analyse):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO analyses_resultats (type_analyse, valeur, produit, region, date_analyse)
        VALUES (?, ?, ?, ?, ?)
    """, (type_analyse, valeur, produit, region, date_analyse))
    conn.commit()
    conn.close()


def get_total_chiffre_affaires():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(v.quantite * p.prix) AS chiffre_affaires_total
        FROM ventes v
        JOIN produits p ON v.id_reference_produit = p.id_reference_produit
    """)
    total = cursor.fetchone()[0]
    conn.close()
    return total


def analyse_and_store():
    # Total chiffre d'affaires
    total = get_total_chiffre_affaires()
    store_analysis_result("chiffre_affaires_total", total, "N/A", "N/A", "2025-04-22")

    # Ventes par produit
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nom, SUM(v.quantite) AS total_ventes
        FROM ventes v
        JOIN produits p ON v.id_reference_produit = p.id_reference_produit
        GROUP BY p.nom;
    """)
    for row in cursor.fetchall():
        produit, total_ventes = row
        store_analysis_result("ventes_par_produit", total_ventes, produit, "N/A", "2025-04-22")

    # Ventes par région
    cursor.execute("""
        SELECT m.ville, SUM(v.quantite) AS total_ventes
        FROM ventes v
        JOIN magasins m ON v.id_magasin = m.id_magasin
        GROUP BY m.ville;
    """)
    for row in cursor.fetchall():
        region, total_ventes = row
        store_analysis_result("ventes_par_region", total_ventes, "N/A", region, "2025-04-22")
    conn.close()


if __name__ == "__main__":
    analyse_and_store()

    print("L'analyse des ventes est terminée")