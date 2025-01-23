import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

uploaded_file = st.file_uploader("Choisissez un fichier", type="csv")
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file, sep=",")

    # Select columns or select all
    columns = st.multiselect('Sélectionnez les colonnes', dataframe.columns.sort_values())
    if not columns:
        columns = dataframe.columns
        columns.sort_values()

    edited_df = dataframe[columns]
    st.write(edited_df)

    # Select columns to display a graphique (axe x, and y)
    x = st.selectbox('Sélectionnez l\'axe des x', columns)
    y = st.selectbox('Sélectionnez l\'axe des y', columns)
    legend = st.checkbox('Afficher une légende')
    hue = None

    if legend:
        hue = st.selectbox('Sélectionnez la colonne pour la légende', columns)

    # Determine the type of plot based on data types
    fig, ax = plt.subplots()
    if dataframe[x].dtype == 'object' and dataframe[y].dtype == 'object':
        # If both x and y are categorical:
        if x == y: #if x and y are the same columns
            sns.countplot(x=x, hue=hue, data=edited_df, ax=ax)
        else: # if x and y are different columns do a cross tabulation
            cross_tab = pd.crosstab(edited_df[x], edited_df[y])
            cross_tab.plot(kind="bar", ax=ax, rot=0)
            ax.set_xlabel(x)
            ax.set_ylabel("Count")

    elif dataframe[x].dtype == 'object' and dataframe[y].dtype in ['int64', 'float64']:
        sns.boxplot(x=x, y=y, hue=hue, data=edited_df, ax=ax)
    elif dataframe[x].dtype in ['int64', 'float64'] and dataframe[y].dtype == 'object':
        sns.barplot(x=y, y=x, hue=hue, data=edited_df, ax=ax)
    elif dataframe[x].dtype in ['int64', 'float64'] and dataframe[y].dtype in ['int64', 'float64']:
        sns.scatterplot(x=x, y=y, hue=hue, data=edited_df, ax=ax)
    else:
        st.write("Types de données non supportés pour la visualisation.")

    st.pyplot(fig)