from __future__ import annotations

import json
from enum import Enum
from typing import Dict, Any, Optional, Final

import requests


_URL: Final[str] = "https://localhost:44369"


class HttpMethod(str, Enum):
    GET = "GET",
    POST = "POST",
    PUT = "PUT",
    DELETE = "DELETE"


class HttpRequest:
    _method: Optional[HttpMethod]
    _url: Optional[str]
    _url_parameters: Optional[Dict[str, Any]]
    _body: Optional[Dict[str, Any]]

    def __init__(self):
        self._method = None
        self._url = None
        self._url_parameters = None
        self._body = None

    @property
    def method(self) -> Optional[HttpMethod]:
        return self._method

    @property
    def url(self) -> Optional[str]:
        return self._url

    @property
    def url_parameters(self) -> Optional[Dict[str, Any]]:
        return self._url_parameters

    @property
    def body(self) -> Optional[Dict[str, Any]]:
        return self._body

    def get(self) -> HttpRequest:
        self._method = HttpMethod.GET
        return self

    def post(self) -> HttpRequest:
        self._method = HttpMethod.POST
        return self

    def put(self) -> HttpRequest:
        self._method = HttpMethod.PUT
        return self

    def delete(self) -> HttpRequest:
        self._method = HttpMethod.DELETE
        return self

    def with_api(self, api: str) -> HttpRequest:
        self._url = f"{_URL}{api}"
        return self

    def with_url_parameters(self, **parameters) -> HttpRequest:
        self._url_parameters = parameters
        return self

    def with_body(self, **body_parameters) -> HttpRequest:
        self._body = body_parameters
        return self

    def send(self) -> requests.Response:
        request = self._build()
        request["verify"] = False
        response = requests.request(**request)
        return response

    def _build(self) -> Dict[str, Any]:
        request = dict()
        request["method"] = self._method.value
        request["url"] = self._url
        request["params"] = self._url_parameters
        if self._body is not None:
            request["data"] = json.dumps(self._body)
        return request
