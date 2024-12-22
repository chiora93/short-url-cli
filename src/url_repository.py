from datetime import datetime
from typing import Optional

from bson.codec_options import CodecOptions

from db import database
from dtos import ShortenedURL


class URLRepository:
    def __init__(self):
        self.database = database
        options = CodecOptions(tz_aware=True)
        self.shortened_urls_collection = self.database.get_collection("shortened_urls", options)

    def get_expanded_url_by_shortened_url(self, shortened_url: str, ) -> Optional[ShortenedURL]:
        query_result = self.shortened_urls_collection.find_one({
            "shortened_url": shortened_url
        })
        return ShortenedURL(**query_result) if query_result is not None else None

    def insert_shortened_url(self, expanded_url: str, shortened_url: str, expiration_date: datetime, ) -> ShortenedURL:
        row = {"expanded_url": expanded_url,
               "shortened_url": shortened_url,
               "expiration_date": expiration_date, }
        self.shortened_urls_collection.insert_one(row)
        return ShortenedURL(**row)
