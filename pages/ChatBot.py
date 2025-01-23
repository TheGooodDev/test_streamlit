import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

st.set_page_config(page_title="News Scraper Bot", layout="centered")
st.title("News Scraper Bot")

# Initialisation de l'historique de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Champ de saisie de l'utilisateur
prompt = st.chat_input("Tapez un mot-clé ou une requête pour rechercher des articles...")

def scrape_news(query: str):
    """
    Cherche des articles sur blogdumoderateur.com à l'aide de BeautifulSoup.
    Renvoie une liste de dictionnaires : {"title", "link", "img"}.
    """
    url = f"https://www.blogdumoderateur.com/?s={query}"
    # Effectue la requête HTTP
    response = requests.get(url)
    
    # Petite pause pour éviter de spammer
    time.sleep(1)
    
    # On parse le HTML
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Sélection de tous les <article>
    articles_html = soup.select("article")
    
    results = []
    for article in articles_html:
        try:
            # Récupère le titre (situé dans div.entry-excerpt, par exemple)
            title_div = article.select_one("div.entry-excerpt")
            if not title_div:
                continue
            title = title_div.get_text(strip=True)
            
            # Récupère le lien (via le premier <a>)
            link_a = article.select_one("a")
            if not link_a:
                continue
            link = link_a.get("href")
            
            # Récupère l'image (balise <img>)
            img_tag = article.select_one("img")
            img = img_tag.get("src") if img_tag else None
            
            # On ajoute seulement si titre/lien valides
            results.append({"title": title, "link": link, "img": img})
        except Exception:
            # En cas d'erreur, on ignore l'article
            pass

    return results

if prompt:
    # Affiche la requête de l’utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Scraping des articles correspondants
    articles = scrape_news(prompt)
    if not articles:
        response_text = f"Je n'ai trouvé aucun article pour '{prompt}'."
    else:
        # Construit la réponse pour affichage
        response_text = "## Voici quelques articles trouvés :\n\n"
        
        for i, art in enumerate(articles, 1):
            response_text += (
                f"### Article {i}\n\n"
                f"![Aperçu de l'image]({art['img']})\n\n"
                f"**[{art['title']}]({art['link']})**\n\n"
                f"---\n\n"
            )

    # Affichage de la réponse dans la conversation
    with st.chat_message("assistant"):
        st.markdown(response_text)

    # Ajout de la réponse de l’assistant à l’historique
    st.session_state.messages.append({"role": "assistant", "content": response_text})
