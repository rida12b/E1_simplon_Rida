import subprocess
import time
import webbrowser
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_step(step, description):
    print(f"\n{'='*50}")
    print(f"🎯 Étape {step}: {description}")
    print(f"{'='*50}\n")
    time.sleep(1)

def run_command(command, description):
    print(f"📌 {description}")
    print(f"$ {command}\n")
    subprocess.run(command, shell=True)
    input("\n➡️ Appuyez sur Entrée pour continuer...\n")

def main():
    clear_screen()
    print("\n🚀 Démonstration du Projet API Météo\n")
    
    # Étape 1: Structure du projet
    print_step(1, "Structure du Projet")
    run_command("dir" if os.name == 'nt' else "ls -l", "Voici les fichiers du projet:")
    
    # Étape 2: Collecte des données
    print_step(2, "Collecte des Données")
    run_command("python collect_data.py", "Lancement de la collecte des données:")
    
    # Étape 3: Vérification des données
    print_step(3, "Vérification des Données Collectées")
    run_command("type data\\temperatures.csv" if os.name == 'nt' else "cat data/temperatures.csv", 
                "Contenu du fichier CSV:")
    
    # Étape 4: Tests unitaires
    print_step(4, "Exécution des Tests")
    run_command("python test_project.py", "Lancement des tests unitaires:")
    
    # Étape 5: Lancement de l'API
    print_step(5, "Lancement de l'API")
    print("📌 Lancement de l'API (dans un nouveau terminal):")
    print("$ uvicorn api:app --reload")
    
    # Ouvrir le navigateur
    time.sleep(2)
    webbrowser.open('http://localhost:8000/docs')
    
    print("\n✨ Points clés à mentionner pendant la démonstration:")
    print("1. 🔒 Sécurité: Authentification par clé API")
    print("2. 📊 Données: Stockage en CSV et SQLite")
    print("3. 🧪 Tests: Couverture complète")
    print("4. 📚 Documentation: Swagger UI")
    
    input("\n🎤 Démonstration terminée. Appuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main() 