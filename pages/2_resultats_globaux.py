from utils.utils import authenticate,plot_heatmap_ecarts_genre,load_data,plot_scores_by_gender, plot_scores_by_level_and_gender,compute_composite_scores,plot_combined_relation,plot_score_distributions_subplots, COLOR_PALETTE, plot_correlation_heatmap
import streamlit as st
import json

nom = authenticate()

# ✅ Affichage unique du message de bienvenue
if st.session_state.get("show_welcome", False):
    st.success(f"Bienvenue {nom} 👋")
    st.info("👉 Pense à ouvrir le menu latéral à gauche pour explorer les pages de l'application.")
    st.session_state["show_welcome"] = False  # Ne plus l'afficher ensuite


df=load_data("data/df_processed.csv")
df_scores=load_data("data/df_scores.csv")


with open("utils/scores_axes.json", "r", encoding="utf-8") as f:
    score_axes = json.load(f)


# Tabs
tab1, tab2, tab3 = st.tabs([
    "**QUESTIONS FERMÉES**",
    "**SCORES COMPOSITES**",
    "**CORRÉLATIONS**"
])

# Onglet 1 — Questions fermées (écarts par genre et par niveau)
with tab1:

    st.subheader("Résultats des questions fermées")

    st.markdown("Pour chaque question fermée, quatre niveaux de réponses ont été proposés aux élèves: « Pas du tout d’accord », « Plutôt pas d’accord », « Plutôt d’accord » et « Tout à fait d’accord ». Ces réponses ont été codées de 0 à 3 qui permettent de calculer un score moyen par question. Un score élevé indique une perception positive, tandis qu’un score faible indique une perception négative.")

    with st.expander("Liste des questions fermées"):
            st.markdown("""
            | Code | Question                                                                                   |
            |------|--------------------------------------------------------------------------------------------|
            | Q3   | Comment te sens-tu globalement dans ton établissement ?                                   |
            | Q4   | As-tu confiance dans les décisions prises par les adultes ?                               |
            | Q6   | Te sens-tu en sécurité dans l’établissement ?                                              |
            | Q7   | As-tu déjà participé à des projets ou activités dans l’établissement ?                    |
            | Q9   | Peux-tu t’exprimer librement dans l’établissement ?                                       |
            | Q10  | Te sens-tu écouté(e) et soutenu(e) ?                                                       |
            | Q12  | As-tu envie de venir chaque jour à l’établissement ?                                      |
            | Q13  | Comment qualifierais-tu la relation entre ta famille et l’établissement ?                 |
            """)

    # Initialisation de la valeur par défaut
    if "vue_scores" not in st.session_state:
        st.session_state.vue_scores = "vue globale par genre"

    # Sélecteur de vue avec st.pills
    vue = st.pills(
        label="",
        options=["vue globale par genre", "vue croisée par niveau et genre"],
        key="vue_scores")

    # Affichage conditionnel
    with st.container(border=True):
        if vue == "vue globale par genre":
            plot_scores_by_gender(df)
        else:
            plot_scores_by_level_and_gender(df)



    # 🧠 Lecture automatique des extrêmes
    score_columns = [
        "sentiment_global", "confiance_adultes", "sentiment_securite",
        "participation_projets", "liberte_expression", "ecoute_et_soutien",
        "envie_venir", "relation_famille_etab"
    ]

    labels = {
        "sentiment_global": "Q3 – Sentiment global",
        "confiance_adultes": "Q4 – Confiance envers les adultes",
        "sentiment_securite": "Q6 – Sentiment de sécurité",
        "participation_projets": "Q7 – Participation aux projets",
        "liberte_expression": "Q9 – Liberté d'expression",
        "ecoute_et_soutien": "Q10 – Écoute et soutien",
        "envie_venir": "Q12 – Envie de venir à l’établissement",
        "relation_famille_etab": "Q13 – Relation famille-établissement"
    }

    moyennes = df[score_columns].mean().sort_values()
    plus_bas = labels[moyennes.idxmin()]
    plus_haut = labels[moyennes.idxmax()]
    ecart = round(moyennes.max() - moyennes.min(), 2)


    st.info(f""" **À retenir** :
    - 📉 Score moyen le plus faible : **{plus_bas}**
    - 📈 Score moyen le plus élevé : **{plus_haut}**

    """,icon="ℹ️")



    st.divider()

    st.subheader("Écarts moyens par genre et par niveau")

    st.markdown("""
    Dans ce diagramme, chaque case indique l’**écart moyen Fille – Garçon** pour une question et un niveau :
    - Un **écart positif** signifie que les filles ont un **score moyen plus élevé** que les garçons.
    - Un **écart négatif** indique que les garçons ont un **score plus élevé** que les filles.
    """)

    with st.container(border=True):
        plot_heatmap_ecarts_genre(df)

    st.info("""**À retenir :**

- Les plus forts écarts en faveur des filles apparaissent en **4e** sur :
  - la participation aux projets (**+0.75**),
  - la confiance dans les décisions des adultes** (**+0.38**),
  - l’écoute et le soutien** (**+0.31**).

- En **5e**, les filles déclarent aussi des scores sensiblement plus élevés sur tous les axes (écarts de **+0.19 à +0.32**).

- En revanche, les écarts sont faibles voire inversés en 3e, où les garçons et les filles répondent de manière plus homogène (valeurs proches de 0, parfois négatives).

- Globalement, les **4e filles** ressortent comme le groupe le plus positivement engagé, notamment dans la dynamique participative.

""", icon="ℹ️")

