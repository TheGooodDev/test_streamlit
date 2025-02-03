import streamlit as st
import requests

# Titre de la page
st.title("Formulaire de Prediction avec appel à l'API")

# Création du formulaire Streamlit
with st.form("prediction_form"):
    st.subheader("Veuillez renseigner les informations suivantes :")

    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=0, max_value=120, value=25, step=1)
    graduated = st.selectbox("Graduated", ["Yes", "No"])
    profession = st.selectbox("Gender", ["Healthcare", "Engineer", "Lawyer","Artist","Doctor","Homemaker","Entertainment","Executive"])
    work_experience = st.number_input("Work Experience (années)",
                                      min_value=0.0,
                                      max_value=50.0,
                                      value=2.0,
                                      step=0.5)
    spending_score = st.selectbox("Spending Score", ["Low", "Average", "High"])
    family_size = st.number_input("Family Size",
                                  min_value=0.0,
                                  max_value=20.0,
                                  value=3.0,
                                  step=1.0)
    segmentation = st.selectbox("Segmentation", ["A", "B", "C", "D"])

    submitted = st.form_submit_button("Envoyer")

# Si l'utilisateur clique sur "Envoyer"
if submitted:
    # Construire le dictionnaire de données
    data = {
        "Gender": gender,
        "Age": age,
        "Graduated": graduated,
        "Profession": profession,
        "Work_Experience": work_experience,
        "Spending_Score": spending_score,
        "Family_Size": family_size,
        "Segmentation": segmentation
    }

    # URL de l'endpoint FastAPI
    url = "https://ynov-api-e3cc457fe7a3.herokuapp.com/predict"

    # Effectuer la requête POST en envoyant le JSON
    try:
        response = requests.post(url, json=data)
        # Vérifier le code de statut
        if response.status_code == 200:
            # Récupérer la réponse sous forme JSON
            result = response.json()
            # if 1 is married if 0 not married
            if result[0] == 1:
                st.success("Vous êtes marié")
            else:
                st.success("Vous n'êtes pas marié")

        else:
            st.error(f"Erreur {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Une erreur est survenue lors de l'appel à l'API : {e}")
