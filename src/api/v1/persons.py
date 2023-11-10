from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from response_models.person import PersonListResponse, PersonResponse
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/search', response_model=list[PersonListResponse])
async def get_persons_by_search(
    name: str | None = None,
    page_size: int = 50,
    page_number: int = 1,
    film_service: PersonService = Depends(get_person_service)
) -> list[PersonListResponse]:
    persons = await film_service.get_persons(
        page_size, page_number, name=name)
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='persons not found'
        )
    return [PersonListResponse(**person.model_dump()) for person in persons]


@router.get('/{person_id}', response_model=PersonResponse)
async def get_person_details(
    person_id: str,
    person_service: PersonService = Depends(get_person_service)
) -> PersonResponse:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='person not found'
        )
    return PersonResponse(**person.model_dump())


@router.get('', response_model=list[PersonListResponse])
async def get_persons(
    page_size: int = 50,
    page_number: int = 1,
    person_service: PersonService = Depends(get_person_service)
) -> list[PersonListResponse]:
    persons = await person_service.get_persons(page_size, page_number)
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='persons not found'
        )
    return [PersonListResponse(**person.model_dump()) for person in persons]
