from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from response_models.genre import GenreListResponse, GenreResponse
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get('/{genre_id}', response_model=GenreResponse)
async def get_genre_details(
    genre_id: str,
    genre_service: GenreService = Depends(get_genre_service)
) -> GenreResponse:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='genre not found'
        )
    return GenreResponse(**genre.model_dump())


@router.get('', response_model=list[GenreListResponse])
async def get_genres(
    genre_service: GenreService = Depends(get_genre_service)
) -> list[GenreListResponse]:
    genres = await genre_service.get_genres()
    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='genres not found'
        )
    return [GenreListResponse(**genre.model_dump()) for genre in genres]
