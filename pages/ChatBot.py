import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

st.set_page_config(page_title="News Scraper Bot", layout="centered")
st.title("News Scraper Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Tapez un mot-clé ou une requête pour rechercher des articles...")

def scrape_news(query: str):
    """
    Cherche des articles sur blogdumoderateur.com à l'aide de BeautifulSoup.
    Renvoie une liste de dictionnaires : {"title", "link", "img"}.
    """
    url = f"https://www.blogdumoderateur.com/?s={query}"
    response = requests.get(url)
    
    time.sleep(1)
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    articles_html = soup.select("article")
    
    results = []
    for article in articles_html:
        try:
            title_div = article.select_one("div.entry-excerpt")
            if not title_div:
                continue
            title = title_div.get_text(strip=True)
            
            link_a = article.select_one("a")
            if not link_a:
                continue
            link = link_a.get("href")
            
            img_tag = article.select_one("img")
            img = img_tag.get("src") if img_tag else None
            
            results.append({"title": title, "link": link, "img": img})
        except Exception:
            pass

    return results

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    articles = scrape_news(prompt)
    if not articles:
        response_text = f"Je n'ai trouvé aucun article pour '{prompt}'."
    else:
        response_text = "## Voici quelques articles trouvés :\n\n"
        
        for i, art in enumerate(articles, 1):
            response_text += (
                f"### Article {i}\n\n"
                f"![Aperçu de l'image]({art['img']})\n\n"
                f"**[{art['title']}]({art['link']})**\n\n"
                f"---\n\n"
            )

    with st.chat_message("assistant"):
        st.markdown(response_text)

    st.session_state.messages.append({"role": "assistant", "content": response_text})
