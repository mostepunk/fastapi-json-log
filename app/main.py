import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.middleware import LoggingMiddleware
from app.core.settings import app_settings
from app.core.logging import logger


def get_application() -> FastAPI:
    application = FastAPI(
        title=app_settings.PROJECT_NAME,
        debug=app_settings.DEBUG,
        version=app_settings.VERSION,
        docs_url="/api/docs"
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_application()
app.middleware('http')(
    LoggingMiddleware()
)


@app.get('/')
async def root():
    logger.info("Got /")
    return {"answer": "I am Root"}


@app.get('/error')
async def error(one: int, two: int):
    """ Example with traceback
    """
    logger.info(f"Got /error, {one=}, {two=}")
    return one / two

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
