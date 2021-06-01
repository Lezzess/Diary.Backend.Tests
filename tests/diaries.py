from typing import Final

from core.web import HttpRequest


_API: Final[str] = "/diaries"


class TestGetAllDiaries:
    def test_WhenRequestIsValid_Returns200AndListOfDiaries(self, http):
        http.get()\
            .with_api(_API)\

        response = http.send()
        diaries = response.json()

        assert response.status_code == 200
        assert type(diaries) is list


class TestAddDiary:
    def test_WhenRequestIsValid_Returns201AndAddedDiary(self, http):
        title = "Diary title"
        description = "Diary description"
        http.post()\
            .with_api(_API)\
            .with_body(title=title, description=description)

        response = http.send()
        diary = response.json()

        assert response.status_code == 201
        assert diary["id"] is not None and not ""
        assert diary["title"] == title
        assert diary["description"] == description

    def test_WhenTitleIsEmpty_Returns400(self, http):
        title = ""
        description = "Diary description"
        http.post() \
            .with_api(_API) \
            .with_body(title=title, description=description)

        response = http.send()

        assert response.status_code == 400

    def test_WhenDescriptionIsEmpty_Returns400(self, http):
        title = "Diary title"
        description = ""
        http.post() \
            .with_api(_API) \
            .with_body(title=title, description=description)

        response = http.send()

        assert response.status_code == 400

    def test_WhenTitleIsLongerThan300Characters_Returns400(self, http):
        title = "t" * 301
        description = "Diary description"
        http.post() \
            .with_api(_API) \
            .with_body(title=title, description=description)

        response = http.send()

        assert response.status_code == 400
