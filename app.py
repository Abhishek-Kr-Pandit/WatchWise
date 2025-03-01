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
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:8]

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

st.title('Get Your Favourite Movies')

selected_movie_name=st.selectbox(
    'Search Your movies',
    movies['title'].values
)

if st.button('Recommend'):
    names,posters=recommened(selected_movie_name)

    cols = st.columns(5)

    for i in range(min(7, len(names))):
        with cols[i % 5]:
            st.text(names[i])
            st.image(posters[i], use_container_width=True)

