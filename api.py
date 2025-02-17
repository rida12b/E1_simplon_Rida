from fastapi import FastAPI, Query, HTTPException
from datetime import datetime, timedelta
import sqlite3
import os
from typing import Optional, List
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

# 📊 Modèle de données pour la réponse
class Temperature(BaseModel):
    ville: str
    date: str
    temperature: float

# 📚 Création de l'application avec documentation
app = FastAPI(
    title="API Meteo",
    description="API de consultation des temperatures collectees via OpenWeatherMap",
    version="1.0.0",
    docs_url=None,  # On désactive l'URL par défaut
    redoc_url=None  # On désactive l'URL RedDoc par défaut
)

# Configuration personnalisée de l'OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API Meteo",
        version="1.0.0",
        description="API de consultation des temperatures",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Route personnalisée pour la documentation Swagger
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API Meteo - Documentation",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )

# 🔒 Middleware CORS et sécurité
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 🔒 Middleware pour les hôtes de confiance
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)

# 📂 Définition du chemin de la base SQLite
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "data", "meteo.db")

@app.get("/", tags=["Informations"])
async def root():
    """
    Page d'accueil de l'API avec informations de base.
    """
    return {
        "nom": "API Meteo",
        "version": "1.0.0",
        "endpoints": [
            "/temperature/{ville} - Derniere temperature",
            "/temperatures/{ville} - Historique des temperatures avec filtres"
        ]
    }

@app.get("/temperature/{ville}", response_model=Temperature, tags=["Temperatures"])
async def get_temperature(ville: str):
    """
    Récupère la dernière température enregistrée pour une ville.
    
    Args:
        ville (str): Nom de la ville (ex: Paris)
        
    Returns:
        Temperature: Dernière température enregistrée
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT date, temperature FROM temperatures WHERE ville = ? ORDER BY date DESC LIMIT 1", 
        (ville,)
    )
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {"ville": ville, "date": result[0], "temperature": result[1]}
    else:
        raise HTTPException(status_code=404, detail="Donnees non trouvees")

@app.get("/temperatures/{ville}", response_model=List[Temperature], tags=["Temperatures"])
async def get_temperatures(
    ville: str,
    start_date: Optional[str] = Query(None, description="Date de debut (format: YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Date de fin (format: YYYY-MM-DD)")
):
    """
    Récupère l'historique des températures pour une ville avec filtres de dates optionnels.
    
    Args:
        ville (str): Nom de la ville (ex: Paris)
        start_date (str, optional): Date de début au format YYYY-MM-DD
        end_date (str, optional): Date de fin au format YYYY-MM-DD
        
    Returns:
        List[Temperature]: Liste des températures enregistrées
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = "SELECT date, temperature FROM temperatures WHERE ville = ?"
    params = [ville]
    
    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
        
    query += " ORDER BY date DESC"
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    if results:
        return [{"ville": ville, "date": result[0], "temperature": result[1]} for result in results]
    else:
        return []
