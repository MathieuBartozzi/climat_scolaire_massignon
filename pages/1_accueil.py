import streamlit as st
import pandas as pd
from utils.utils import load_data,authenticate
import ast
import plotly.express as px


nom = authenticate()

# Titre principal
st.title("Climat scolaire – Portail d’analyse")

# Sous-titre
st.markdown("Bienvenue dans votre espace d’exploration des données issues du questionnaire Climat scolaire.")

# Encadré de contexte
st.info(
    "Ce portail a pour objectif de **faciliter la lecture et l’analyse** des réponses recueillies auprès des élèves. "
    "Il vous permet d’identifier les points d’appui et les axes d’amélioration pour renforcer le bien-être et le climat dans votre établissement."
)


# Chargement des données avec mise en cache
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

file_path = "data/df_processed.csv"
df = load_data(file_path)

colonnes_ouvertes = [
    "confiance_dialogue_extrait",
    "projets_participes",
    "lieux_expression_libre",
    "moments_agreables",
    "moments_desagreables",
    "lieux_agreables",
    "lieux_desagreables",
    "changements_souhaites"
]


nb_total = len(df)

# Appliquer la conversion string → liste python
for col in colonnes_ouvertes:
    df[col] = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

# Vérifie si au moins une des listes est non vide pour chaque élève
nb_avec_au_moins_une_reponse_ouverte = (
    df[colonnes_ouvertes]
    .applymap(lambda x: isinstance(x, list) and len(x) > 0)
    .any(axis=1)
    .sum()
)

pourcentage_ouvertes = round(100 * nb_avec_au_moins_une_reponse_ouverte / nb_total, 1)



# Onglets principaux
tabs = st.tabs(["**BILAN DES RÉPONSES**", "**MÉTHODOLOGIE**", "**À PROPOS**"])

# Onglet 1 — Bilan des réponses
with tabs[0]:
    # st.subheader("📈 Bilan des réponses")
    st.markdown(f"""
    - **Nombre total de répondants** : {len(df)} élèves
    - **Taux de réponses aux questions ouvertes** : {pourcentage_ouvertes}% (ces questions étaient facultatives)
    - **Croisement des répondants par genre et niveau** :
    """)

    # Création d'un tableau croisé genre × niveau
    cross_tab = df.groupby(['niveau', 'genre']).size().reset_index(name='effectif')

    # Regroupement des effectifs par niveau et genre
    cross_tab = df.groupby(['niveau', 'genre']).size().reset_index(name='effectif')

    # Création du graphique
    fig = px.bar(
        cross_tab,
        x="niveau",
        y="effectif",
        color="genre",
        barmode="group",
        labels={
            "niveau": "Niveau",
            "effectif": "Nombre d'élèves",
            "genre": "Genre"
        },
        color_discrete_sequence=px.colors.qualitative.Set2,
        height=400
    )

    # Affichage dans Streamlit
    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True)



# Onglet 2 — Méthodologie
with tabs[1]:
    # st.subheader("Méthodologie d’analyse")

    st.markdown("#### Un questionnaire structuré")
    st.markdown("""
    Les élèves ont répondu à un questionnaire structuré en deux volets :

    - **Des questions fermées** (à choix multiples ou échelles de satisfaction) portant sur le bien-être, la sécurité, l’écoute, l’engagement, etc.
    - **Des questions ouvertes**, où ils pouvaient s’exprimer librement sur leurs ressentis, leurs souhaits, ou des moments vécus.

    Ces deux types de réponses ont été analysés avec une méthodologie adaptée à leur nature.
    """)
    st.divider()
    st.markdown("#### L’analyse des questions fermées")

    st.markdown("""
    Les réponses fermées ont été converties en **scores numériques** permettant de calculer des moyennes sur différents thèmes.

    Nous avons ensuite :
    - Comparé les réponses **entre filles et garçons**, ou **entre niveaux scolaires** (6e, 5e, 4e, 3e)
    - Repéré les **écarts significatifs** (par exemple, des ressentis très différents selon le genre)
    - Visualisé ces résultats à l’aide de **graphismes clairs** (barres, cartes colorées)

    Ces analyses permettent de **repérer des tendances collectives** et des signaux faibles, utiles pour le pilotage pédagogique.
    """)
    st.divider()
    st.markdown("#### Une lecture fine grâce aux “profils d’élèves”")

    st.markdown("""
    Chaque élève a été associé à un **profil** en fonction de ses réponses globales.
    Cette classification automatique regroupe les élèves selon leurs ressentis et comportements dominants.
    Ces profils aident à **sortir d’une lecture purement statistique** pour penser en termes de besoins pédagogiques différenciés.
    """)

    st.divider()
    st.markdown("#### Une IA pour comprendre les réponses ouvertes")

    st.markdown("""
    Les réponses ouvertes srévèlent ce que les élèves vivent **avec leurs mots**.

    Pour les analyser sans les réduire :
    - Puis nous avons utilisé **GPT-4o**, une intelligence artificielle avancée, pour **extraire les mots-clés ou thèmes les plus représentatifs**.
    - Nous avons conduit un travail sur la fréquence des termes similaires (ex. “récré”, “pause”, “cour”)
    """)

    st.success("Cette méthodologie a été pensée pour être rigoureuse, lisible, et surtout utile aux équipes éducatives.")



# Onglet 3 — À propos
with tabs[2]:
    # st.subheader("💡 À propos de cette démarche")

    st.markdown("""
    Ce portail a été conçu pour aider les établissements à mieux comprendre le vécu des élèves à partir des réponses qu’ils ont données dans un questionnaire sur le climat scolaire.

    L’objectif est simple : **mettre les données au service de l’écoute et de l’action éducative**.

    ---

    #### Une approche pédagogique et éthique

    - Aucune donnée nominative n’est utilisée.
    - L’analyse est collective et respecte la confidentialité.
    - Les réponses ouvertes sont traitées automatiquement par une intelligence artificielle (GPT-4o) pour faire émerger les mots les plus représentatifs, sans interprétation individuelle.

    ---

    #### Un outil libre et réutilisable

    Ce projet s’appuie sur :
    - Des outils open source (Python, Pandas, Streamlit)
    - Un traitement local des données
    - Une logique adaptable à d’autres établissements ou contextes

    ---

    #### 👤 Contact

    Pour toute question, amélioration ou collaboration pédagogique, vous pouvez contacter :

    **mathieu.bartozzi@mlfmonde.org**
    """)
