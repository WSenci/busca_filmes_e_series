import requests
from tkinter import *

API_KEY = "758c966fcd7292ff4a1dcc51479f21a9"
BASE_URL = "https://api.themoviedb.org/3"

def search_movie(movie_name):
    endpoint = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": movie_name,
        "language": "pt-BR"
    }
    
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro: {response.status_code}")
        return None

def search_serie(series_name):
    endpoint = f"{BASE_URL}/search/tv"
    params = {
        "api_key": API_KEY,
        "query": series_name,
        "language": "pt-BR"
    }
    
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro: {response.status_code}")
        return None

def search_all(query):
    movies = search_movie(query)
    series = search_serie(query)

    all_results = {
        "movies": movies.get('result', []) if movies else [],
        "series": series.get('results', []) if series else []
    }

    return all_results

# resultado = search_movie("Interestelar")
# if resultado:
#     for movie in resultado.get('results', []):
#         print(f"Título: {movie['title']}, Lançamento: {movie['release_date']}")

# resultado = search_serie("Breaking Bad")
# if resultado:
#     for serie in resultado.get('results', []):
#         print(f"Título: {serie['name']}, Lançamento: {serie['first_air_date']}")

query = "The Witcher"
resultado = search_all(query)
print("Filmes:")
for movie in resultado['movies']:
    print(f"Título: {movie['title']}, Lançamento: {movie['release_date']}")

print("\nSéries:")
for serie in resultado['series']:
    print (f"Título: {serie['name']}, Lançamento: {serie['first_air_date']}")
