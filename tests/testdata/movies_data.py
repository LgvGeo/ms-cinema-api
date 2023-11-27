import uuid

TEST_FILM = {
        'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95',
        'imdb_rating': 8.5,
        'genre': [
            {
                'id': 'fb111f22-121e-44a7-b78f-b19191810fbf',
                'name': 'Adventure'}],
        'title': 'Zmurki',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'name': 'Ann'},
            {'id': 'fb111f22-121e-44a7-b78f-b19191810fbf', 'name': 'Bob'}
        ],
        'writers': [
            {'id': 'caf76c67-c0fe-477e-8766-3ab3ff2574b5', 'name': 'Ben'},
            {'id': 'b45bd7bc-2e16-46d5-b125-983d356768c6', 'name': 'Howard'}
        ]
    }

MOVIES_DATA = [{
        'id': str(uuid.uuid4()),
        'imdb_rating': x / 100,
        'genre': [
            {
                'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95',
                "name": 'Action'}],
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'name': 'Ann'},
            {'id': 'fb111f22-121e-44a7-b78f-b19191810fbf', 'name': 'Bob'}
        ],
        'writers': [
            {'id': 'caf76c67-c0fe-477e-8766-3ab3ff2574b5', 'name': 'Ben'},
            {'id': 'b45bd7bc-2e16-46d5-b125-983d356768c6', 'name': 'Howard'}
        ]
    } for x in range(10)]
MOVIES_DATA.append(TEST_FILM)
sorted(MOVIES_DATA, key=lambda x: x['imdb_rating'], reverse=True)
