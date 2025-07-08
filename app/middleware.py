import json
import logging

from fastapi import Request
from fastapi.responses import StreamingResponse

from starlette.concurrency import iterate_in_threadpool


logger = logging.getLogger("custom-logger")


async def log_requests_response(request: Request, call_next):
    method = request.method

    request_id = request.headers.get("X-Request-ID")

    request_body = await request.body()
    request_body = request_body.decode()

    path = request.url.path

    client_host = request.client.host
    client_port = request.client.port

    response: StreamingResponse = await call_next(request)

    response_body = [chunk async for chunk in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))

    response_body = b''.join(response_body).decode()
    response_status_code = response.status_code

    request_to_response_json = {
        "request": {
            "id": request_id,
            "body": request_body
        },
        "response": response_body
    }
    request_to_response_json = json.dumps(request_to_response_json)

    logger.info('%s:%d - "%s %s HTTP/1.1" %s - %d',
                client_host, client_port, method, path, request_to_response_json, response_status_code)

    return response