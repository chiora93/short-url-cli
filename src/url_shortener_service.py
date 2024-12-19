from datetime import UTC, datetime, timedelta

import settings
from custom_types import ErrorMessage
from url_repository import URLRepository
from utils import shorten_url, is_valid_url


class URLShortenerService:
    def __init__(self):
        self.repository = URLRepository()

    def minify_url(self, url: str) -> [str, ErrorMessage]:
        """
        Minify URL

        This method validates the incoming input to ensure is a valid URL, then calculates the shorten URL and
        finally stores it into database.
        """
        # validations
        if not url or not url.strip():
            return None, "Empty URL input"
        if not is_valid_url(url):
            return None, "Malformed URL input"

        shortened_url = shorten_url(url)
        expiration_date = datetime.now(UTC) + timedelta(seconds=settings.SHORTENED_URL_TTL_SECONDS)
        self.repository.insert_shortened_url(url, shortened_url, expiration_date)
        return shortened_url, None

    def expand_url(self, shortened_url: str):
        return self.repository.get_expanded_url_by_shortened_url(shortened_url)
