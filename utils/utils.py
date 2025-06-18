import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from itertools import combinations
import json



@st.cache_data
def load_data(path):
    return pd.read_csv(path)

# ──────────────────────────────────────────────────────────────
# 🧮 CALCUL DES SCORES COMPOSITES
# ──────────────────────────────────────────────────────────────


def compute_composite_scores(df, scores_mapping, scale=5, max_score=3, context_cols=["genre", "niveau"]):
    df_copy = df.copy()

    if "projets_participes" in df_copy.columns:
        df_copy["_n_projets_participes"] = df_copy["projets_participes"].apply(
            lambda x: len(eval(x)) if isinstance(x, str) and x.startswith("[") else 0
        )
        max_count = df_copy["_n_projets_participes"].max() or 1
        df_copy["_score_nb_projets"] = df_copy["_n_projets_participes"].apply(
            lambda x: (x / max_count) * max_score if x > 0 else 0
        )

    for axis, cols in scores_mapping.items():
        cols_to_use = cols.copy()
        if axis.lower() == "engagement" and "_score_nb_projets" in df_copy.columns:
            cols_to_use.append("_score_nb_projets")
        available_cols = [col for col in cols_to_use if col in df_copy.columns]
        df_copy[axis] = df_copy[available_cols].mean(axis=1) * scale / max_score if available_cols else None

    final_cols = [col for col in context_cols if col in df_copy.columns] + list(scores_mapping.keys())
    return df_copy[final_cols].copy()


# ──────────────────────────────────────────────────────────────
# 🎨 PARAMÈTRES VISUELS
# ──────────────────────────────────────────────────────────────

COLOR_PALETTE = px.colors.qualitative.Set2


# ──────────────────────────────────────────────────────────────
# 📊 VISUALISATIONS STREAMLIT-COMPATIBLES
# ──────────────────────────────────────────────────────────────

def plot_score_distributions(df, score_columns):
    for score in score_columns:
        fig = px.histogram(
            df, x=score, nbins=6,
            title=f"Distribution du score : {score}",
            color="genre",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig)



from plotly.subplots import make_subplots
import plotly.graph_objects as go

def plot_score_distributions_subplots(df, score_columns, rows=2, cols=2, palette=None):
    """
    Affiche les distributions des scores composites par genre sous forme de grille (subplots),
    avec noms lisibles des axes thématiques.
    """


    # Dictionnaire des noms lisibles
    labels = {
        "bien_etre": "Bien-être",
        "climat_de_confiance": "Confiance",
        "expression_et_ecoute": "Expression / écoute",
        "engagement": "Engagement"
    }


    # Sous-titres formatés avec les noms lisibles
    subtitles = [labels.get(col, col) for col in score_columns]

    # Création de la grille
    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=subtitles
    )

    # Récupère les genres uniques
    genres = df["genre"].dropna().unique()


    # Génère un mapping couleur si palette fournie
    if palette and len(palette) >= len(genres):
        color_map = {genre: palette[i] for i, genre in enumerate(genres)}
    else:
        color_map = {genre: None for genre in genres}

    # Boucle sur les axes composites
    for i, score in enumerate(score_columns):
        row = i // cols + 1
        col = i % cols + 1

        for genre in genres:
            data = df[df["genre"] == genre][score]
            fig.add_trace(
                go.Histogram(
                    x=data,
                    name=genre,
                    nbinsx=6,
                    marker_color=color_map.get(genre, "#999999"),
                    showlegend=(i == 0)
                ),
                row=row,
                col=col
            )

    # Mise en forme finale
    fig.update_layout(
        height=500 if rows == 1 else 800,
        # title_text="Distributions des scores composites par axe (par genre)",
        bargap=0.1
    )

    st.plotly_chart(fig, use_container_width=True)




