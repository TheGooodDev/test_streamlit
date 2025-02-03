import streamlit as st
import streamlit.components.v1 as components

# Configuration de la page (optionnel)
st.set_page_config(
    page_title="Doc API intégrée en iFrame",
    layout="wide"
)

st.title("Intégration de la documentation de l'API en iFrame")
st.markdown(
    """
    <style>
    /* Sélecteur CSS du conteneur iFrame, 
       Streamlit ajoute généralement un ID auto-généré
       donc il faut parfois cibler "iframe" directement */
    iframe {
        filter: invert(1);
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Affichage de l'iframe
components.iframe(
    src="https://ynov-api-e3cc457fe7a3.herokuapp.com/docs",
    width=1200,
    height=800,
    scrolling=True
)
