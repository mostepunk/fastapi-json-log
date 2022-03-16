import time
import math
import json
import http
import logging
import dataclasses
from typing import ClassVar

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import RequestResponseEndpoint
from starlette.types import ASGIApp, Message, Receive

from app.schemas.json_logs import RequestJsonLogSchema
from app.core.logging import logger

EMPTY_VALUE = ''
PORT = '8000'
PASS_ROUTES = [
    '/openapi.json',
    '/docs',
    '/api/v1/healthcheck',
]


@dataclasses.dataclass
class ReceiveProxy:
    """Proxy to starlette.types.Receive.__call__ with caching first receive call.
       https://github.com/tiangolo/fastapi/issues/394#issuecomment-994665859
    """

    receive: Receive
    cached_body: bytes
    _is_first_call: ClassVar[bool] = True

    async def __call__(self):
        # First call will be for getting request body => returns cached result
        if self._is_first_call:
            self._is_first_call = False
            return {
                "type": "http.request",
                "body": self.cached_body,
                "more_body": False
            }

        return await self.receive()


class LoggingMiddleware:
    """ Middleware that saves logs to JSON
        The main problem is
        After getting request_body
            body = await request.body()
        Body is removed from requests. I found solution as ReceiveProxy
    """
    @staticmethod
    async def get_protocol(request: Request) -> str:
        protocol = str(request.scope.get('type', ''))
        http_version = str(request.scope.get('http_version', ''))
        if protocol.lower() == 'http' and http_version:
            return f'{protocol.upper()}/{http_version}'
        return EMPTY_VALUE

    async def get_request_body(self, request: Request) -> bytes:
        body = await request.body()

        request._receive = ReceiveProxy(
            receive=request.receive, cached_body=body
        )
        return body

    async def __call__(
            self,
            request: Request,
            call_next: RequestResponseEndpoint,
            *args,
            **kwargs
    ):
        # logger.debug(f"Started Middleware: {__name__}")
        start_time = time.time()
        exception_object = None
        request_body = await self.get_request_body(request)
        server: tuple = request.get('server', ('localhost', PORT))
        request_headers: dict = dict(request.headers.items())

        # Response Side
        try:
            response = await call_next(request)
        except Exception as ex:
            logging.error(f"Exception: {ex}")
            response_body = bytes(
                http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase.encode()
            )
            response = Response(
                content=response_body,
                status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR.real,
            )
            exception_object = ex
            response_headers = {}
        else:
            response_headers = dict(response.headers.items())
            response_body = b''

            async for chunk in response.body_iterator:
                response_body += chunk

            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )

        # pass /openapi.json /docs
        if request.url.path in PASS_ROUTES:
            return response

        duration: int = math.ceil((time.time() - start_time) * 1000)

        # Initializing of json fields
        request_json_fields = RequestJsonLogSchema(
            # Request side
            request_uri=str(request.url),
            request_referer=request_headers.get('referer', EMPTY_VALUE),
            request_method=request.method,
            request_path=request.url.path,
            request_host=f'{server[0]}:{server[1]}',
            request_size=int(request_headers.get('content-length', 0)),
            request_content_type=request_headers.get(
                'content-type', EMPTY_VALUE),
            request_headers=request_headers,
            request_body=request_body,
            request_direction='in',

            # Response side
            response_status_code=response.status_code,
            response_size=int(response_headers.get('content-length', 0)),
            response_headers=response_headers,
            response_body=response_body,

            duration=duration
        ).dict()

        message = (
                f'{"Error" if exception_object else "Answer"} '
                f'code: {response.status_code} '
                f'request url: {request.method} \"{str(request.url)}\" '
                f'duration: {duration} ms '
      )
        logger.info(
            message,
            extra={
                'request_json_fields': request_json_fields,
                'to_mask': True,
            },
            exc_info=exception_object,
        )
        return response

