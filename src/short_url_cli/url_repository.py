from datetime import datetime
from typing import Optional

from bson.codec_options import CodecOptions

from short_url_cli.db import database
from short_url_cli.dtos import ShortenedURL


class URLRepository:
    def __init__(self, database_instance = None):
        self.database = database_instance or database
        options = CodecOptions(tz_aware=True)
        self.shortened_urls_collection = self.database.get_collection("shortened_urls", options)

    def get_by_expanded_url(self, expanded_url: str, ) -> Optional[ShortenedURL]:
        query_result = self.shortened_urls_collection.find_one({
            "expanded_url": expanded_url
        })
        return ShortenedURL(**query_result) if query_result is not None else None

    def get_by_shortened_url(self, shortened_url: str, ) -> Optional[ShortenedURL]:
        query_result = self.shortened_urls_collection.find_one({
            "shortened_url": shortened_url
        })
        return ShortenedURL(**query_result) if query_result is not None else None

    def insert(self, expanded_url: str, shortened_url: str, expiration_date: datetime, ) -> ShortenedURL:
        row = {"expanded_url": expanded_url,
               "shortened_url": shortened_url,
               "expiration_date": expiration_date, }
        self.shortened_urls_collection.update_one({
            "expanded_url": expanded_url,
        }, {"$set": row}, upsert=True)
        return ShortenedURL(**row)
