import typer

from url_shortener_service import URLShortenerService

app = typer.Typer()


@app.command(no_args_is_help=True)
def minify(url: str):
    """
    Minify a URL.
    """
    typer.echo(f"Minifying url {url} ...")
    minified_url, error_message = URLShortenerService().minify_url(url)
    if error_message:
        typer.echo(f"Something went wrong: {error_message}")
        return
    typer.echo(f"Minified url {minified_url}")


@app.command(no_args_is_help=True)
def expand(shortened_url: str):
    """
    Expand a URL given the shortened version.

    Can return an error in case of non-existing URL or if the shortened URL is expired.
    """
    typer.echo(f"Expanding url {shortened_url} ...")
    expanded_url, error_message = URLShortenerService().expand_url(shortened_url)
    if error_message:
        typer.echo(f"Can't expand URL: {error_message}")
        return
    typer.echo(f"Expanded URL is: {expanded_url}")


if __name__ == "__main__":
    app()
