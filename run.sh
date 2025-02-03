# Création d'une image docker
docker build . -t steamlit-dashboard

# Start un container
docker run -p 8501:8000 -e PORT=8501 -v "$(pwd):/home/app" -it steamlit-dashboard