from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "Api Python"
app.version = "2.0"

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 3,
        'title': 'Gravedad',
        'overview': "Pelicula en el espacio",
        'year': '2018',
        'rating': 7.7,
        'category': 'Ficcion'    
    }

]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')


@app.get('/movies', tags=['movies'])
def get_movies():
    return movies


@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
    for item in movies:
        if item["id"] == id:
            return item
        return []

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str, year: int):
        return [ item for item in movies if item['category'] == category]