# Onglet 2 — Scores composites par axe
with tab2:
    st.subheader("Scroring par axe thématique")

    st.markdown("""
                Pour faciliter la lecture des résultats, certaines questions fermées ont été regroupées en **axes thématiques**.
                Chaque axe correspond à une **moyenne de plusieurs questions** portant sur une même dimension du climat scolaire.
                Voici les 4 axes utilisés :
        - **Bien-être** → sentiment global, sécurité, envie de venir
        - **Confiance** → décisions des adultes, relation famille-établissement
        - **Expression / écoute** → liberté d'expression, écoute et soutien
        - **Engagement** → participation aux projets ou activités
                """)




    with open("utils/scores_axes.json", "r", encoding="utf-8") as f:
        score_axes = json.load(f)


    df_composite = compute_composite_scores(df, score_axes, context_cols=["genre"])

    with st.container(border=True):
        plot_score_distributions_subplots(
            df_composite,
            list(score_axes.keys()),
            rows=2,
            cols=2,
            palette=COLOR_PALETTE
        )



    def summarize_extremes(df, composite_columns, labels, top_n=3):
        lignes = []

        resultats = []
        for axe in composite_columns:
            for (niveau, genre), group in df.groupby(["niveau", "genre"]):
                if group[axe].notna().sum() == 0:
                    continue
                moyenne = group[axe].mean()
                resultats.append({
                    "score": axe,
                    "niveau": niveau,
                    "genre": genre,
                    "moyenne": moyenne
                })

        # Tri par moyenne
        sorted_results = sorted(resultats, key=lambda x: x["moyenne"])
        plus_faibles = sorted_results[:top_n]
        plus_forts = sorted_results[-top_n:][::-1]  # ordre décroissant

        lignes.append("**📉 Les 3 scores moyens les plus faibles sont :**")
        for r in plus_faibles:
            lignes.append(f"- {labels[r['score']]} en {r['niveau']} pour les {r['genre'].lower()}s : {r['moyenne']:.2f}/5")

        lignes.append("\n**📈 Les 3 scores moyens les plus élevés sont :**")
        for r in plus_forts:
            lignes.append(f"- {labels[r['score']]} en {r['niveau']} pour les {r['genre'].lower()}s : {r['moyenne']:.2f}/5")

        st.info("**À retenir :**\n\n" + "\n".join(lignes), icon="ℹ️")

    score_composite_cols = ["bien_etre", "climat_de_confiance", "expression_et_ecoute", "engagement"]
    labels = {
        "bien_etre": "Bien-être",
        "climat_de_confiance": "Confiance",
        "expression_et_ecoute": "Expression / écoute",
        "engagement": "Engagement"
    }

    summarize_extremes(df_scores, score_composite_cols, labels)








# Onglet 3 — Corrélations entre axes
with tab3:
    # 👉 Recalcul des scores composites (une seule fois)
    score_mapping = {
        "Bien-être": ["sentiment_global", "sentiment_securite", "envie_venir"],
        "Confiance": ["confiance_adultes", "relation_famille_etab"],
        "Expression / écoute": ["liberte_expression", "ecoute_et_soutien"],
        "Engagement": ["participation_projets"]
    }
    df_composite = compute_composite_scores(df, score_mapping, context_cols=[])

    # 🔢 Heatmap de corrélation
    st.markdown("### Matrice de corrélation")
    st.markdown("""
Ce tableau croisé indique le **degré de corrélation linéaire** entre chaque paire d’axes thématiques :

- **+1** : forte corrélation positive (les scores évoluent ensemble)
- **−1** : forte corrélation négative (les scores évoluent en sens inverse)
- **0** : absence de lien linéaire

> Ce graphique permet de repérer rapidement les **liens forts ou faibles entre les grandes dimensions du climat scolaire**.
    """)


    score_cols = list(score_mapping.keys())
    with st.container(border=True):
        plot_correlation_heatmap(df_composite, score_cols)


    st.info("""**À retenir** :

- Corrélation forte entre **Bien-être** et **Confiance** (**0.60**) : les élèves qui se sentent bien dans l’établissement ont aussi tendance à faire confiance aux adultes.
- Corrélation modérée entre **Bien-être** et **Expression / écoute** (**0.53**), et entre **Confiance** et **Expression / écoute** (**0.53**) : le sentiment d’écoute favorise le bien-être et la confiance.
- 🚫 Faibles corrélations de l’**Engagement** avec les autres axes (**≤ 0.10**) : ce score semble capter une dimension à part, moins liée au climat relationnel.

""", icon="ℹ️")


    st.markdown("---")


    # 🔁 Nuage de points entre deux axes
    st.markdown("### Corrélation entre deux axes choisis")
    st.markdown("""
Ces graphiques permetent d’explorer la **distribution croisée des scores** entre deux dimensions du climat scolaire.

- La **boîte à moustaches** à gauche indique comment les scores du second axe varient selon le niveau atteint sur le premier axe.
- La **heatmap** à droite montre combien d’élèves partagent une même combinaison de scores sur ces deux axes.

    """)

    col1, col2 = st.columns(2)
    x_axis = col1.selectbox("Axe horizontal (X)", score_cols, index=0)
    y_axis = col2.selectbox("Axe vertical (Y)", score_cols, index=1)

    if x_axis == y_axis:
        st.warning("📌 Choisissez deux axes différents pour afficher une corrélation.")
    else:
        plot_combined_relation(df_composite, x_axis, y_axis)
