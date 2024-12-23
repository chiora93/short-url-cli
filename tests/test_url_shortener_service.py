from datetime import datetime, UTC, timedelta
from unittest.mock import MagicMock, patch

from short_url_cli.url_shortener_service import URLShortenerService


@patch("short_url_cli.settings.SHORTENED_URL_TTL_SECONDS", 60)  # Supponiamo 60 secondi di TTL
@patch("short_url_cli.url_shortener_service.URLRepository")
def test_minify_url_empty_input(repo_mock):
    service = URLShortenerService()
    shortened_url, error = service.minify_url("")
    assert shortened_url is None
    assert error == "Empty URL input"


@patch("short_url_cli.settings.SHORTENED_URL_TTL_SECONDS", 60)
@patch("short_url_cli.url_shortener_service.URLRepository")
def test_minify_url_invalid_url(repo_mock):
    service = URLShortenerService()
    shortened_url, error = service.minify_url("not-a-valid-url")
    assert shortened_url is None
    assert error == "Malformed URL input"


@patch("short_url_cli.settings.SHORTENED_URL_TTL_SECONDS", 60)
@patch("short_url_cli.url_shortener_service.URLRepository")
def test_minify_url_already_exists_not_expired(repo_mock):
    """
    If an existing record is found and it's not expired,
    we expect an error stating that it already exists (come da codice).
    """
    mock_record = MagicMock()
    mock_record.expiration_date = datetime.now(UTC) + timedelta(seconds=30)  # not expired
    repo_instance = repo_mock.return_value
    repo_instance.get_by_expanded_url.return_value = mock_record

    service = URLShortenerService()
    shortened_url, error = service.minify_url("https://www.example.com")
    assert shortened_url is None
    assert error == "Shortened URL already exists"


@patch("short_url_cli.settings.SHORTENED_URL_TTL_SECONDS", 60)
@patch("short_url_cli.url_shortener_service.URLRepository")
@patch("short_url_cli.url_shortener_service.shorten_url", return_value="https://myurlshortener.com/abcd123")
def test_minify_url_ok(mock_shorten_url, repo_mock):
    """
    Normal flow: the URL is valid, doesn't exist in DB or is expired, so we create a new shortened.
    """
    repo_instance = repo_mock.return_value
    repo_instance.get_by_expanded_url.return_value = None

    service = URLShortenerService()
    shortened_url, error = service.minify_url("https://www.example.com")
    assert shortened_url == "https://myurlshortener.com/abcd123"
    assert error is None
    # Verifichiamo che insert sia stato chiamato
    repo_instance.insert.assert_called_once()


@patch("short_url_cli.url_shortener_service.URLRepository")
def test_expand_url_not_found(repo_mock):
    repo_instance = repo_mock.return_value
    repo_instance.get_by_shortened_url.return_value = None

    service = URLShortenerService()
    expanded_url, error = service.expand_url("https://myurlshortener.com/xxxx")
    assert expanded_url is None
    assert error == "Shortened URL doesn't exist"


@patch("short_url_cli.url_shortener_service.URLRepository")
def test_expand_url_expired(repo_mock):
    mock_record = MagicMock()
    mock_record.expiration_date = datetime.now(UTC) - timedelta(seconds=30)  # expired
    mock_record.expanded_url = "https://www.example.com"
    repo_instance = repo_mock.return_value
    repo_instance.get_by_shortened_url.return_value = mock_record

    service = URLShortenerService()
    expanded_url, error = service.expand_url("https://myurlshortener.com/xxxx")
    assert expanded_url is None
    assert error == "Expired URL"


@patch("short_url_cli.url_shortener_service.URLRepository")
def test_expand_url_ok(repo_mock):
    mock_record = MagicMock()
    mock_record.expiration_date = datetime.now(UTC) + timedelta(seconds=30)  # not expired
    mock_record.expanded_url = "https://www.example.com"
    repo_instance = repo_mock.return_value
    repo_instance.get_by_shortened_url.return_value = mock_record

    service = URLShortenerService()
    expanded_url, error = service.expand_url("https://myurlshortener.com/xxxx")
    assert expanded_url == "https://www.example.com"
    assert error is None
