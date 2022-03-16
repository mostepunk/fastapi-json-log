from typing import Union, List, Optional
from pydantic import BaseModel, Field, validator


class BaseJsonLogSchema(BaseModel):
    """
    Main log in JSON format
    """
    thread: Union[int, str]
    level_name: str
    message: str
    source_log: str
    timestamp: str = Field(..., alias='@timestamp')
    app_name: str
    app_version: str
    app_env: str
    duration: int
    exceptions: Union[List[str], str] = None
    trace_id: str = None
    span_id: str = None
    parent_id: str = None

    class Config:
        allow_population_by_field_name = True


class RequestJsonLogSchema(BaseModel):
    """
    Schema for request/response answer
    """
    request_uri: str
    request_referer: str
    request_method: str
    request_path: str
    request_host: str
    request_size: int
    request_content_type: str
    request_headers: dict
    request_body: Optional[str]
    request_direction: str
    response_status_code: int
    response_size: int
    response_headers: dict
    response_body: Optional[str]
    duration: int

    @validator(
        'request_body',
        'response_body',
        pre=True,
    )
    def valid_body(cls, field):
        if isinstance(field, bytes):
            try:
                field = field.decode()
            except UnicodeDecodeError:
                field = b'file_bytes'
            return field

        if isinstance(field, str):
            return field
