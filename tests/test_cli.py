from unittest.mock import patch

from short_url_cli.cli import app
from typer.testing import CliRunner

runner = CliRunner()


@patch("short_url_cli.cli.URLShortenerService")
def test_minify_command_ok(service_mock):
    """
    Test that the minify command prints the expected output when everything goes fine.
    """
    # Configure mock to return (shortened_url, None) without errors
    instance = service_mock.return_value
    instance.minify_url.return_value = ("https://myurlshortener.com/abcd", None)

    result = runner.invoke(app, ["minify", "https://www.example.com/path?q=search"])
    assert result.exit_code == 0
    assert "Minified url https://myurlshortener.com/abcd" in result.stdout


@patch("short_url_cli.cli.URLShortenerService")
def test_minify_command_error(service_mock):
    """
    Test that the minify command prints an error when the service returns an error.
    """
    instance = service_mock.return_value
    instance.minify_url.return_value = (None, "Malformed URL input")

    result = runner.invoke(app, ["minify", "invalid_url"])
    assert result.exit_code == 0
    assert "Something went wrong: Malformed URL input" in result.stdout


@patch("short_url_cli.cli.URLShortenerService")
def test_expand_command_ok(service_mock):
    """
    Test that the expand command prints the expected output when everything goes fine.
    """
    instance = service_mock.return_value
    instance.expand_url.return_value = ("https://www.example.com/path?q=search", None)

    result = runner.invoke(app, ["expand", "https://myurlshortener.com/abcd"])
    assert result.exit_code == 0
    assert "Expanded URL is: https://www.example.com/path?q=search" in result.stdout


@patch("short_url_cli.cli.URLShortenerService")
def test_expand_command_error(service_mock):
    """
    Test that the expand command prints an error message when the service returns an error.
    """
    instance = service_mock.return_value
    instance.expand_url.return_value = (None, "Expired URL")

    result = runner.invoke(app, ["expand", "https://myurlshortener.com/abcd"])
    assert result.exit_code == 0
    assert "Can't expand URL: Expired URL" in result.stdout
