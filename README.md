# 🌡️ API Météo OpenData

## 📝 Description
API de collecte et de consultation des données météorologiques pour différentes villes, utilisant l'API OpenWeatherMap.

## 🚀 Fonctionnalités
- ✅ Collecte automatique des températures
- ✅ Stockage en CSV et SQLite
- ✅ API REST avec FastAPI
- ✅ Filtrage par date
- ✅ Nettoyage automatique des données
- ✅ Tests unitaires et d'intégration
- ✅ Documentation Swagger

## 🛠️ Installation

1. Cloner le projet :
```bash
git clone https://github.com/rida12b/E1_simplon_Rida.git
cd E1_simplon_Rida
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer l'environnement :
- Copier `.env.example` vers `.env`
- Modifier les variables dans `.env` avec vos valeurs
```bash
cp .env.example .env
```

## 🔧 Structure du Projet

```
opendata_meteo/
├── data/                  # Données collectées
│   ├── temperatures.csv   # Données au format CSV
│   └── meteo.db          # Base SQLite
├── api.py                # API FastAPI
├── collect_data.py       # Script de collecte
├── clean_data.py         # Nettoyage des données
├── store_data.py         # Gestion de la BDD
├── test_project.py       # Tests unitaires
└── requirements.txt      # Dépendances
```

## 📡 Utilisation

### 1. Collecte des Données
```bash
python collect_data.py
```
- Collecte automatique toutes les heures
- Stockage en CSV et SQLite
- Logs dans `data/collect.log`

### 2. Lancement de l'API
```bash
uvicorn api:app --reload
```
- Documentation Swagger : http://localhost:8000/docs
- Endpoints :
  - GET `/temperature/{ville}` : Dernière température
  - GET `/temperatures/{ville}` : Historique avec filtres

### 3. Tests
```bash
python test_project.py
```
- Tests unitaires
- Tests d'intégration
- Tests de la base de données

## 🔒 Sécurité

### Protection des Données
- Pas de données personnelles collectées
- Validation des entrées
- Protection CORS configurée
- Logs anonymisés

### Bonnes Pratiques
- Variables sensibles dans `.env`
- Validation des données
- Gestion des erreurs
- Documentation des endpoints

## 📊 Maintenance

### Nettoyage des Données
```bash
python clean_data.py
```
- Suppression des doublons
- Validation des températures
- Formatage des dates

### Logs et Monitoring
- Logs de collecte dans `data/collect.log`
- Logs d'API dans `data/api.log`
- Monitoring des erreurs

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 License
MIT License - Voir le fichier LICENSE pour plus de détails.

## 🙏 Remerciements
- OpenWeatherMap pour l'API météo
- FastAPI pour le framework
- SQLite pour la base de données
