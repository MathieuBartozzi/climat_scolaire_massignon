
# import streamlit as st
# import os

# # Définir l'état de connexion
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# # Fonctions de login/logout simples
# def login():
#     st.title("🔐 Connexion requise")
#     st.markdown("Cliquez sur le bouton pour accéder à l'application.")
#     if st.button("Se connecter"):
#         st.session_state.logged_in = True
#         st.rerun()

# def logout():
#     st.sidebar.write("Déconnexion")
#     if st.sidebar.button("Se déconnecter"):
#         st.session_state.logged_in = False
#         st.rerun()

# # Définir les pages comme objets
# dashboard = st.Page("pages/1_📊_Dashboard.py", title="Dashboard", icon="📊")
# ecarts = st.Page("pages/2_⚖️_Écarts_genre.py", title="Écarts F/G", icon="⚖️")
# ouvertes = st.Page("pages/3_💬_Questions_ouvertes.py", title="Réponses ouvertes", icon="💬")
# outils = st.Page("pages/4_🧰_Outils.py", title="Outils", icon="🧰")
# upload = st.Page("pages/5_⚙️_Upload.py", title="Données", icon="⚙️")

# login_page = st.Page(login, title="Connexion", icon="🔐")
# logout_page = st.Page(logout, title="Déconnexion", icon="🚪")

# # Navigation sécurisée
# if st.session_state.logged_in:
#     pg = st.navigation(
#         {
#             "Navigation": [dashboard, ecarts, ouvertes, outils],
#             "Données": [upload],
#             "Compte": [logout_page]
#         }
#     )
# else:
#     pg = st.navigation([login_page])


import streamlit as st

# 🌐 Configuration générale
st.set_page_config(page_icon="🏠",layout="wide")



# ✅ Accès autorisé
# st.title("📚 Climat scolaire – Portail d’analyse")

# user=st.user()

# # 🔐 Fonction de login avec message de restriction
# def login():
#     st.title("🔐 Accès restreint")
#     st.warning("Cette application est réservée aux utilisateurs autorisés.")
#     if user:
#         st.info(f"Vous êtes connecté en tant que : {user.email}")
#     else:
#         st.info("Connectez-vous avec un compte Google pour continuer.")

# # 🔓 Fonction de pseudo logout (affiche juste un message)
# def logout():
#     st.title("🔓 Session active")
#     st.info(f"Vous êtes connecté en tant que : {user.email}")
#     st.success("Pour vous déconnecter, fermez l’onglet ou déconnectez-vous de Streamlit Cloud.")

# 📁 Définir les pages comme objets
accueil = st.Page("pages/1_accueil.py", title="Accueil", icon="🏠")
dashboard = st.Page("pages/2_resultats_globaux.py", title="Résultats globaux", icon="📊")
ecarts = st.Page("pages/3_profils.py", title="Profils", icon="⚖️")
ouvertes = st.Page("pages/4_ouvertes.py", title="Réponses ouvertes", icon="💬")
# outils = st.Page("pages/5_🧰_Outils.py", title="Outils", icon="🧰")
# upload = st.Page("pages/6_⚙️_Upload.py", title="Données", icon="⚙️")

# login_page = st.Page(login, title="Connexion", icon="🔐")
# logout_page = st.Page(logout, title="Déconnexion", icon="🚪")

# # 🔁 Navigation conditionnelle en fonction de l'utilisateur
# if user and user.email in EMAILS_AUTORISÉS:
#     pg = st.navigation(
#         {
#             "Navigation": [dashboard, ecarts, ouvertes, outils],
#             "Données": [upload],
#             "Compte": [logout_page]
#         }
#     )
# else:
#     pg = st.navigation([login_page])

pg = st.navigation(
        {
            "Présentation": [accueil],
            "Navigation": [dashboard, ecarts, ouvertes]
        }
    )

pg.run()
