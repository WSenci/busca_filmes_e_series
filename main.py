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

def search_all():
    query = inputBusca.get()
    movies = search_movie(query)
    series = search_serie(query)

    all_results = {
        "movies": movies.get('result', []) if movies else [],
        "series": series.get('results', []) if series else []
    }

    filmes = Label(janela, text="Filmes:", font=("Arial", 14))
    filmes.grid(column=0, row=2, padx=10, pady=10)
    for movie in all_results['movies']:
        print(f"Título: {movie['title']}, Lançamento: {movie['release_date']}")

    series = Label(janela, text="Séries:", font=("Arial", 14))
    series.grid(column=0, row=4, padx=10, pady=10)
    for serie in all_results['series']:
        print (f"Título: {serie['name']}, Lançamento: {serie['first_air_date']}")

    return 

janela = Tk()
janela.title("Busca Filmes e Séries - Python")
janela.geometry("1280x720")
# janela.attributes('-fullscreen', True) colocar janela em fullscreen

titulo = Label(janela, text="Coloque o nome do filme ou da série:", font=("Arial", 16, "bold"))
titulo.grid(column=0, row=0, padx=10, pady=10)

inputBusca = Entry(width=20, bg="White", font=("Arial", 14))
inputBusca.grid(column=0, row=1, padx=10, pady=10)

botaoBusca = Button(janela, text="Buscar", bg="#3b0b66", fg="white", width=8, height=2, command=search_all)
botaoBusca.grid(column=1, row=1, padx=10, pady=10)

janela.mainloop()