def plot_combined_relation(df, x_col, y_col):
    df_plot = df[[x_col, y_col]].dropna().copy()
    df_plot[f"{x_col}_round"] = df_plot[x_col].round(0)
    df_plot[f"{y_col}_round"] = df_plot[y_col].round(0)

    fig_box = px.box(
        df_plot,
        x=f"{x_col}_round",
        y=y_col,
        points="all",
        color_discrete_sequence=["steelblue"],
        labels={f"{x_col}_round": x_col.replace("_", " "), y_col: y_col.replace("_", " ")}
    )

    heatmap_data = pd.crosstab(df_plot[f"{y_col}_round"], df_plot[f"{x_col}_round"])
    heatmap_trace = go.Heatmap(
        z=heatmap_data.values[::-1],
        x=heatmap_data.columns,
        y=heatmap_data.index[::-1],
        text=heatmap_data.values[::-1],
        texttemplate="%{text}",
        colorscale="Blues",
        zmin=0,
        zmax=heatmap_data.values.max(),
        colorbar=dict(title="Nombre d'élèves"),
        hovertemplate=f"{x_col.replace('_', ' ')}: %{{x}}<br>{y_col.replace('_', ' ')}: %{{y}}<br>n: %{{z}}<extra></extra>"
    )

    fig = make_subplots(rows=1, cols=2, column_widths=[0.5, 0.5], horizontal_spacing=0.12)
    for trace in fig_box.data:
        fig.add_trace(trace, row=1, col=1)
    fig.add_trace(heatmap_trace, row=1, col=2)

    fig.update_layout(height=500, width=1000, showlegend=False)
    fig.update_xaxes(title_text=x_col.replace("_", " "), row=1, col=1)
    fig.update_yaxes(title_text=y_col.replace("_", " "), row=1, col=1)
    fig.update_xaxes(title_text=x_col.replace("_", " "), row=1, col=2)
    fig.update_yaxes(title_text=y_col.replace("_", " "), row=1, col=2)

    st.plotly_chart(fig)


def plot_all_score_combinations(df, score_cols):
    for x_col, y_col in combinations(score_cols, 2):
        plot_combined_relation(df, x_col, y_col)


def plot_scores_by_gender(df):
    score_columns = [
        "sentiment_global", "confiance_adultes", "sentiment_securite",
        "participation_projets", "liberte_expression", "ecoute_et_soutien",
        "envie_venir", "relation_famille_etab"
    ]
    mapping_q = {
        "sentiment_global": "Q3", "confiance_adultes": "Q4",
        "sentiment_securite": "Q6", "participation_projets": "Q7",
        "liberte_expression": "Q9", "ecoute_et_soutien": "Q10",
        "envie_venir": "Q12", "relation_famille_etab": "Q13"
    }
    question_labels = {
    "Q3": "Comment te sens-tu globalement dans ton établissement ?",
    "Q4": "As-tu confiance dans les décisions prises par les adultes ?",
    "Q6": "Te sens-tu en sécurité dans l’établissement ?",
    "Q7": "As-tu déjà participé à des projets ou activités dans l’établissement ?",
    "Q9": "Peux-tu t’exprimer librement dans l’établissement ?",
    "Q10": "Te sens-tu écouté(e) et soutenu(e) ?",
    "Q12": "As-tu envie de venir chaque jour à l’établissement ?",
    "Q13": "Comment qualifierais-tu la relation entre ta famille et l’établissement ?"
}
    ordre_questions = list(mapping_q.values())

    df_melted = df[["genre"] + score_columns].melt("genre", value_vars=score_columns, var_name="question", value_name="score")
    df_melted["question"] = df_melted["question"].map(mapping_q)
    df_grouped = df_melted.groupby(["question", "genre"], as_index=False)["score"].mean()
    df_grouped["question"] = pd.Categorical(df_grouped["question"], categories=ordre_questions, ordered=True)
    df_grouped["intitule"] = df_grouped["question"].map(question_labels)


    fig = px.bar(
        df_grouped, x="question", y="score", color="genre",
        barmode="group", category_orders={"question": ordre_questions},
        color_discrete_sequence=COLOR_PALETTE, height=600,
        # title="Scores moyens par question fermée selon le genre",
        hover_data=["intitule"]
    )
    fig.update_layout(xaxis_title=None, yaxis_title="Score moyen (0–3)", yaxis_range=[0, 3])
    st.plotly_chart(fig)


