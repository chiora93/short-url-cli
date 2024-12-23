from unittest.mock import patch

from short_url_cli.utils import is_valid_url, shorten_url


@patch("short_url_cli.settings.SHORTENED_URL_BASE_URL", "https://myurlshortener.com/")
def test_is_valid_url_valid():
    valid_urls = [
        "https://www.google.com",
        "http://example.com",
        "https://sub.domain.co.uk/path?param=value",
    ]
    for url in valid_urls:
        assert is_valid_url(url) is True, f"URL should be valid but got invalid: {url}"


def test_is_valid_url_invalid():
    invalid_urls = [
        "",
        "   ",
        "not a url",
        "http//missingcolon.com",
        "www.missing-scheme.com",
    ]
    for url in invalid_urls:
        assert is_valid_url(url) is False, f"URL should be invalid but got valid: {url}"


@patch("short_url_cli.settings.SHORTENED_URL_BASE_URL", "https://myurlshortener.com/")
def test_shorten_url_structure():
    """
    Test that the shorten_url function returns a string that begins with 
    settings.SHORTENED_URL_BASE_URL and has some "randomness" at the end.
    """
    url = "https://www.example.com/path?q=search"
    short = shorten_url(url)
    base_url = "https://myurlshortener.com/"
    assert short.startswith(base_url), "Shortened URL must start with base URL"
    # Controlla che ci sia un minimo di lunghezza dopo il base_url
    assert len(short) > len(base_url), "Shortened URL must contain extra characters"


@patch("short_url_cli.settings.SHORTENED_URL_BASE_URL", "https://myurlshortener.com/")
def test_shorten_url_different_for_different_inputs():
    """
    This test checks (heuristically) that different URLs produce different shortened outputs.
    Nota: non è garantito che due URL diversi non producano collisioni, 
    ma ci aspettiamo che raramente accada con l’hash personalizzato.
    """
    url1 = "https://www.example1.com/"
    url2 = "https://www.example2.com/"
    short1 = shorten_url(url1)
    short2 = shorten_url(url2)
    assert short1 != short2, "Different URLs should produce different shortened results (heuristically)"
