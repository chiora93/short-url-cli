from datetime import datetime

from pydantic import BaseModel


class ShortenedURL(BaseModel):
    expanded_url: str
    shortened_url: str
    expiration_date: datetime
