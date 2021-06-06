import uuid
from typing import Final

import pytest

from core.apis.diaries_api import DiariesApi


@pytest.fixture(scope="module")
def diaries_api():
    return DiariesApi()


_API: Final[str] = "/diaries"


class TestGetAllDiaries:
    def test_WhenDiaryExists_Returns200AndListContainingExistingDiary(self, diaries_api):
        title = "Diary title"
        description = "Diary description"

        add_diary_response = diaries_api.add(title, description)
        existing_diary = add_diary_response.body
        get_all_diaries_response = diaries_api.get_all()
        diaries = get_all_diaries_response.body

        assert get_all_diaries_response.status_code == 200
        assert any(diary["id"] == existing_diary["id"] for diary in diaries)


class TestGetDiary:
    def test_WhenDiaryExists_Returns200AndExistingDiary(self, diaries_api):
        title = "Diary title"
        description = "Diary description"

        add_diary_response = diaries_api.add(title, description)
        existing_diary = add_diary_response.body
        get_diary_response = diaries_api.get(existing_diary["id"])
        diary = get_diary_response.body

        assert get_diary_response.status_code == 200
        assert diary["id"] == existing_diary["id"]

    def test_WhenDiaryNotExists_Returns404(self, diaries_api):
        id = str(uuid.uuid4())

        diaries_api.remove(id)
        get_diary_response = diaries_api.get(id)

        assert get_diary_response.status_code == 404

    def test_WhenInvalidIdIsPassed_Returns400(self, diaries_api):
        id = "invalid-guid"

        get_diary_response = diaries_api.get(id)

        assert get_diary_response.status_code == 400


class TestAddDiary:
    def test_WhenRequestIsValid_Returns201AndAddedDiary(self, diaries_api):
        title = "Diary title"
        description = "Diary description"

        add_diary_response = diaries_api.add(title, description)
        diary = add_diary_response.body

        assert add_diary_response.status_code == 201
        assert diary["id"] is not None and not ""
        assert diary["title"] == title
        assert diary["description"] == description

    def test_WhenTitleIsEmpty_Returns400(self, diaries_api):
        title = ""
        description = "Diary description"

        add_diary_response = diaries_api.add(title, description)

        assert add_diary_response.status_code == 400

    def test_WhenDescriptionIsEmpty_Returns400(self, diaries_api):
        title = "Diary title"
        description = ""

        add_diary_response = diaries_api.add(title, description)

        assert add_diary_response.status_code == 400

    def test_WhenTitleIsLongerThan300Characters_Returns400(self, diaries_api):
        title = "t" * 301
        description = "Diary description"

        add_diary_response = diaries_api.add(title, description)

        assert add_diary_response.status_code == 400


class TestUpdateDiary:
    def test_WhenDiaryExistsAndValidDataIsPassed_Returns200AndUpdatesDiary(self, diaries_api):
        title = "Diary title"
        description = "Diary description"
        updated_title = "New diary title"
        updated_description = "New diary description"

        add_diary_response = diaries_api.add(title, description)
        added_diary = add_diary_response.body
        update_diary_response = diaries_api.update(added_diary["id"], updated_title, updated_description)
        updated_diary = update_diary_response.body

        assert update_diary_response.status_code == 200
        assert updated_diary["title"] == updated_title
        assert updated_diary["description"] == updated_description

    def test_WhenDiaryNotExists_Returns404(self, diaries_api):
        id = str(uuid.uuid4())
        title = "New diary title"
        description = "New diary description"

        diaries_api.remove(id)
        update_diary_response = diaries_api.update(id, title, description)

        assert update_diary_response.status_code == 404

    def test_WhenInvalidIdIsPassed_Returns400(self, diaries_api):
        id = "invalid-guid"
        title = "New diary title"
        description = "New diary description"

        update_diary_response = diaries_api.update(id, title, description)

        assert update_diary_response.status_code == 400

    def test_WhenTitleIsEmpty_Returns400(self, diaries_api):
        title = "Diary title"
        description = "Diary description"
        updated_title = ""
        updated_description = "New diary description"

        add_diary_response = diaries_api.add(title, description)
        added_diary = add_diary_response.body
        update_diary_response = diaries_api.update(added_diary["id"], updated_title, updated_description)

        assert update_diary_response.status_code == 400

    def test_WhenDescriptionIsEmpty_Returns400(self, diaries_api):
        title = "Diary title"
        description = "Diary description"
        updated_title = "New diary title"
        updated_description = ""

        add_diary_response = diaries_api.add(title, description)
        added_diary = add_diary_response.body
        update_diary_response = diaries_api.update(added_diary["id"], updated_title, updated_description)

        assert update_diary_response.status_code == 400

    def test_WhenTitleIsLongerThan300Characters_Returns400(self, diaries_api):
        title = "Diary title"
        description = "Diary description"
        updated_title = "t" * 301
        updated_description = "New diary description"

        add_diary_response = diaries_api.add(title, description)
        added_diary = add_diary_response.body
        update_diary_response = diaries_api.update(added_diary["id"], updated_title, updated_description)

        assert update_diary_response.status_code == 400


class TestRemoveDiary:
    def test_WhenDiaryExists_Returns200AndRemovesDiary(self, diaries_api):
        title = "Diary title"
        description = "Diary description"

        add_diary_response = diaries_api.add(title, description)
        added_diary = add_diary_response.body
        remove_diary_response = diaries_api.remove(added_diary["id"])
        get_diary_response = diaries_api.get(added_diary["id"])

        assert remove_diary_response.status_code == 200
        assert get_diary_response.status_code == 404

    def test_WhenInvalidIdIsPassed_Returns400(self, diaries_api):
        id = "invalid-guid"

        remove_diary_response = diaries_api.remove(id)

        assert remove_diary_response.status_code == 400

    def test_WhenDiaryNotExists_Returns404(self, diaries_api):
        id = str(uuid.uuid4())

        diaries_api.remove(id)
        remove_diary_response = diaries_api.remove(id)

        assert remove_diary_response.status_code == 404
