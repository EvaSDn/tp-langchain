import os
from dotenv import load_dotenv
from agent import creer_agent, interroger_agent

load_dotenv()

SCENARIOS = {
    "1": (
        "Scénario 1 – Consultation base de données",
        "Quelles sont les informations du client Marie Dupont ? "
        "Quel est son solde et son type de compte ?"
    ),
    "2": (
        "Scénario 2 – Données financières",
        "Donne-moi le cours actuel d'Apple (AAPL) et du Bitcoin (BTC). "
        "Lequel a la plus forte variation aujourd'hui ?"
    ),
    "3": (
        "Scénario 3 – Calculs financiers multiples",
        "Je veux acheter un ordinateur portable (P001). "
        "Quel est son prix TTC avec la TVA à 20% ? "
        "Et quelle serait ma marge si je le revendais 1200€ ?"
    ),
    "4": (
        "Scénario 4 – Conversion de devises (API)",
        "Combien vaut 500 euros en dollars américains et en livres sterling ? "
        "Donne-moi les deux conversions."
    ),
    "5": (
        "Scénario 5 – Calcul de prêt + intérêts",
        "Je souhaite emprunter 150 000€ sur 20 ans à un taux de 4% par an. "
        "Quelle serait ma mensualité et combien paierais-je d'intérêts au total ? "
        "Si je place 20 000€ à 3% pendant 5 ans, quel capital j'obtiendrai-je ?"
    ),
    "6": (
        "Scénario 6 – Recommandation personnalisée",
        "Je suis un client Premium avec un budget de 400€. "
        "Je cherche du matériel informatique. "
        "Quels produits me recommanderais-tu ?"
    ),
    "7": (
        "Scénario 7 – Analyse de texte complète",
        "Résume ce texte : 'LangChain est un framework pour construire des "
        "applications intelligentes basées sur des modèles de langage.' "
        "Extrait ensuite les mots-clés et formate un rapport avec "
        "les champs Sujet:LangChain|Type:Résumé|Auteur:Agent."
    ),
    "8": (
        "Scénario 8 – Analyse financière complète (multi-outils)",
        "Analyse financière : "
        "1) Cours de Microsoft (MSFT) et d'Ethereum (ETH). "
        "2) Convertis 1000 USD en EUR. "
        "3) Si j'investis 5000€ à 7% pendant 10 ans, quel capital ?"
    ),
    "9": (
    "Scénario 9 – Portefeuille boursier",
    "Calcule mon portefeuille : AAPL:10|MSFT:5|TSLA:3"
),
"10": (
    "Scénario 10 – Recherche web Tavily",
    "Quelles sont les actualités d'Apple aujourd'hui ?"
),
"11": (
    "Scénario 11 – Portefeuille boursier",
    "Calcule mon portefeuille : AAPL:10|MSFT:5|TSLA:3"
),
"12": (
    "Scénario 12 – PythonREPL",
    "Trie ce portefeuille par valeur décroissante et donne les statistiques : AAPL:10|MSFT:5|TSLA:3|GOOGL:2"
),
}


def afficher_menu():
    print("\n" + "="*60)
    print("        AGENT LANGCHAIN — MENU DES SCÉNARIOS")
    print("="*60)
    for num, (titre, _) in SCENARIOS.items():
        print(f"  {num}. {titre}")
    print("  memoire - Mémoire conversationnelle")
    print("  quit — Quitter")
    print("="*60)


if __name__ == "__main__":
    print("Initialisation de l'agent...")
    agent = creer_agent()
    print("Agent prêt.")

    while True:
        afficher_menu()
        choix = input("\nVotre choix : ").strip().lower()

        if choix in ("quit", "exit", "q"):
            print("\nAu revoir !")
            break
        elif choix in SCENARIOS:
            titre, question = SCENARIOS[choix]
            print(f"\n>>> {titre}")
            interroger_agent(agent, question)
        elif choix == "memoire":
            print("\n>>> Démonstration mémoire conversationnelle")
            agent_memoire = creer_agent()
            questions = [
                "Donne-moi les infos du client Sophie Bernard",
                "Quel produit lui recommandes-tu ?",
                "Calcule le prix TTC et dis-moi si elle peut se le permettre"
            ]
            for q in questions:
                print(f"\n{'='*60}")
                print(f"Question : {q}")
                print('='*60)
                result = agent_memoire.invoke({"input": q})
                print(f"\nRéponse : {result['output']}")
        else:
            print(f"\n  Choix invalide '{choix}'. Entrez un numéro entre 1 et 12, ou 'quit'.")
