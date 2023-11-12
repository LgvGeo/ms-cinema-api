import uuid
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from models.response_models.film import MovieResponse, MoviesListResponse
from services.film import FilmService, get_film_service
from settings.messages import FILM_NOT_FOUND

router = APIRouter()


@router.get(
        '/search',
        response_model=list[MoviesListResponse],
        summary="Search films",
        description="Search films by title"

)
async def get_films_by_search(
    query: str | None = None,
    page_size: Annotated[
        int, Query(description='Pagination page size', ge=1)] = 10,
    page_number: Annotated[int, Query(description='Page number', ge=1)] = 1,
    film_service: FilmService = Depends(get_film_service)
) -> list[MoviesListResponse]:
    films = await film_service.get_films(page_size, page_number, title=query)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=FILM_NOT_FOUND
        )
    return [MoviesListResponse(**film.model_dump()) for film in films]


@router.get(
        '/{film_id}',
        response_model=MovieResponse,
        summary="Get film",
        description="Get film with all details if exists"
)
async def get_film_details(
    film_id: str,
    film_service: FilmService = Depends(get_film_service)
) -> MovieResponse:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=FILM_NOT_FOUND
        )
    return MovieResponse(**film.model_dump())


@router.get(
        '',
        response_model=list[MoviesListResponse],
        summary="Get films",
        description="Get films list"
)
async def get_films(
    page_size: Annotated[
        int, Query(description='Pagination page size', ge=1)] = 10,
    page_number: Annotated[int, Query(description='Page number', ge=1)] = 1,
    sort: str | None = None,
    genre: uuid.UUID | None = None,
    film_service: FilmService = Depends(get_film_service)
) -> list[MoviesListResponse]:
    films = await film_service.get_films(page_size, page_number, sort, genre)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=FILM_NOT_FOUND
        )
    return [MoviesListResponse(**film.model_dump()) for film in films]
