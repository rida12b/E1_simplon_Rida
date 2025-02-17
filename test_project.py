import unittest
import os
import sqlite3
from datetime import datetime, timedelta
import requests
from fastapi.testclient import TestClient
from api import app, API_KEY

class TestWeatherProject(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Initialisation des tests"""
        cls.client = TestClient(app)
        cls.base_dir = os.path.dirname(os.path.abspath(__file__))
        cls.data_dir = os.path.join(cls.base_dir, "data")
        cls.csv_path = os.path.join(cls.data_dir, "temperatures.csv")
        cls.db_path = os.path.join(cls.data_dir, "meteo.db")
        cls.api_key = API_KEY
        
        # Vérifier que le dossier data existe
        if not os.path.exists(cls.data_dir):
            os.makedirs(cls.data_dir)
            print("✅ Dossier data créé")

    def test_project_structure(self):
        """Test de la structure du projet"""
        self.assertTrue(os.path.exists("api.py"), "api.py doit exister")
        self.assertTrue(os.path.exists(".env"), "Fichier .env doit exister")
        self.assertTrue(os.path.exists("data"), "Dossier data doit exister")
        
    def test_env_file(self):
        """Test du fichier .env"""
        with open(".env", "r") as f:
            content = f.read()
        self.assertIn("API_KEY=", content, "API_KEY doit etre definie dans .env")
        
    def test_database_structure(self):
        """Test de la structure de la base de donnees"""
        self.assertTrue(os.path.exists(self.db_path), "Base de donnees doit exister")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='temperatures'")
        self.assertIsNotNone(cursor.fetchone(), "Table temperatures doit exister")
        
        cursor.execute("PRAGMA table_info(temperatures)")
        columns = {row[1] for row in cursor.fetchall()}
        expected_columns = {"ville", "date", "temperature"}
        self.assertTrue(expected_columns.issubset(columns), "Colonnes requises manquantes")
        
        conn.close()
        
    def test_api_endpoints(self):
        """Test des endpoints de l'API"""
        # Test sans clé API
        response = self.client.get("/temperature/Paris")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "Cle API manquante")
        
        # Test avec clé API invalide
        headers = {"X-API-Key": "invalid_key"}
        response = self.client.get("/temperature/Paris", headers=headers)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["detail"], "Cle API invalide")
        
        # Test avec clé API valide
        headers = {"X-API-Key": self.api_key}
        response = self.client.get("/", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("endpoints", response.json())
        
    def test_security_headers(self):
        """Test des en-têtes de sécurité"""
        headers = {"X-API-Key": self.api_key}
        response = self.client.get("/", headers=headers)
        
        security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'"
        }
        
        for header, value in security_headers.items():
            self.assertEqual(
                response.headers.get(header),
                value,
                f"L'en-tete {header} est manquant ou incorrect"
            )

if __name__ == "__main__":
    print("\n🌡️ Tests du projet meteo...\n")
    unittest.main(verbosity=2) 