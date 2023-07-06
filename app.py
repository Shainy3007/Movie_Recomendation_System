import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    dist = similarity[movie_index]
    movies_list = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:6]
    recommended = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended.append(movies.iloc[i[0]].title)
    return recommended, recommended_movie_posters


st.title('Movie Recommender System')
option = st.selectbox('', movies['title'].values)

if st.button('Recommend'):
    recomendations, posters = recommend(option)
    col1, col2, col3, col4, = st.columns(4)
    with col1:
        st.text(recomendations[0])
        st.image(posters[0])
    with col2:
        st.text(recomendations[1])
        st.image(posters[1])
    with col3:
        st.text(recomendations[3])
        st.image(posters[3])
    with col4:
        st.text(recomendations[4])
        st.image(posters[4])



