from http import HTTPStatus

from tests.testdata.movies_data import MOVIES_DATA, TEST_FILM


class TestFilms:
    async def test_returning_all_films(self, get_data):

        """
            All films from test data are expected to be returned
        """

        params = {'page_size': 100}
        response = await get_data('/api/v1/films', params=params)
        right_response = [
            {
                'id': x['id'],
                'title': x['title'],
                'imdb_rating': x['imdb_rating']
            } for x in MOVIES_DATA
        ]
        assert response.status == HTTPStatus.OK
        assert response.body == right_response

    async def test_genre_filtering(self, get_data):

        """
        Test genre filtering.
        Only one film exists with genre_id fb111f22-121e-44a7-b78f-b19191810fbf
        It means that just one film is expected to be returned
        """

        params = {
            'page_size': 100,
            'genre': 'fb111f22-121e-44a7-b78f-b19191810fbf'
        }
        response = await get_data('/api/v1/films', params=params)
        assert response.status == HTTPStatus.OK
        assert len(response.body) == 1

    async def test_getting_film_by_id(self, get_data):

        """
        film with given id is expected to be returned
        """

        id = 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95'
        right_response = {
            'id': TEST_FILM['id'],
            'actors': TEST_FILM['actors'],
            'description': TEST_FILM['description'],
            'director': TEST_FILM['director'],
            'genre': TEST_FILM['genre'],
            'imdb_rating': TEST_FILM['imdb_rating'],
            'title': TEST_FILM['title'],
            'writers': TEST_FILM['writers'],
        }
        response = await get_data(f'/api/v1/films/{id}')
        assert response.status == HTTPStatus.OK
        assert response.body == right_response

    async def test_getting_film_by_id_if_does_not_exist(self, get_data):

        """
        film with given id does not exist and is not expected to be returned
        """

        id = 'ef86b8ff-3c82-4d31-ad8e-7nnnnf4e3f95'

        response = await get_data(f'/api/v1/films/{id}')
        assert response.status == HTTPStatus.NOT_FOUND

    async def test_search_film(self, get_data):

        """
        Test search film by title.
        """

        title = 'zmurki'
        params = {'query': title}
        right_response = [{
            'id': TEST_FILM['id'],
            'imdb_rating': TEST_FILM['imdb_rating'],
            'title': TEST_FILM['title'],
        }]

        response = await get_data('/api/v1/films/search', params)
        assert response.status == HTTPStatus.OK
        assert response.body == right_response

    async def test_pagination(self, get_data):

        """
        Test pagination.
        """

        params = {'page_size': 4, 'page_number': 1}
        response = await get_data('/api/v1/films', params=params)
        assert response.status == HTTPStatus.OK
        assert len(response.body) == 4

    async def test_film_cached(self, get_data_from_cache, get_data):

        """
        Test caching
        """

        id = 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95'

        await get_data(f'/api/v1/films/{id}')
        data = await get_data_from_cache(f'film:{id}')
        assert data == TEST_FILM
