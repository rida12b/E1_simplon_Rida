import pandas as pd
import os
import sqlite3

print("🔄 Démarrage du nettoyage des données...")  # ✅ Ajout d'un message pour voir si ça tourne

# 📂 Définition des chemins
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "data", "temperatures.csv")
db_path = os.path.join(base_dir, "data", "meteo.db")

# 📌 Nettoyage des données CSV
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    df.drop_duplicates(inplace=True)  
    df = df[df["temperature"] > -50]  
    df.to_csv(file_path, index=False)
    print("✅ Fichier CSV nettoyé !")  # ✅ Ajout de confirmation
else:
    print("⚠️ Aucun fichier CSV trouvé !")

# 📌 Nettoyage des données SQL
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM temperatures WHERE temperature < -50")
    conn.commit()
    conn.close()
    print("✅ Base de données SQL nettoyée !")  # ✅ Ajout de confirmation
else:
    print("⚠️ Aucun fichier SQL trouvé !")

print("✅ Nettoyage terminé !")  # ✅ Message final
