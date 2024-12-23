from datetime import datetime
from unittest.mock import MagicMock

from short_url_cli.dtos import ShortenedURL
from short_url_cli.url_repository import URLRepository


def test_get_by_expanded_url_found():
    # Mock db
    db_mock = MagicMock()
    collection_mock = MagicMock()
    db_mock.get_collection.return_value = collection_mock

    fake_doc = {
        "expanded_url": "https://www.example.com",
        "shortened_url": "https://myurlshortener.com/abcd",
        "expiration_date": datetime(2024, 1, 1),
    }
    collection_mock.find_one.return_value = fake_doc

    repo = URLRepository(db_mock)
    result = repo.get_by_expanded_url("https://www.example.com")

    assert isinstance(result, ShortenedURL)
    assert result.expanded_url == fake_doc["expanded_url"]
    assert result.shortened_url == fake_doc["shortened_url"]
    assert result.expiration_date == fake_doc["expiration_date"]


def test_get_by_expanded_url_not_found():
    db_mock = MagicMock()
    collection_mock = MagicMock()
    db_mock.get_collection.return_value = collection_mock
    collection_mock.find_one.return_value = None

    repo = URLRepository(db_mock)
    result = repo.get_by_expanded_url("https://www.unknown.com")
    assert result is None


def test_get_by_shortened_url_found():
    db_mock = MagicMock()
    collection_mock = MagicMock()
    db_mock.get_collection.return_value = collection_mock

    fake_doc = {
        "expanded_url": "https://www.example.com",
        "shortened_url": "https://myurlshortener.com/abcd",
        "expiration_date": datetime(2024, 1, 1),
    }
    collection_mock.find_one.return_value = fake_doc

    repo = URLRepository(db_mock)
    result = repo.get_by_shortened_url("https://myurlshortener.com/abcd")
    assert isinstance(result, ShortenedURL)
    assert result.shortened_url == fake_doc["shortened_url"]


def test_get_by_shortened_url_not_found():
    db_mock = MagicMock()
    collection_mock = MagicMock()
    db_mock.get_collection.return_value = collection_mock
    collection_mock.find_one.return_value = None

    repo = URLRepository(db_mock)
    result = repo.get_by_shortened_url("https://myurlshortener.com/unknown")
    assert result is None


def test_insert():
    db_mock = MagicMock()
    collection_mock = MagicMock()
    db_mock.get_collection.return_value = collection_mock

    repo = URLRepository(db_mock)

    expanded_url = "https://www.example.com"
    shortened_url = "https://myurlshortener.com/abcd"
    expiration_date = datetime(2025, 1, 1)

    saved_record = repo.insert(expanded_url, shortened_url, expiration_date)
    # Check that update_one was called with upsert=True
    collection_mock.update_one.assert_called_with(
        {"expanded_url": expanded_url},
        {"$set": {
            "expanded_url": expanded_url,
            "shortened_url": shortened_url,
            "expiration_date": expiration_date
        }},
        upsert=True
    )
    assert saved_record.expanded_url == expanded_url
    assert saved_record.shortened_url == shortened_url
    assert saved_record.expiration_date == expiration_date
