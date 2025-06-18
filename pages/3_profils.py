
from utils.utils import authenticate,plot_cluster_profile, load_data, plot_single_cluster_distribution
import streamlit as st

nom = authenticate()

# ✅ Affichage unique du message de bienvenue
if st.session_state.get("show_welcome", False):
    st.success(f"Bienvenue {nom} 👋")
    st.info("👉 Pense à ouvrir le menu latéral à gauche pour explorer les pages de l'application.")
    st.session_state["show_welcome"] = False  # Ne plus l'afficher ensuite


df_scores = load_data("data/df_scores.csv")

st.subheader("Profilage des réponses")

st.markdown("Cette partie présente les profils d’élèves dégagés par analyse de similarité sur leurs réponses.")


st.markdown("""
Les élèves ont été regroupés en **profils types** selon leurs réponses à plusieurs dimensions du climat scolaire (confiance, bien-être, écoute, engagement).

Chaque profil regroupe des élèves aux **comportements et ressentis similaires**, déterminés automatiquement via une classification K-means.

- Le premier graphique montre le **score moyen par axe** pour chaque profil.
- Le second affiche la **répartition des élèves** par genre et niveau dans chaque profil.

Cela permet de mieux **comprendre les nuances de vécu** dans l’établissement et d’identifier les groupes d’élèves à soutenir ou valoriser.
""")


# Interface avec st.pills
# 💡 Initialisation de la valeur par défaut (au chargement de la page)
if "selected_profil" not in st.session_state:
    st.session_state.selected_profil = "Profil 1"  # Profil affiché par défaut

selected_label = st.pills(
    "Choisis un profil",
    options=[f"Profil {i + 1}" for i in sorted(df_scores["cluster_kmeans"].unique())],
    key="selected_profil"
)
repartition_profils = df_scores["cluster_kmeans"].value_counts(normalize=True).sort_index()

# Transforme en dictionnaire "Profil 1" → xx %
taille_profils = {
    f"Profil {k+1}": f"{round(p*100, 1)}%" for k, p in repartition_profils.items()}

with st.container(border=True):
    if selected_label:

        cluster_id = int(selected_label.split()[-1]) - 1
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Profil des scores moyens**")
            st.plotly_chart(plot_cluster_profile(df_scores, cluster_id))
        with col2:
            st.markdown("**Nombre d'élèves par genre et niveau**")
            st.plotly_chart(plot_single_cluster_distribution(df_scores, cluster_id), use_container_width=True)
        with col3:
                    # Contenu textuel associé
            commentaires = {
                "Profil 1": """
            - Climat très positif : **confiance (3.91)**, **expression (3.67)** et **bien-être (3.57)** à des niveaux élevés.
            - **Engagement également bon** : **1.94**, bien au-dessus des autres.
            - **Majorité de filles**, tous niveaux confondus.

            ➡️ Ce sont des élèves qui semblent globalement **épanouis et bien intégrés** dans leur environnement scolaire.
            """,
                "Profil 2": """

            - Scores très faibles sur tous les axes : **confiance (1.44)**, **bien-être (0.46)**, **expression (0.95)**, **engagement (0.99)**.
            - Surreprésentation d’élèves de **6e**, garçons majoritaires.

            ➡️ Ces élèves semblent vivre une **expérience scolaire très difficile et préoccupante**.
            """,
                "Profil 3": """

            - Confiance modérée (**2.90**), mais **bien-être faible (1.70)** et **expression limitée (1.82)**.
            - **Engagement relativement bon (2.17)**, supérieur à celui de certains autres profils.
            - **Filles très majoritaires**, plutôt de la **6e à la 4e**.

            ➡️ Ces élèves montrent un **ressenti fragile**, mais ils gardent **une certaine motivation**.
            """,
                "Profil 4": """
            - Climat relationnel assez bon : **confiance (3.12)**, **expression (2.74)**.
            - **Engagement extrêmement faible (0.29)**
            - **Profil plus masculin**, présence décroissante avec les niveaux.

            ➡️ Ces élèves sont **désengagés de la vie de l´établissement**, malgré un cadre relationnel perçu comme plutôt favorable.
            """
            }

            st.markdown("**Analyse**")
            st.markdown(f"Proportion d’élèves concernés : {taille_profils[selected_label]}")
            st.markdown(commentaires[selected_label])

st.info("""
        **À retenir :**

- Les élèves se répartissent en **4 profils distincts**, révélant une grande hétérogénéité dans le vécu scolaire.
- Un groupe majoritaire est **épanoui et engagé**, tandis qu’un autre cumule **mal-être, isolement et désengagement**, notamment chez les **garçons de 6e**.
- Deux profils intermédiaires témoignent d’un **ressenti fragile ou d’un désengagement silencieux**, malgré un climat parfois perçu comme favorable.
- Le **genre, le niveau** et surtout **l’engagement scolaire** structurent fortement ces profils.

""")
