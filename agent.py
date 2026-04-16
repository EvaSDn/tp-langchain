from langchain_classic.tools import Tool
from langchain_tavily import TavilySearch
from langchain_experimental.tools import PythonREPLTool
from tools.database import rechercher_client,rechercher_produit
from tools.finance import obtenir_cours_action, obtenir_cours_crypto
from tools.calculs import calculer_tva,calculer_interets_composes,calculer_marge,calculer_mensualite_pret
from tools.api_publique import convertir_devise
from tools.texte import resumer_texte, formater_rapport, extraire_mots_cles
from tools.recommandation import recommander_produits
from tools.portefeuille import calculer_portefeuille
from langchain_core.tools import StructuredTool
from langchain_classic.agents import create_openai_tools_agent
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from dotenv import load_dotenv

load_dotenv()
tavily_search = TavilySearch(
    max_results=3,
    description=(
        'Recherche des informations sur le web en temps réel. '
        'Utilise cet outil pour : actualités financières, informations sur une entreprise, '
        'résultats trimestriels, événements récents. '
        'Entrée : une question ou des mots-clés en langage naturel.'
    )
)

python_repl = PythonREPLTool()
python_repl.description = (
    'Exécute du code Python pour des calculs complexes ou traitements '
    'de données non couverts par les autres outils. '
    'Entrée : code Python valide sous forme de chaîne.'
)
tools = [
    # ── Outil 1 : Base de données ─────────────────────────────────────
    StructuredTool.from_function(
        name='rechercher_client',
        func=rechercher_client,
        description='Recherche un client par nom ou ID (ex: C001). Retourne solde, type de compte, historique achats.'
    ),
    StructuredTool.from_function(
        name='rechercher_produit',
        func=rechercher_produit,
        description='Recherche un produit par nom ou ID. Retourne prix HT, TVA, prix TTC, stock.'
    ),
    # ── Outil 2 : Données financières ─────────────────────────────────
    StructuredTool.from_function(
        name='cours_action',
        func=obtenir_cours_action,
        description='Cours boursier d\'une action. '
                     'Entrée : symbole majuscule ex AAPL, MSFT, TSLA, LVMH, AIR.'
    ),
    StructuredTool.from_function(
        name='cours_crypto',
        func=obtenir_cours_crypto,
        description='Cours d\'une crypto. Entrée : symbole ex BTC, ETH, SOL, BNB, DOGE.'
    ),
    # ── Outil 3 : Calculs financiers ──────────────────────────────────
    StructuredTool.from_function(
        name='calculer_tva',
        func=calculer_tva,
        description='Calcule TVA et prix TTC. Entrée : prix_ht,taux ex 100,20.'
    ),
    StructuredTool.from_function(
        name='calculer_interets',
        func=calculer_interets_composes,
        description='Intérêts composés. Entrée : capital,taux_annuel,années ex 10000,5,3.'
    ),
    StructuredTool.from_function(
        name='calculer_marge',
        func=calculer_marge,
        description='Marge commerciale. Entrée : prix_vente,cout_achat ex 150,80.'
    ),
    StructuredTool.from_function(
        name='calculer_mensualite',
        func=calculer_mensualite_pret,
        description='Mensualité prêt. Entrée : capital,taux_annuel,mois ex 200000,3.5,240.'
    ),
    # ── Outil 4 : API publique ────────────────────────────────────────
    StructuredTool.from_function(
        name='convertir_devise',
        func=convertir_devise,
        description='Conversion de devises en temps réel (API Frankfurter). Entrée : montant,DEV_SOURCE,DEV_CIBLE ex 100,USD,EUR.'
    ),
    # ── Outil 5 : Transformation de texte ────────────────────────────
    StructuredTool.from_function(
        name='resumer_texte',
        func=resumer_texte,
        description='Résume un texte et donne des statistiques. Entrée : texte complet.'
    ),
    StructuredTool.from_function(
        name='formater_rapport',
        func=formater_rapport,
        description='Formate en rapport. Entrée : Cle1:Val1|Cle2:Val2.'
    ),
    StructuredTool.from_function(
        name='extraire_mots_cles',
        func=extraire_mots_cles,
        description='Extrait les mots-clés d\'un texte. Entrée : texte complet.'
    ),
    # ── Outil 6 : Recommandation ────────────────────────────────────
    StructuredTool.from_function(
        name='recommander_produits',
        func=recommander_produits,
        description='Recommandations produits. Entrée : budget,categorie,type_compte ex 300,Informatique,Premium. Catégories : Informatique, Mobilier, Audio, Toutes. Types : Standard, Premium, VIP.'
    ),
    # ── Outil 7 : Recherche web ─────────────────────────────────────
    tavily_search,
    # ── Outil B1 : Portefeuille boursier ─────────────────────────────
    StructuredTool.from_function(
        name='calculer_portefeuille',
        func=calculer_portefeuille,
        description='Calcule la valeur totale d\'un portefeuille d\'actions en temps réel. Entrée : SYMBOLE:QUANTITE séparés par | ex: AAPL:10|MSFT:5|TSLA:3'
    ),
    # ── Outil B2 : Python REPL ────────────────────────────────────────
    python_repl,
]

from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain_classic import hub
import os
 
def creer_agent():
    """Crée et retourne un agent LangChain configuré avec mémoire."""

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un assistant financier intelligent. Utilise les outils disponibles pour répondre aux questions."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )

    return agent_executor

def interroger_agent(agent, question: str):
    """Envoie une question à l'agent et affiche la réponse finale."""
    print(f"\n{'='*60}")
    print(f"Question : {question}")
    print('='*60)
    result = agent.invoke({"input": question})
    print(f"\nRéponse finale : {result['output']}")
    return result