def plot_scores_by_level_and_gender(df):
    score_columns = [
        "sentiment_global", "confiance_adultes", "sentiment_securite",
        "participation_projets", "liberte_expression", "ecoute_et_soutien",
        "envie_venir", "relation_famille_etab"
    ]
    mapping_q = {
        "sentiment_global": "Q3", "confiance_adultes": "Q4",
        "sentiment_securite": "Q6", "participation_projets": "Q7",
        "liberte_expression": "Q9", "ecoute_et_soutien": "Q10",
        "envie_venir": "Q12", "relation_famille_etab": "Q13"
    }
    question_labels = {
    "Q3": "Comment te sens-tu globalement dans ton établissement ?",
    "Q4": "As-tu confiance dans les décisions prises par les adultes ?",
    "Q6": "Te sens-tu en sécurité dans l’établissement ?",
    "Q7": "As-tu déjà participé à des projets ou activités dans l’établissement ?",
    "Q9": "Peux-tu t’exprimer librement dans l’établissement ?",
    "Q10": "Te sens-tu écouté(e) et soutenu(e) ?",
    "Q12": "As-tu envie de venir chaque jour à l’établissement ?",
    "Q13": "Comment qualifierais-tu la relation entre ta famille et l’établissement ?"
}

    ordre_questions = list(mapping_q.values())

    df_melted = df[["niveau", "genre"] + score_columns].melt(["niveau", "genre"], value_vars=score_columns, var_name="question", value_name="score")
    df_melted["Question"] = df_melted["question"].map(mapping_q)

    df_grouped = df_melted.groupby(["Question", "niveau", "genre"], as_index=False)["score"].mean()
    df_grouped = df_grouped.rename(columns={"genre": "Genre", "niveau": "Niveau"})

    niveau_labels = {"6e": "niveau 6e", "5e": "niveau 5e", "4e": "niveau 4e", "3e": "niveau 3e"}
    ordre_niveaux = list(niveau_labels.values())
    df_grouped["Niveau_label"] = df_grouped["Niveau"].map(niveau_labels)
    df_grouped["Niveau_label"] = pd.Categorical(df_grouped["Niveau_label"], categories=ordre_niveaux, ordered=True)
    df_grouped["Question"] = pd.Categorical(df_grouped["Question"], categories=ordre_questions, ordered=True)
    df_grouped["intitule"] = df_grouped["Question"].map(question_labels)



    fig = px.bar(
        df_grouped, x="Question", y="score", color="Genre",
        barmode="group", facet_col="Niveau_label",
        category_orders={"Niveau_label": ordre_niveaux, "Question": ordre_questions},
        color_discrete_sequence=COLOR_PALETTE, height=600,
        # title="Scores moyens par question fermée par niveau et genre",
        hover_data=["intitule"]
    )
    fig.update_layout(xaxis_title=None, yaxis_title="Score moyen (0–3)", yaxis_range=[0, 3])
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.for_each_xaxis(lambda axis: axis.update(title=None))
    st.plotly_chart(fig)


def plot_heatmap_ecarts_genre(df):
    score_columns = [
        "sentiment_global", "confiance_adultes", "sentiment_securite",
        "participation_projets", "liberte_expression", "ecoute_et_soutien",
        "envie_venir", "relation_famille_etab"
    ]
    question_labels = {
        "sentiment_global": "Sentiment global dans l’établissement",
        "confiance_adultes": "Confiance dans les décisions des adultes",
        "sentiment_securite": "Sentiment de sécurité dans l’établissement",
        "participation_projets": "Participation aux projets",
        "liberte_expression": "Sentiment d'expression libre",
        "ecoute_et_soutien": "Sentiment d'etre écouté(e) et soutenu(e)",
        "envie_venir": "Envie de venir chaque jour",
        "relation_famille_etab": "Qualité de la relation famille / établissement ?"
    }
    df_melted = df[["niveau", "genre"] + score_columns].melt(["niveau", "genre"], value_vars=score_columns, var_name="question", value_name="score")
    df_melted["question_code"] = df_melted["question"].map(question_labels)
    df_grouped = df_melted.groupby(["niveau", "question_code", "genre"], as_index=False)["score"].mean()
    df_pivot = df_grouped.pivot_table(index=["niveau", "question_code"], columns="genre", values="score").reset_index()
    df_pivot["diff"] = df_pivot["Fille"] - df_pivot["Garçon"]
    heatmap_data = df_pivot.pivot(index="niveau", columns="question_code", values="diff")

    fig = px.imshow(
        heatmap_data, text_auto=True,
        color_continuous_scale="RdBu",
        color_continuous_midpoint=0,
        labels=dict(color="Écart Fille - Garçon"),
        aspect="auto",
        # title="Écarts Fille - Garçon par niveau et question"
    )
    fig.update_layout(xaxis_title="", yaxis_title="", height=500)
    st.plotly_chart(fig)


def plot_correlation_heatmap(df, score_cols):
    """
    Affiche une heatmap des corrélations (Pearson) entre les scores composites.
    """
    corr_matrix = df[score_cols].corr(method="pearson").round(2)

    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="RdBu",
        zmin=-1, zmax=1
        # title="📊 Corrélations entre les scores composites"
    )
    fig.update_layout(height=600, width=600)
    st.plotly_chart(fig, use_container_width=True)
# ──────────────────────────────────────────────────────────────
# 📚 TRAITEMENT DES QUESTIONS OUVERTES
# ──────────────────────────────────────────────────────────────

