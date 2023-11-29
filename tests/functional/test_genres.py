from http import HTTPStatus

from tests.testdata.genres_data import GENRES_DATA, TEST_GENRE


class TestGenres:
    async def test_returning_all_genres(self, get_data):

        """
            All genres from test data are expected to be returned
        """

        response = await get_data('/api/v1/genres')
        right_response = [
            {
                'id': x['id'],
                'name': x['name']
            } for x in GENRES_DATA
        ]

        assert response.status == HTTPStatus.OK
        assert sorted(response.body, key=lambda x: x['name']) == right_response

    async def test_get_genre_by_id(self, get_data):

        """
            genre with given id is expected to be returned
        """

        id = 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95'
        response = await get_data(f'/api/v1/genres/{id}')

        assert response.status == HTTPStatus.OK
        assert response.body == TEST_GENRE

    async def test_get_genre_by_id_if_does_not_exist(self, get_data):

        """
            genre with given id is not expected to be returned
        """

        id = 'ef86b8ff-3c82-4d31-nnne-72b69f4e3f95'
        response = await get_data(f'/api/v1/genres/{id}')

        assert response.status == HTTPStatus.NOT_FOUND

    async def test_genre_cached(self, get_data_from_cache, get_data):

        """
            Test caching
        """

        id = 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95'
        await get_data(f'/api/v1/genres/{id}')
        data = await get_data_from_cache(f'genre:{id}')

        assert data == TEST_GENRE
