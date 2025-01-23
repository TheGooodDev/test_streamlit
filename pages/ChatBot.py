import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
    # Options pour Chrome en mode "headless" (sans interface graphique)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    # On effectue la recherche directement via l’URL (ex: blogdumoderateur)
    driver.get(f"https://www.blogdumoderateur.com/?s={query}")

    # Attendre un peu le chargement
    time.sleep(2)

    # Récupérer les balises <article>
    articles_html = driver.find_elements(By.CSS_SELECTOR, 'article')
    
    results = []
    for article in articles_html:
        try:
            # Titre dans div.entry-excerpt
            title = article.find_element(By.CSS_SELECTOR, 'div.entry-excerpt').text
            # Lien dans le premier <a> trouvé
            link = article.find_element(By.CSS_SELECTOR, 'a').get_attribute("href")
            # Image dans la balise <img>
            img = article.find_element(By.CSS_SELECTOR, 'img').get_attribute("src")

            results.append({"title": title, "link": link, "img": img})
        except:
            pass

    driver.quit()
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
