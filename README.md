# Forecast API

Une API de prévision de séries temporelles flexible et robuste, basée sur **FastAPI** et **Prophet**.

Cette API est conçue pour être facilement intégrée dans des workflows d'automatisation (comme n8n) grâce à sa capacité à comprendre différents formats de données d'entrée.

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.8+
- pip

### Installation

**Étape 1 : Cloner le repository**

```bash
git clone https://github.com/jonathan-dady/forecasting_api.git
cd forecasting_api
```

**Étape 2 : Créer un environnement virtuel**

```powershell
# Windows PowerShell
python -m venv .venv
```

**Étape 3 : Activer l'environnement virtuel**

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

**Étape 4 : Installer les dépendances**

```bash
pip install -r requirements.txt
```

### Lancer le Serveur

**Étape 1 : Activer l'environnement virtuel (si vous en avez un)**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Étape 2 : Lancer Uvicorn**

```powershell
uvicorn app.main:app --reload
```

**Étape 3 : Ouvrir la documentation dans votre navigateur**

L'API sera accessible sur :
- **Documentation Interactive (Swagger)** : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) ← **Testez ici !**
- **Documentation Alternative (ReDoc)** : [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Endpoint API** : `POST http://127.0.0.1:8000/api/v1/forecast`

> **💡 Astuce** : Le flag `--reload` fait redémarrer automatiquement le serveur quand vous modifiez le code.

---

## 🌐 Déploiement en Production (Render)

Cette API est prête à être déployée sur **Render** gratuitement.

### Configuration Render

1. **Créer un nouveau Web Service** sur [Render](https://render.com)
2. **Connecter votre repo GitHub** : `https://github.com/jonathan-dady/forecasting_api`
3. **Configuration** :
   - **Build Command** : `pip install -r requirements.txt` (auto-détecté)
   - **Start Command** : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment** : Laisser vide (aucune variable nécessaire)

4. **Cliquer sur Deploy** et attendre 5-10 minutes

### Votre API sera accessible sur :
- `https://votre-app.onrender.com/docs` (Swagger UI)
- `https://votre-app.onrender.com/api/v1/forecast` (Endpoint API)

### ⚠️ Note sur le plan gratuit
- L'API s'endort après 15 minutes d'inactivité
- Premier appel après le réveil : 30-60 secondes
- 750 heures/mois de disponibilité

### Version Python
Le fichier `.python-version` force l'utilisation de **Python 3.11.11** (compatible avec Prophet).

---

## 📖 Guide d'Utilisation : "Quoi changer pour faire quoi ?"

L'endpoint principal est `POST /api/v1/forecast`.

### 1. Changer l'Horizon de Prévision
Pour prédire plus ou moins loin dans le futur, modifiez le paramètre `horizon`.

```json
{
  "horizon": 12,  // Prédire 12 périodes (ex: 12 mois)
  ...
}
```

### 2. Changer la Fréquence Temporelle
Indiquez l'unité de temps de vos données avec `frequency`.

- `"D"` : Quotidien (Daily)
- `"W"` : Hebdomadaire (Weekly)
- `"M"` : Mensuel (Monthly)
- `"Y"` : Annuel (Yearly)

```json
{
  "frequency": "W", // Mes données sont par semaine
  ...
}
```

### 3. Utiliser des Données aux Formats Variés (Inputs Flexibles)
L'API est intelligente. Elle essaie de deviner quelles colonnes sont les dates et les valeurs.

**Cas A : Format Standard (Recommandé)**
```json
"data": [
  {"ds": "2023-01-01", "y": 100},
  {"ds": "2023-02-01", "y": 120}
]
```

**Cas B : Noms de colonnes explicites (Anglais/Français)**
L'API reconnait automatiquement : `date`, `datetime`, `timestamp`, `value`, `val`, `amount`, `quantity`.
```json
"data": [
  {"date": "2023-01-01", "value": 100},
  {"date": "2023-02-01", "value": 120}
]
```

**Cas C : Noms de colonnes personnalisés**
Si vos colonnes ont des noms exotiques, dites-le à l'API via `date_column` et `value_column`.
```json
{
  "data": [
    {"mon_temps": "2023-01-01", "mon_chiffre": 100}
  ],
  "date_column": "mon_temps",
  "value_column": "mon_chiffre",
  ...
}
```

### 4. Changer de Modèle de Prévision
Par défaut, l'API utilise **Prophet** (`"prophet"`).
*(Note : Le support pour ARIMA est prévu mais pas encore actif)*

```json
{
  "model": "prophet",
  ...
}
```

---

## 🛠 Guide Développeur : Modifier le Code

### Structure du Projet
- `app/domain/models.py` : C'est ici qu'on définit les **formats de données** acceptés (Pydantic). Ajoutez des champs ici si vous voulez passer plus de paramètres (ex: `seasonality_mode`).
- `app/adapters/parsers.py` : C'est ici qu'on gère la **lecture des données**. Modifiez ce fichier pour supporter de nouveaux formats d'entrée bizarres.
- `app/services/forecasting.py` : C'est le **cerveau**. Modifiez ce fichier pour ajuster les hyperparamètres de Prophet ou ajouter un nouveau modèle (ex: scikit-learn, ARIMA).

### Ajouter un nouveau modèle
1. Ajoutez le nom du modèle dans l'Enum `ForecastModel` (`app/domain/models.py`).
2. Dans `app/services/forecasting.py`, ajoutez une condition `if request.model == ...` et implémentez la logique.
