import streamlit as st
import pandas as pd
import seaborn as sns

st.set_page_config(page_title='Dashboard', page_icon=':bar_chart:', layout='wide', initial_sidebar_state='auto')

# Title
st.title('Dashboard')

# SubTitle
st.subheader('This is a subheader')

#Text
st.write('Présentation de données avec Streamlit')

@st.cache_data
def load_data():
    return pd.read_csv('https://raw.githubusercontent.com/Quera-fr/Python-Programming/refs/heads/main/data.csv')

df = load_data()
# Champ de texte
name = st.text_input('Entrez votre texte')

st.write(f'Bonjour {name}')

# Checkbox
if st.checkbox('Afficher les données'):
    st.write(df)

# Image
st.sidebar.image('https://www.streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png', width=300)

st.sidebar.video('https://www.youtube.com/watch?v=JwSS70SZdyM')



with st.form(key='my_form'):

    col1, col2 = st.columns(2)

    with col1:
        profession = st.selectbox("Choissisez une profession",df.Profession.unique())
        data_age =df[df.Profession == profession].Age
        # slider
        age = st.slider('Age', min_value=0, max_value=100, value=(data_age.min(), data_age.max()), )

    with col2:
        data_age = df[(df.Profession == profession) & (df.Age >= age[0]) & (df.Age <= age[1])].Age

        if st.form_submit_button(label='Valider'):
            plot = sns.histplot(data_age, kde=True)
            st.pyplot(plot.figure)


# camera
