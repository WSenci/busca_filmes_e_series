import requests
from tkinter import *
from PIL import Image, ImageTk

API_KEY = "758c966fcd7292ff4a1dcc51479f21a9"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w200"

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

    for widget in result_frame.winfo_children():
        widget.destroy()

    row_counter = 0
    if movies and movies.get('results'):
        Label(result_frame, text="Filmes:", font=("Arial", 14, "bold")).grid(column=0, row=row_counter, padx=10, pady=10)
        row_counter += 1
        display_results(movies.get('results'), result_frame, row_offset=row_counter)
        row_counter += len(movies.get('results'))

    if series and series.get('results'):
        Label(result_frame, text="Séries:", font=("Arial", 14, "bold")).grid(column=0, row=row_counter, padx=10, pady=10)
        row_counter += 1
        display_results(series.get('results'), result_frame, row_offset=row_counter)

    result_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def display_results(results, frame, row_offset):
    for idx, item in enumerate(results):
        col = idx % 3
        row = row_offset + (idx // 3) * 2

        poster_path = item.get('poster_path')
        if poster_path:
            image_url = f"{IMAGE_BASE_URL}{poster_path}"
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                image_data = response.raw
                img = Image.open(image_data)
                img = img.resize((100, 150), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)

                img_label = Label(frame, image=photo)
                img_label.image = photo
                img_label.grid(column=col, row=row, padx=10, pady=10)

        title = item.get('title') or item.get('name', "Título não disponível")
        date = item.get('release_date') or item.get('first_air_date', "Data não disponível")
        text_label = Label(frame, text=f"{title}\n{date}", font=("Arial", 12), justify="center", wraplength=100)
        text_label.grid(column=col, row=row + 1, padx=10, pady=10)

def fetch_filtered_movies():
    endpoint = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "language": "pt-BR",
        "sort_by": "vote_average.desc",
        "vote_count.gte": 1000
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro: {response.status_code}")
        return None

def fetch_filtered_series():
    endpoint = f"{BASE_URL}/discover/tv"
    params = {
        "api_key": API_KEY,
        "language": "pt-BR",
        "sort_by": "vote_average.desc",
        "vote_count.gte": 500
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro: {response.status_code}")
        return None

def show_top_rated_movies():
    movies = fetch_filtered_movies()

    for widget in result_frame.winfo_children():
        widget.destroy()

    if movies and movies.get('results'):
        Label(result_frame, text="Filmes Mais Bem Avaliados:", font=("Arial", 14, "bold")).grid(column=0, row=0, padx=10, pady=10)
        display_results(movies.get('results'), result_frame, row_offset=1)

    result_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def show_top_rated_series():
    series = fetch_filtered_series()

    for widget in result_frame.winfo_children():
        widget.destroy()

    if series and series.get('results'):
        Label(result_frame, text="Séries Mais Bem Avaliadas:", font=("Arial", 14, "bold")).grid(column=0, row=0, padx=10, pady=10)
        display_results(series.get('results'), result_frame, row_offset=1)

    result_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_mouse_wheel(event):
    if event.num == 4:
        canvas.yview_scroll(-1, "units")
    elif event.num == 5:
        canvas.yview_scroll(1, "units")
    else:
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

janela = Tk()
janela.title("Busca Filmes e Séries - Python")
janela.geometry("1280x720")

titulo = Label(janela, text="Coloque o nome do filme ou da série:", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

inputBusca = Entry(janela, width=40, bg="White", font=("Arial", 14))
inputBusca.pack(pady=10)

botaoBusca = Button(janela, text="Buscar", bg="#3b0b66", fg="white", width=8, height=2, command=search_all)
botaoBusca.pack(pady=10)

botaoMelhoresFilmes = Button(janela, text="Melhores Filmes", bg="#3b0b66", fg="white", width=15, height=2, command=show_top_rated_movies)
botaoMelhoresFilmes.pack(pady=10)

botaoMelhoresSeries = Button(janela, text="Melhores Séries", bg="#3b0b66", fg="white", width=15, height=2, command=show_top_rated_series)
botaoMelhoresSeries.pack(pady=10)

main_frame = Frame(janela)
main_frame.pack(fill=BOTH, expand=1)

canvas = Canvas(main_frame)
canvas.pack(side=LEFT, fill=BOTH, expand=1)

scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

canvas.bind_all("<MouseWheel>", on_mouse_wheel)
canvas.bind_all("<Button-4>", on_mouse_wheel)
canvas.bind_all("<Button-5>", on_mouse_wheel)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

result_frame = Frame(canvas)
canvas.create_window((0, 0), window=result_frame, anchor="nw")

janela.mainloop()
