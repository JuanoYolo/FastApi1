from fastapi import Depends, FastAPI, Body, Path, Query, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title = "Api Python"
app.version = "2.0"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales invalidas")

class User(BaseModel):
    email: str
    password: str

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

@app.post('/login',tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
    return JSONResponse(status_code=200, content=token)

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
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
