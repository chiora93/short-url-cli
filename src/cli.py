import typer

from url_shortener_service import URLShortenerService

app = typer.Typer()


@app.command()
def minify(url: str):
    typer.echo(f"Minifying url {url} ...")
    minified_url, error_message = URLShortenerService().minify_url(url)
    if error_message:
        typer.echo(f"Something went wrong: {error_message}")
        return
    typer.echo(f"Minified url {minified_url}")


@app.command()
def expand(url: str):
    typer.echo(f"Expanding url {url} ...")
    expanded_url = URLShortenerService().expand_url(url)
    typer.echo(f"Expanded URL is: {expanded_url}")


if __name__ == "__main__":
    app()
