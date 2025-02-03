FROM continuumio/miniconda3

# Définir le répertoire de travail
WORKDIR /home/app

# Copier le fichier des dépendances en premier (pour profiter du cache Docker)
COPY requirements.txt .

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'app (Streamlit + autres fichiers nécessaires)
COPY Dashboard.py .
COPY pages/ ./pages
COPY .streamlit ./.streamlit


# Lancer Streamlit en utilisant la variable d'environnement $PORT
CMD ["sh", "-c", "streamlit run Dashboard.py --server.port=$PORT --server.address=0.0.0.0"]
