# 🌡️ API Météo OpenData

## 📝 Description
API de collecte et de consultation des données météorologiques pour différentes villes, utilisant l'API OpenWeatherMap.

## 🚀 Fonctionnalités
- Collecte automatique des températures
- Stockage en CSV et SQLite
- API REST sécurisée
- Filtrage par date
- Nettoyage automatique des données

## 🛠️ Installation

1. Cloner le projet :
```bash
git clone [URL_DU_PROJET]
cd opendata_meteo
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer l'environnement :
- Créer un fichier `.env` à la racine du projet
- Ajouter votre clé API OpenWeatherMap :
```env
API_KEY=votre_clé_api_openweathermap
```

## 🔧 Configuration

### Base de données
- SQLite : `data/meteo.db`
- CSV : `data/temperatures.csv`

### Scripts
- `collect_data.py` : Collecte des données
- `store_data.py` : Gestion de la base de données
- `clean_data.py` : Nettoyage des données
- `api.py` : API REST
- `test_project.py` : Tests unitaires et d'intégration

## 📡 Utilisation de l'API

### Authentification
L'API nécessite une clé d'authentification. Ajoutez l'en-tête `X-API-Key` à vos requêtes :
```
X-API-Key: votre_clé_api_secrète
```

### Endpoints

1. **GET /** : Page d'accueil
```bash
curl http://localhost:8000/
```

2. **GET /temperature/{ville}** : Dernière température
```bash
curl -H "X-API-Key: votre_clé_api_secrète" http://localhost:8000/temperature/Paris
```

3. **GET /temperatures/{ville}** : Historique des températures
```bash
curl -H "X-API-Key: votre_clé_api_secrète" "http://localhost:8000/temperatures/Paris?start_date=2024-01-01&end_date=2024-12-31"
```

## 🔒 Sécurité et RGPD

### Sécurité
- Authentification par clé API
- En-têtes de sécurité HTTP
- Protection CORS
- Validation des entrées

### RGPD
1. **Données collectées**
   - Ville
   - Date et heure
   - Température
   - Aucune donnée personnelle n'est collectée

2. **Stockage**
   - Données stockées localement
   - Pas de transfert vers des serveurs tiers
   - Conservation illimitée pour analyse historique

3. **Accès aux données**
   - API sécurisée par authentification
   - Logs d'accès anonymisés
   - Pas de tracking des utilisateurs

4. **Droits des utilisateurs**
   - Données publiques et non personnelles
   - Pas de nécessité de consentement RGPD
   - Pas de données à caractère personnel

## 🧪 Tests

Lancer les tests :
```bash
python test_project.py
```

## 📊 Performances
- Collecte toutes les heures
- Temps de réponse API < 100ms
- Cache des requêtes fréquentes
- Optimisation des requêtes SQL

## 📝 Licence
MIT License - Voir le fichier LICENSE pour plus de détails.
