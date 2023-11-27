import uuid

TEST_PERSON = {
  "id": "2d6f6284-13ce-4d25-9453-c4335432c116",
  "name": "Adam Driver",
  "films": [
    {
      "id": "12a8279d-d851-4eb9-9d64-d690455277cc",
      "title": "Star Wars: Episode VIII - The Last Jedi",
      "roles": [
        "actor"
      ]
    },
    {
      "id": "1d42ceae-9397-475c-9517-e94dda7bc2a1",
      "title": "Star Wars: Episode VII - The Force",
      "roles": [
        "actor"
      ]
    }
  ]
}
PERSONS_DATA = [{
  "id": str(uuid.uuid4()),
  "name": "Tom Driver",
  "films": [
    {
      "id": "12a8279d-d851-4eb9-9d64-d690455277cc",
      "title": "Star Wars: Episode VIII - The Last Jedi",
      "roles": [
        "actor"
      ]
    },
    {
      "id": "1d42ceae-9397-475c-9517-e94dda7bc2a1",
      "title": "Star Wars: Episode VII - The Force",
      "roles": [
        "actor"
      ]
    }
  ]
} for _ in range(10)]
PERSONS_DATA.append(TEST_PERSON)
