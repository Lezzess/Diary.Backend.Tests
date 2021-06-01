from typing import Final

import pytest

from core.apis.diaries_api import DiariesApi


@pytest.fixture(scope="module")
def diaries_api():
    return DiariesApi()


_API: Final[str] = "/diaries"


class TestGetAllDiaries:
    def test_WhenRequestIsValid_Returns200AndListOfDiaries(self, diaries_api):
        response = diaries_api.get_all()
        diaries = response.body

        assert response.status_code == 200
        assert type(diaries) is list


class TestGetDiary:
    def test_WhenIdOfExistingDiaryIsSpecified_Returns200AndDiaryWithSpecifiedId(self, diaries_api):
        pass


class TestAddDiary:
    def test_WhenRequestIsValid_Returns201AndAddedDiary(self, diaries_api):
        title = "Diary title"
        description = "Diary description"

        response = diaries_api.add(title, description)
        diary = response.body

        assert response.status_code == 201
        assert diary["id"] is not None and not ""
        assert diary["title"] == title
        assert diary["description"] == description

    def test_WhenTitleIsEmpty_Returns400(self, diaries_api):
        title = ""
        description = "Diary description"

        response = diaries_api.add(title, description)

        assert response.status_code == 400

    def test_WhenDescriptionIsEmpty_Returns400(self, diaries_api):
        title = "Diary title"
        description = ""

        response = diaries_api.add(title, description)

        assert response.status_code == 400

    def test_WhenTitleIsLongerThan300Characters_Returns400(self, diaries_api):
        title = "t" * 301
        description = "Diary description"

        response = diaries_api.add(title, description)

        assert response.status_code == 400
