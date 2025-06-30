import streamlit as st
from utils.utils import (
    authenticate
)

nom = authenticate()

# ✅ Affichage unique du message de bienvenue
if st.session_state.get("show_welcome", False):
    st.success(f"Bienvenue {nom} 👋")
    st.info("👉 Pense à ouvrir le menu latéral à gauche pour explorer les pages de l'application.")
    st.session_state["show_welcome"] = False  # Ne plus l'afficher ensuite



# ◼ Bloc 1 : Idées à retenir
with st.container(border=True):
    st.subheader("✅ Idées clés à retenir")
    st.markdown("""
- **Sentiment de sécurité très positif**, mais **envie de venir à l'établissement très faible**.
- **Filles de 4e** : fortement engagées, écoutées, confiantes.
- **Garçons de 6e** : scores les plus faibles, isolement et désengagement.
- **4 profils-types** identifiés : du groupe épanoui au profil silencieux.
- **La cour** = lieu et moment de bien-être majeur.
- **L'écoute, le respect et la compréhension** sont les clés de la confiance pour les élèves.
- **Des changements concrets sont demandés** : horaires, cantine, climatisation, respect, liberté.
    """)

# ◼ Bloc 2 : Angles morts
with st.container(border=True):
    st.subheader(" 👀 Zones d'ombre et angles morts à explorer")
    st.markdown("""
- **Des élèves n'identifient aucun lieu ni adulte où s'exprimer.**
- **Salle de classe très ambivalente** : lieu agréable pour certains, oppressant pour d'autres.
- **Engagement déconnecté du climat relationnel** : faut-il revoir nos projets pédagogiques ?
- **Profils silencieux sous-représentés dans les verbatims.**
- **Aucune mise en perspective avec les perceptions adultes.**
    """)


with st.container(border=True):
    st.subheader("🎯 Vers où aller ?")
    st.markdown("""
1. Comment faire évoluer ces constats vers un **plan d'action collectif** ?
2. Quels profils mériteraient **un accompagnement spécifique** ?
3. Quels **lieux, temps ou rituels scolaires** peuvent être transformés ?
4. Quelles **expérimentations pédagogiques** pour reconnecter engagement et bien-être ?
    """)
