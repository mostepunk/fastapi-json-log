# Json logging for FastAPI
This application formats output logs to JSON It needs to Elastic stack or for OpenSearch.
There are two loggers "main" It needs for log your data, and request/response log as middleware for logging all incoming and outgoing information

## Requirements
- loguru
- fastapi
- stackprinter
- uvicorn

## Run app
`uvicorn --host=0.0.0.0 --port 8888 app.main:app --reload`

## Example answers
Two records created. \
First is from `logger.info("Got /")`
```json
{
    "thread": 459014,
    "level_name": "Information",
    "message": "Got /",
    "source_log": "main",
    "@timestamp": "2022-03-16T09:51:03+03:00",
    "app_name": "FastAPI example application",
    "app_version": "0.0.1",
    "app_env": "dev",
    "duration": 649
}
```
Another from Middleware
```json
{
    "thread": 459014,
    "level_name": "Information",
    "message": "Answer code: 200 request url: GET \"http://127.0.0.1:8888/\" duration: 2 ms ",
    "source_log": "main",
    "@timestamp": "2022-03-16T09:51:03+03:00",
    "app_name": "FastAPI example application",
    "app_version": "0.0.1",
    "app_env": "dev",
    "duration": 2,
    "request_uri": "http://127.0.0.1:8888/",
    "request_referer": "http://127.0.0.1:8888/docs",
    "request_method": "GET",
    "request_path": "/",
    "request_host": "127.0.0.1:8888",
    "request_size": 0,
    "request_content_type": "",
    "request_headers": {
        "host": "127.0.0.1:8888",
        "connection": "keep-alive",
        "sec-ch-ua": "\"Chromium\";v=\"98\", \" Not A;Brand\";v=\"99\"",
        "accept": "application/json",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.121 Safari/537.36",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "http://127.0.0.1:8888/docs",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "cookie": "_pk_id.1.dc78=4ec40eae396f1c32.1645453915.; GUID_20B40965CCF8B7300FCB1E3B5CB9925FB27970B0_8888=NcjlKqKxMJq9RgiYXEf3; io=fSKn7g-dE_J63nxDAAAA"
    },
    "request_body": "",
    "request_direction": "in",
    "response_status_code": 200,
    "response_size": 22,
    "response_headers": {
        "content-length": "22",
        "content-type": "application/json"
    },
    "response_body": "{\"answer\":\"I am Root\"}"
}
```
