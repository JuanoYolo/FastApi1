from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "Api Python"
app.version = "2.0"

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5,max_length=15)
    overview: str= Field(min_length=5, max_length=50)
    year: int = Field(le=2023)
    rating: float = Field(ge = 1,le=10)
    category: str = Field(min_length=5,max_length=15)

    class Config:
        schema_extra = {
            "example" : {
                "id": 1,
                "Title": "Pelicula",
                'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
                'year': 2009,
                'rating': 7.8,
                'category': 'Acción'  

            }
        }

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


@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)


@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=movies)
        return JSONResponse(status_code=404, content=[])

@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5,max_length=15)) -> List[Movie]:
        data = [ item for item in movies if item['category'] == category]
        return JSONResponse(content=data)


@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movie_list.append(movie.dict())
    return JSONResponse(status_code=201, content={"Message": "Se ha registrado la pelicula"})


@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movies(id: int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category

            return JSONResponse(status_code=200, content={"Message": "Se ha modificado la pelicula"})

@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movies(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"Message": "Se ha eliminado la pelicula"})
