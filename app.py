import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import re

# Charger le dataset
file_path = "steam_games.csv"
df = pd.read_csv(file_path)

# Création de l'application Streamlit
st.title("Analyse des Jeux Steam")
st.write("Ce projet permet d'explorer et d'analyser un dataset de jeux Steam.")

# Sélection de l'analyse
option = st.selectbox(
    "Quel type de graphique souhaitez-vous afficher ?",
    ["Distribution des genres", "Distribution des évaluations", "Top éditeurs", "Répartition des prix", "Évolution du nombre de jeux par année"]
)

# Analyse des genres
def plot_genres():
    df['genre'] = df['genre'].dropna()
    all_genres = df['genre'].str.split(',').explode()
    top_genres = all_genres.value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    top_genres.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title("Top 10 des genres les plus fréquents sur Steam")
    ax.set_xlabel("Genres")
    ax.set_ylabel("Nombre de jeux")
    st.pyplot(fig)

# Analyse des évaluations
def plot_reviews():
    if 'all_reviews' in df.columns:
        df['all_reviews_cleaned'] = df['all_reviews'].str.extract(r'(\d+)')
        df['all_reviews_cleaned'] = pd.to_numeric(df['all_reviews_cleaned'], errors='coerce')
        df['all_reviews_normalized'] = (df['all_reviews_cleaned'] - df['all_reviews_cleaned'].min()) / \
                                       (df['all_reviews_cleaned'].max() - df['all_reviews_cleaned'].min())
        
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df['all_reviews_normalized'].dropna(), bins=50, kde=True, color='orange', ax=ax)
        ax.set_title("Distribution normalisée des évaluations des utilisateurs")
        ax.set_xlabel("Score des évaluations normalisé")
        ax.set_ylabel("Nombre de jeux")
        st.pyplot(fig)
    else:
        st.write("⚠️ La colonne 'all_reviews' n'existe pas dans le dataset !")

# Analyse des éditeurs
def plot_publishers():
    top_publishers = df['publisher'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    top_publishers.plot(kind='bar', color='green', ax=ax)
    ax.set_title("Top 10 des éditeurs de jeux sur Steam")
    ax.set_xlabel("Éditeurs")
    ax.set_ylabel("Nombre de jeux")
    st.pyplot(fig)

# Répartition des prix
def plot_prices():
    if 'original_price' in df.columns:
        df['original_price'] = df['original_price'].replace('[\$,Free]', '', regex=True)
        df['original_price'] = pd.to_numeric(df['original_price'], errors='coerce')
        
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df['original_price'].dropna(), bins=50, kde=True, color='purple', ax=ax)
        ax.set_title("Répartition des prix des jeux sur Steam")
        ax.set_xlabel("Prix ($)")
        ax.set_ylabel("Nombre de jeux")
        st.pyplot(fig)

# Évolution du nombre de jeux par année
def plot_games_over_time():
    if 'release_date' in df.columns:
        df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year
        games_per_year = df['release_year'].value_counts().sort_index()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        games_per_year.plot(kind='line', color='red', ax=ax)
        ax.set_title("Évolution du nombre de jeux publiés par année")
        ax.set_xlabel("Année")
        ax.set_ylabel("Nombre de jeux")
        st.pyplot(fig)

# Afficher le graphique correspondant au choix de l'utilisateur
if option == "Distribution des genres":
    plot_genres()
elif option == "Distribution des évaluations":
    plot_reviews()
elif option == "Top éditeurs":
    plot_publishers()
elif option == "Répartition des prix":
    plot_prices()
elif option == "Évolution du nombre de jeux par année":
    plot_games_over_time()