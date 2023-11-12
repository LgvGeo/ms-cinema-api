from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from models.response_models.person import PersonListResponse, PersonResponse
from services.person import PersonService, get_person_service
from settings.messages import PERSON_NOT_FOUND

router = APIRouter()


@router.get(
        '/search',
        response_model=list[PersonListResponse],
        summary="Search persons",
        description="Search persons by name"
)
async def get_persons_by_search(
    name: str | None = None,
    page_size: Annotated[
        int, Query(description='Pagination page size', ge=1)] = 10,
    page_number: Annotated[int, Query(description='Page number', ge=1)] = 1,
    film_service: PersonService = Depends(get_person_service)
) -> list[PersonListResponse]:
    persons = await film_service.get_persons(
        page_size, page_number, name=name)
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PERSON_NOT_FOUND
        )
    return [PersonListResponse(**person.model_dump()) for person in persons]


@router.get(
        '/{person_id}',
        response_model=PersonResponse,
        summary="Get person",
        description="Get person with all details if exists"
)
async def get_person_details(
    person_id: str,
    person_service: PersonService = Depends(get_person_service)
) -> PersonResponse:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PERSON_NOT_FOUND
        )
    return PersonResponse(**person.model_dump())


@router.get(
        '',
        response_model=list[PersonListResponse],
        summary="Get persons",
        description="Get persons list"
)
async def get_persons(
    page_size: Annotated[
        int, Query(description='Pagination page size', ge=1)] = 10,
    page_number: Annotated[int, Query(description='Page number', ge=1)] = 1,
    person_service: PersonService = Depends(get_person_service)
) -> list[PersonListResponse]:
    persons = await person_service.get_persons(page_size, page_number)
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PERSON_NOT_FOUND
        )
    return [PersonListResponse(**person.model_dump()) for person in persons]
