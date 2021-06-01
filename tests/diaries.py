from typing import Final

from core.web import HttpRequest


_API: Final[str] = "/diaries"


class TestGetAllDiaries:
    def test_WhenRequestIsValid_Returns200AndListOfDiaries(self, http):
        http\
            .get()\
            .with_api(_API)\

        response = http.send()
        response_body = response.json()

        assert response.status_code == 200
        assert type(response_body) is list

