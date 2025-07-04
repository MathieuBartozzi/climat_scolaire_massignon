
import streamlit as st
from utils.utils import authenticate

# 🌐 Configuration générale
st.set_page_config(page_icon=":material/dashboard:",layout="wide")
st.logo("logo.png", size="large")

# Authentification de l'utilisateur
nom = authenticate()

# ✅ Affichage unique du message de bienvenue
if st.session_state.get("show_welcome", False):
    st.success(f"Bienvenue {nom} 👋")
    st.info("👉 Pense à ouvrir le menu latéral à gauche pour explorer les pages de l'application.")
    st.session_state["show_welcome"] = False  # Ne plus l'afficher ensuite




# 📁 Définir les pages comme objets
accueil = st.Page("pages/1_accueil.py", title="Accueil", icon=":material/home:")
dashboard = st.Page("pages/2_resultats_globaux.py", title="Résultats globaux", icon=":material/analytics:")
ecarts = st.Page("pages/3_profils.py", title="Profils", icon=":material/group:")
ouvertes = st.Page("pages/4_ouvertes.py", title="Réponses ouvertes", icon=":material/comment:")
conclusion = st.Page("pages/5_conclusions.py", title="Conclusion", icon=":material/insights:")


# 📊 Créer la navigation avec les pages
pg = st.navigation(
        {
            "Présentation": [accueil],
            "Navigation": [dashboard, ecarts, ouvertes,conclusion]
        },
        expanded=True
    )

pg.run()
