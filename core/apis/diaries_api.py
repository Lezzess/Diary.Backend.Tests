from typing import Final, Optional

from core.web import HttpRequest, HttpResponse


class DiariesApi:
    _API: Final[str] = "/diaries"

    @staticmethod
    def get_all() -> HttpResponse:
        request = HttpRequest()

        request \
            .get() \
            .with_api(DiariesApi._API)

        return request.send()

    @staticmethod
    def get(id: str) -> HttpResponse:
        request = HttpRequest()

        request \
            .get() \
            .with_api(f"{DiariesApi._API}/{id}")

        return request.send()

    @staticmethod
    def add(title: Optional[str], description: Optional[str]) -> HttpResponse:
        request = HttpRequest()

        request \
            .post() \
            .with_api(DiariesApi._API) \
            .with_body(title=title, description=description)

        return request.send()

    @staticmethod
    def update(id: str, title: Optional[str], description: Optional[str]) -> HttpResponse:
        request = HttpRequest()

        request \
            .put() \
            .with_api(f"{DiariesApi._API}/{id}") \
            .with_body(title=title, description=description)

        return request.send()

    @staticmethod
    def remove(id: str) -> HttpResponse:
        request = HttpRequest()

        request \
            .delete() \
            .with_api(f"{DiariesApi._API}/{id}") \

        return request.send()
