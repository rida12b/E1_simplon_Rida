import sqlite3
import os

# 📂 Définition du chemin de la base de données
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "data", "meteo.db")

# 🔗 Connexion à SQLite (crée la base si elle n'existe pas)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 📌 Création de la table pour stocker les températures
cursor.execute("""
    CREATE TABLE IF NOT EXISTS temperatures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ville TEXT,
        date TEXT,
        temperature REAL
    )
""")

conn.commit()
conn.close()
print("✅ Base de données SQLite créée avec succès !")
