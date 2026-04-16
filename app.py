import streamlit as st
from dotenv import load_dotenv
from agent import creer_agent

load_dotenv()

st.title("Mon agent IA")

with st.sidebar:
    st.header("Outils disponibles")
    st.markdown("""
    - **rechercher_client** — Infos client
    - **rechercher_produit** — Infos produit
    - **cours_action** — Cours boursier
    - **cours_crypto** — Cours crypto
    - **calculer_portefeuille** — Valeur portefeuille
    - **calculer_tva** — TVA et prix TTC
    - **calculer_interets** — Intérêts composés
    - **calculer_marge** — Marge commerciale
    - **calculer_mensualite** — Mensualité prêt
    - **convertir_devise** — Conversion devises
    - **resumer_texte** — Résumé de texte
    - **formater_rapport** — Formatage rapport
    - **extraire_mots_cles** — Mots-clés
    - **recommander_produits** — Recommandations
    - **tavily_search** — Recherche web
    - **python_repl** — Exécution Python
    """)
    if st.button("Réinitialiser la conversation"):
        st.session_state.historique = []
        st.rerun()

# Initialisation de l'agent et de l'historique
if "agent" not in st.session_state:
    st.session_state.agent = creer_agent()

if "historique" not in st.session_state:
    st.session_state.historique = []

# Affichage de l'historique
for echange in st.session_state.historique:
    with st.chat_message("user"):
        st.write(echange["question"])
    with st.chat_message("assistant"):
        st.write(echange["reponse"])

question = st.chat_input("Posez votre question...")

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Réflexion en cours..."):
            result = st.session_state.agent.invoke({"input": question})
            reponse = result["output"]
        st.write(reponse)

    st.session_state.historique.append({
        "question": question,
        "reponse": reponse
    })