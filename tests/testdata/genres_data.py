import string
import uuid

TEST_GENRE = {
        'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95',
        'name': 'z',
        'description': 'New World',
    }

GENRES_DATA = [{
        'id': str(uuid.uuid4()),
        'name': x,
        'description': 'New World',
    } for x in string.ascii_lowercase[:10]]
GENRES_DATA.append(TEST_GENRE)
sorted(GENRES_DATA, key=lambda x: x['name'])
