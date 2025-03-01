from http.client import responses

import streamlit as st
import pickle
import pandas as pd
import requests
import os

port = int(os.environ.get("PORT", 8501))


def fetch_poster(movie_id):
    response=requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=aed98b0b6bd6e21b44f8a3b66c95c5ce&language=en-US')
    data=response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']



def recommened(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommened_movies = []
    recommened_movies_posters=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommened_movies.append(movies.iloc[i[0]].title)
        # fetching poster from api
        recommened_movies_posters.append(fetch_poster(movie_id))
    return recommened_movies,recommened_movies_posters
    

movies_dict=pickle.load(open('movie_dict.pkl', 'rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name=st.selectbox(
    'Search Your movies',
    movies['title'].values
)

if st.button('Recommend'):
    names,posters=recommened(selected_movie_name)

    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
