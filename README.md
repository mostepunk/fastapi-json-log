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
