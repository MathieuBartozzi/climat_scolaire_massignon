import streamlit as st
import pandas as pd
from utils.utils import (
    authenticate,
    load_data,
    harmoniser_colonnes_ouvertes,
    compter_mots_uniques_par_colonnes,
    plot_question_ouverte_barplot
)

nom = authenticate()

# ✅ Affichage unique du message de bienvenue
if st.session_state.get("show_welcome", False):
    st.success(f"Bienvenue {nom} 👋")
    st.session_state["show_welcome"] = False  # Ne plus l'afficher ensuite

# ----------------------
# Paramètres de la page
# ----------------------
st.title("Analyse des réponses aux questions ouvertes")

# Colonnes ciblées
colonnes_ouvertes = [
    "confiance_dialogue_extrait",
    "lieux_expression_libre",
    "moments_agreables",
    "moments_desagreables",
    "lieux_agreables",
    "lieux_desagreables",
    "changements_souhaites"
]

# Titre lisibles
question_titles = {
    "confiance_dialogue_extrait": "Situations dans lesquelles les élèves se sentent écoutés ou en confiance",
    "lieux_expression_libre": "Lieux où les élèves peuvent s’exprimer librement",
    "moments_agreables": "Moments les plus agréables vécus au sein de l’établissement",
    "moments_desagreables": "Moments les plus désagréables vécus au sein de l’établissement",
    "lieux_agreables": "Lieux perçus comme agréables dans l’établissement",
    "lieux_desagreables": "Lieux perçus comme désagréables dans l’établissement",
    "changements_souhaites": "Changements souhaités dans l’établissement"
}

# --------------------------
# Chargement et préparation
# --------------------------
df = load_data("data/df_full.csv")

# Dictionnaire de regroupement harmonisé
regroupements = {
    "non": "aucun",
    "récré": "récréation",
    "récréations": "récréation",
    "pause méridienne": "pause",
    "pauses": "pause",
    "plateau": "terrain",
    "MASSMUN": "MUN",
    "OSUIMUN": "MUN",
    "THIMUN": "MUN",
    "FERMUN": "MUN",
    "cours": "en cours",
    "cour": "la cour",
    "récréation": "la cour",
    "salle": "salle de classe",
    "classe": "salle de classe",
    "classes": "salle de classe",
    "salles": "salle de classe",
    "évaluations": "évaluation"
}

df = harmoniser_colonnes_ouvertes(df, colonnes_ouvertes, regroupements)
frequences_par_question = compter_mots_uniques_par_colonnes(df, colonnes_ouvertes)


# --------------------------
# Interface : Selectbox
# --------------------------
selected_colonne = st.selectbox(
    "Choisis une question à explorer",
    options=colonnes_ouvertes,
    format_func=lambda x: question_titles.get(x, x)
)

# Affichage du barplot
fig = plot_question_ouverte_barplot(selected_colonne, frequences_par_question, min_freq=15, question_titles=question_titles)

with st.container(border=True):
    st.plotly_chart(fig, use_container_width=True)