import ast
import pandas as pd
import plotly.express as px

# Harmonisation des réponses libres
def parse_et_harmoniser(val, regroupements):
    try:
        if isinstance(val, str) and val.startswith("["):
            val = ast.literal_eval(val)
        if not isinstance(val, list):
            return []
        return [regroupements.get(m.strip().lower(), m.strip().lower()) for m in val]
    except:
        return []

# Nettoyage des colonnes ouvertes
def harmoniser_colonnes_ouvertes(df, colonnes, regroupements):
    df_copy = df.copy()
    for col in colonnes:
        df_copy[col] = df_copy[col].apply(lambda x: parse_et_harmoniser(x, regroupements))
    return df_copy

# Comptage des fréquences pour chaque colonne
def compter_mots_uniques_par_colonnes(df, colonnes):
    stats = {}
    for col in colonnes:
        mots = df.explode(col)[col]
        mots = mots[mots.notna() & (mots != "")]
        compte = mots.value_counts().reset_index()
        compte.columns = ["mot", "frequence"]
        stats[col] = compte
    return stats

# Génération d'un barplot pour une colonne spécifique
def plot_question_ouverte_barplot(colonne, freq_dict, min_freq=5, question_titles=None, color_palette=None):
    df_freq = freq_dict.get(colonne)
    if df_freq is None or df_freq.empty:
        return None

    df_plot = df_freq[df_freq["frequence"] >= min_freq]
    if df_plot.empty:
        return None

    # title = question_titles.get(colonne, colonne.replace('_', ' ').capitalize())

    fig = px.bar(
        df_plot.sort_values("frequence", ascending=True),
        x="frequence", y="mot", orientation="h",
        # title=title,
        labels={"frequence": "Fréquence", "mot": ""},
        color="mot",
        color_discrete_sequence=color_palette if color_palette else px.colors.qualitative.Pastel
    )

    fig.update_layout(
        showlegend=False,
        yaxis=dict(categoryorder="total ascending"),
        height=400,
        margin=dict(l=100, r=40, t=60, b=40)
    )
    return fig


# ──────────────────────────────────────────────────────────────
# 📚 UTILISATION CLUSTERING
# ──────────────────────────────────────────────────────────────


#to keep
def plot_cluster_profile(df_scores, cluster_id):
    # Filtrage des données pour un cluster donné
    cluster_data = df_scores[df_scores["cluster_kmeans"] == cluster_id][[
        "climat_de_confiance", "bien_etre", "expression_et_ecoute", "engagement"
    ]]

    # Moyenne des scores pour le cluster
    cluster_mean = cluster_data.mean()

    # Labels lisibles
    question_labels = {
        "climat_de_confiance": "Climat de confiance",
        "bien_etre": "Bien-être",
        "expression_et_ecoute": "Expression / écoute",
        "engagement": "Engagement"
    }

    categories = [question_labels[col] for col in cluster_mean.index]
    values = cluster_mean.values.tolist()

    # Pour fermer le polygone, on répète le premier point
    categories += [categories[0]]
    values += [values[0]]

    # Création du radar chart
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=f"Profil {cluster_id + 1}",
        marker_color='cornflowerblue'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 4])
        ),
        showlegend=False,
        # title_text=f"Scores moyens",
        height=300,
        width=300,
        margin=dict(t=30)
    )

    return fig




#to keep
def plot_single_cluster_distribution(df_scores, cluster_id):
    # Filtrage du cluster
    df_c = df_scores[df_scores["cluster_kmeans"] == cluster_id]

    # Comptes genre et niveau
    genre_counts = df_c["genre"].value_counts().reindex(["Fille", "Garçon"]).fillna(0)
    niveau_counts = df_c["niveau"].value_counts().reindex(["6e", "5e", "4e", "3e"]).fillna(0)

    # Création d'une figure à deux sous-graphiques côte à côte
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "xy"}, {"type": "xy"}]]
    )

    # Graphe genre
    fig.add_trace(
        go.Bar(
            x=["Fille", "Garçon"],
            y=genre_counts.values,
            marker_color="cornflowerblue",
            showlegend=False
        ),
        row=1, col=1
    )

    # Graphe niveau
    fig.add_trace(
        go.Bar(
            x=["6e", "5e", "4e", "3e"],
            y=niveau_counts.values,
            marker_color="orange",
            showlegend=False
        ),
        row=1, col=2
    )

    fig.update_layout(
        # title_text="Nombre d'élèves par genre et niveau",
        height=400,
        width=300,
        margin=dict(t=30)
    )

    return fig
