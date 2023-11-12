from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from models.response_models.genre import GenreListResponse, GenreResponse
from services.genre import GenreService, get_genre_service
from settings.messages import GENRE_NOT_FOUND

router = APIRouter()


@router.get(
        '/{genre_id}',
        response_model=GenreResponse,
        summary="Get genre",
        description="Get genre with all details if exists"
)
async def get_genre_details(
    genre_id: str,
    genre_service: GenreService = Depends(get_genre_service)
) -> GenreResponse:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=GENRE_NOT_FOUND
        )
    return GenreResponse(**genre.model_dump())


@router.get(
        '',
        response_model=list[GenreListResponse],
        summary="Get genres",
        description="Get genres list"
)
async def get_genres(
    genre_service: GenreService = Depends(get_genre_service)
) -> list[GenreListResponse]:
    genres = await genre_service.get_genres()
    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=GENRE_NOT_FOUND
        )
    return [GenreListResponse(**genre.model_dump()) for genre in genres]
