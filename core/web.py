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


class HttpRequestError(Exception):
    _message: str
    _request: HttpRequest
    _response: HttpResponse

    def __init__(self, message, request: HttpRequest, response: HttpResponse):
        self._message = message
        self._request = request
        self._response = response

    def __str__(self):
        return f"{self._message}\n" \
               f"Status code: {self._response.status_code}\n" \
               f"Status message: {self._response.reason}\n" \
               f"Status text: {self._response.text}\n" \
               f"Url: {self._request.url}\n" \
               f"Method: {self._request.method}\n" \
               + f"{self._request.url_parameters}\n" if self._request.url_parameters else "" \
               + f"{self._request.body}" if self._request.body else ""


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

    def send(self) -> HttpResponse:
        request = self._build()
        request["verify"] = False
        response = requests.request(**request)
        return HttpResponse(self, response)

    def _build(self) -> Dict[str, Any]:
        request = dict()
        request["headers"] = {"Content-Type": "application/json"}
        request["method"] = self._method.value
        request["url"] = self._url
        request["params"] = self._url_parameters
        if self._body is not None:
            request["data"] = json.dumps(self._body)
        return request


class HttpResponse:
    _request: HttpRequest
    _body: Optional[Any]

    status_code: int
    reason: Optional[str]
    text: Optional[str]

    def __init__(self, request: HttpRequest, response: requests.Response):
        self._request = request
        self._body = response.json() if self._is_json_content_type(response) else None

        self.status_code = response.status_code

        is_successful_status_code = 200 <= response.status_code < 300
        self.reason = response.reason if not is_successful_status_code else None
        self.text = response.text if not is_successful_status_code else None

    @property
    def body(self):
        if not self._body:
            raise HttpRequestError("Response returned no body", self._request, self)
        return self._body

    @staticmethod
    def _is_json_content_type(response: requests.Response) -> bool:
        for key, value in response.headers.items():
            if key.lower() == "content-type" and value.lower().find("application/json") != -1:
                return True
        return False

