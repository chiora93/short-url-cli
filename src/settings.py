""" Module that contains all project settings """
import os
from urllib.parse import quote_plus

# Database settings

# See https://pymongo.readthedocs.io/en/stable/examples/authentication.html#percent-escaping-username-and-password
DATABASE_USERNAME = quote_plus(os.environ.get("DATABASE_USERNAME"))
DATABASE_PASSWORD = quote_plus(os.environ.get("DATABASE_PASSWORD"))
DATABASE_HOST = os.environ.get("DATABASE_HOST", "localhost")
DATABASE_PORT = os.environ.get("DATABASE_PORT", "27017")
DATABASE_URL = os.environ.get("DATABASE_URL", f"mongodb://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/")
DATABASE_NAME = "url_shortener"

# Application settings
SHORTENED_URL_TTL_SECONDS = 30  # Num of seconds for which a shortened URL should remain valid to be expanded
SHORTENED_URL_BASE_URL = "https://myurlshortener.com/"