import requests
import pandas as pd
import datetime
import os
import schedule
import time
import sqlite3
from dotenv import find_dotenv, load_dotenv


# Charger les variables d'environnement
env_path = find_dotenv()
if not env_path:
    raise FileNotFoundError("❌ ERREUR : Le fichier `.env` est introuvable ! Vérifie qu'il est bien dans `opendata_meteo/`")

load_dotenv(env_path)
API_KEY = os.getenv("API_KEY")

if API_KEY is None:
    raise ValueError("❌ ERREUR : Clé API introuvable. Vérifie le fichier `.env` et son format.")
# 🔑 Récupérer la clé API depuis .env
API_KEY = os.getenv("API_KEY")

print("🔍 DEBUG : API_KEY chargée =", API_KEY)  # Afficher la clé API chargée

if API_KEY is None:
    raise ValueError("❌ ERREUR : La clé API n'est pas chargée depuis .env ! Vérifie le fichier .env et son format.")
# 🌍 Ville cible
VILLE = "Paris"
API_URL = f"http://api.openweathermap.org/data/2.5/weather?q={VILLE}&appid={API_KEY}&units=metric"

# 📂 Définition des chemins
base_dir = os.path.dirname(os.path.abspath(__file__))  # Récupère le dossier du script
data_dir = os.path.join(base_dir, "data")  # Chemin vers le dossier `data`
file_path = os.path.join(data_dir, "temperatures.csv")  # Fichier CSV
db_path = os.path.join(data_dir, "meteo.db")  # Base de données SQLite

# 📂 Vérifie si le dossier `data/` existe, sinon le créer
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# 📌 Fonction pour récupérer les données météo et les stocker
def collect_weather_data():
    try:
        # 📡 Récupération des données météo
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()

        data = response.json()
        temperature = data['main']['temp']
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 📊 Sauvegarde des données en CSV
        df = pd.DataFrame([[VILLE, date, temperature]], columns=["ville", "date", "temperature"])
        if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
            df.to_csv(file_path, mode="w", header=True, index=False)
        else:
            df.to_csv(file_path, mode="a", header=not os.path.exists(file_path), index=False)


        # 📂 Connexion à la base SQLite et insertion des données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO temperatures (ville, date, temperature) VALUES (?, ?, ?)", 
                       (VILLE, date, temperature))
        conn.commit()
        conn.close()

        print(f"✅ Données enregistrées : {VILLE} | {date} | {temperature}°C (CSV + SQLite)")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion à l'API : {e}")
    except Exception as e:
        print(f"❌ Erreur inconnue : {e}")

# 📌 Exécuter immédiatement la première collecte
collect_weather_data()

# 📅 Planification toutes les heures
schedule.every(1).hours.do(collect_weather_data)

print("🕒 Automatisation activée : collecte toutes les heures...")

# ⏳ Boucle pour exécuter `schedule`
while True:
    schedule.run_pending()
    time.sleep(60)
