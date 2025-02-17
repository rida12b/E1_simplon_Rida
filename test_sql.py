import sqlite3
import os

# 📂 Connexion à la base SQLite
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "data", "meteo.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 📌 Récupérer les 5 dernières températures enregistrées
cursor.execute("SELECT * FROM temperatures ORDER BY id DESC LIMIT 5")
rows = cursor.fetchall()

conn.close()

# 🔍 Afficher les résultats
print("\n📊 Dernières températures enregistrées :")
for row in rows:
    print(row)
