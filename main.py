import requests

# Substitua pela sua chave de API
API_KEY = "758c966fcd7292ff4a1dcc51479f21a9"
BASE_URL = "https://api.themoviedb.org/3"

# Exemplo: Pesquisar por um filme
def search_movie(movie_name):
    endpoint = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": movie_name,
        "language": "pt-BR"  # Para resultados em português
    }
    
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro: {response.status_code}")
        return None

# Exemplo de uso
resultado = search_movie("ruptura")
if resultado:
    for movie in resultado.get('results', []):
        print(f"Título: {movie['title']}, Lançamento: {movie['release_date']}")
