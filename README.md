Pour ce TP, j'ai développé un agent conversationnel financier avec LangChain. L'agent peut interroger une base de données PostgreSQL, récupérer des cours boursiers en temps réel, faire des calculs financiers et chercher des informations sur le web.

## Ce que j'ai implémenté

1. Base de données PostgreSQL
2. Cours boursiers réels grâce à yfinance
3. Recherche web à l'aide de TavilySearch
4. Calcul de portefeuille boursier
5. PythonREPLTool
6. Une interface Streamlit
7. La possibilité d'avoir une mémoire conversationnelle à l'aide de ConversationBufferMemory
8. API REST FastAPI

## Prérequis pour ce projet

- Python 3.10+
- Docker pour utiliser PostgreSQL
- Une clé API OpenAI
- Une clé API Tavily

## Installation et test du projet

Pour commencer, il faut cloner le projet :
```bash
git clone 
cd tp_projet
```

Ensuite, il faut créer et activer le venv :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

Puis, nous installons les dépendances nécessaires pour le projet :
```bash
pip install -r requirements.txt
```

Maintenant, nous allons configurer les variables d'environnement :
```bash
cp .env.example .env
```

Ouvre le `.env` et remplis tes clés API

**Voici un exemple d'un fichier .env :**
```bash
# Clé API OpenAI
OPENAI_API_KEY=your_openai_api_key_here
# Clé API Tavily
TAVILY_API_KEY=your_tavily_api_key_here
# Base de données PostgreSQL
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/tp_langchain
```

## Lancement de PostgreSQL avec Docker

```bash
docker-compose up -d
```

**Pour vérifier si Docker est bien lancé :**
```bash
docker ps
```

La base de données et les tables sont créées automatiquement au premier lancement.

Nous pouvons commencer la partie test du projet. Pour commencer, nous devons lancer l'application :

**Menu interactif dans le terminal :**
```bash
python main.py
```

**Interface web Streamlit :**
```bash
streamlit run app.py
```

**API REST :**
```bash
uvicorn api:app --reload
```

## Comment tester

### Menu terminal
Tape un numéro de 1 à 12 pour lancer un scénario, `memory` pour tester la mémoire conversationnelle, ou `quit` pour quitter.

### Démonstration mémoire (C2)
L'agent enchaîne 3 questions liées sur Sophie Bernard et se souvient du contexte à chaque étape.

### API REST
```bash
curl -X POST http://localhost:8000/api/agent/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Quelles sont les infos du client Marie Dupont ?"}'
```

La documentation interactive de l'API est disponible sur : http://localhost:8000/docs

## Structure du projet

```
tp_projet/
├── agent.py              # Configuration de l'agent LangChain
├── main.py               # Menu interactif
├── app.py                # Interface Streamlit
├── api.py                # API REST FastAPI
├── docker-compose.yml    # Configuration PostgreSQL
├── requirements.txt      # Dépendances Python
├── .env                  # Variables d'environnement
└── tools/
    ├── database.py       # Connexion PostgreSQL + recherche clients/produits
    ├── finance.py        # Cours boursiers yfinance + portefeuille
    ├── calculs.py        # TVA, intérêts, marge, mensualité
    ├── api_publique.py   # Conversion de devises (API Frankfurter)
    ├── texte.py          # Résumé, mots-clés, formatage rapport
    ├── recommandation.py # Recommandations produits
    └── portefeuille.py   # Calcul valeur portefeuille boursier
```
