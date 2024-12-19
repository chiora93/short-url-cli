# short-url-cli
CLI that allows to expand a shorten URL and to shorten an URL

# Set up

## Define env file

Before starting the application you need to define a `.env` file in the root folder.

Example of `.env`:
```bash
DATABASE_HOST=database
DATABASE_USERNAME=urlshortener
DATABASE_PASSWORD=23j9fj
MONGO_INITDB_ROOT_USERNAME=urlshortener
MONGO_INITDB_ROOT_PASSWORD=23j9fj
```

## Start database

```bash
docker compose up -d database --build
```

# CLI usage

## Minify URL

To minify a URL you have to use the `minify` command of the CLI:

```bash
docker compose run --rm cli minify <URL>
```

where `<URL>` is the URL you want to minify.

Example of command and related output:
```
docker compose run --rm cli minify google.com

Minifying url google.com..
Minified url https://myurlshortener.com/43AC
```

## Expand URL

To expand a URL you need to use the `expand` CLI command:
```bash
docker compose run --rm cli expand <SHORTEN_URL>
```
where `<SHORTEN_URL>` is the minified URL you want to expand.

Example of command and related output:
```
docker compose run --rm cli expand https://myurlshortener.com/43AC

Expanding url https://myurlshortener.com/43AC ...
Expanded URL is: google.com
```