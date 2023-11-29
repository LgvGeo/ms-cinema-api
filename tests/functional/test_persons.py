from http import HTTPStatus

from tests.testdata.persons_data import PERSONS_DATA, TEST_PERSON


class TestPersons:
    async def test_returning_all_persons(self,  get_data):

        """
            All persons from test data are expected to be returned
        """

        params = {'page_size': 100}
        response = await get_data('/api/v1/persons', params=params)
        right_response = [
            {
                'id': x['id'],
                'name': x['name']
            } for x in PERSONS_DATA
        ]
        assert response.status == HTTPStatus.OK
        assert response.body == right_response

    async def test_getting_person_by_id(self, get_data):

        """
        person with given id is expected to be returned
        """

        id = '2d6f6284-13ce-4d25-9453-c4335432c116'
        response = await get_data(f'/api/v1/persons/{id}')
        assert response.status == HTTPStatus.OK
        assert response.body == TEST_PERSON

    async def test_getting_person_by_id_if_does_not_exist(self, get_data):

        """
        person with given id does not exist and is not expected to be returned
        """

        id = 'ef86b8ff-3c82-4d31-ad8e-7nnnnf4e3f95'

        response = await get_data(f'/api/v1/persons/{id}')
        assert response.status == HTTPStatus.NOT_FOUND

    async def test_search_person(self, get_data):

        """
        Test search person by name.
        """

        name = 'adam'
        params = {'name': name}
        right_response = [
            {
                'id': TEST_PERSON['id'],
                'name': TEST_PERSON['name']
            }
        ]
        response = await get_data('/api/v1/persons/search', params)
        assert response.status == HTTPStatus.OK
        assert response.body == right_response

    async def test_pagination(self, get_data):

        """
        Test pagination.
        """

        params = {'page_size': 4, 'page_number': 1}
        response = await get_data('/api/v1/persons', params=params)
        assert response.status == HTTPStatus.OK
        assert len(response.body) == 4

    async def test_person_cached(self, get_data_from_cache, get_data):

        """
        Test caching
        """

        id = '2d6f6284-13ce-4d25-9453-c4335432c116'

        await get_data(f'/api/v1/persons/{id}')
        data = await get_data_from_cache(f'person:{id}')
        assert data == TEST_PERSON
