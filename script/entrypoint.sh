set -e

MAX_ATTEMPTS=3
ATTEMPT=1

while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do

    echo "Création de la base de données..."
    python script/create_database.py

    echo "Importation des données..."
    python script/import_data.py

    echo "Exécution des analyses..."
    python queries/analyse_data.py

    # shellcheck disable=SC2181
    if [ $? -eq 0 ]; then
        echo "Toutes les étapes ont été effectuées"
        exit 0
        else
        echo "erreur détectée..."
        sleep 10
        ATTEMPT=$((ATTEMPT + 1))
        fi
done
echo "Trop de tentatives échouées, arrêt du conteneur."
exit 1