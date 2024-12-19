from datetime import datetime, UTC

from db import database


class URLRepository:
    def __init__(self):
        self.database = database

    def get_expanded_url_by_shortened_url(self, shortened_url: str):
        shortened_urls_collection = self.database["shortened_urls"]
        query_result = shortened_urls_collection.find_one({
            "shortened_url": shortened_url, "expiration_date": {
                "$gte": datetime.now(UTC)
            }
        }, {"expanded_url": 1})
        return query_result["expanded_url"] if query_result is not None else None

    def insert_shortened_url(self, expanded_url: str, shortened_url: str, expiration_date: datetime):
        shortened_urls_collection = self.database["shortened_urls"]
        row = {"expanded_url": expanded_url, "shortened_url": shortened_url, "expiration_date": expiration_date}
        x = shortened_urls_collection.insert_one(row)
        return x.inserted_id
