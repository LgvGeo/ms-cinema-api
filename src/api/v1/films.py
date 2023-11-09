import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from response_models.film import MovieResponse, MoviesListResponse
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get('/search', response_model=list[MoviesListResponse])
async def get_films_by_search(
    query: str | None = None,
    page_size: int = 50,
    page_number: int = 1,
    film_service: FilmService = Depends(get_film_service)
) -> list[MoviesListResponse]:
    films = await film_service.get_films(page_size, page_number, title=query)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='films not found'
        )
    return [MoviesListResponse(**film.model_dump()) for film in films]


@router.get('/{film_id}', response_model=MovieResponse)
async def get_film_details(
    film_id: str,
    film_service: FilmService = Depends(get_film_service)
) -> MovieResponse:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='film not found'
        )
    return MovieResponse(**film.model_dump())


@router.get('', response_model=list[MoviesListResponse])
async def get_films(
    page_size: int = 50,
    page_number: int = 1,
    sort: str | None = None,
    genre: uuid.UUID | None = None,
    film_service: FilmService = Depends(get_film_service)
) -> list[MoviesListResponse]:
    films = await film_service.get_films(page_size, page_number, sort, genre)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='films not found'
        )
    return [MoviesListResponse(**film.model_dump()) for film in films]
