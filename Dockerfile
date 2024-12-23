FROM python:3.12

# Install poetry
RUN pip install --no-cache-dir poetry

# Set workdir
WORKDIR /app

# Copy poetry configuration
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application
COPY src .

# Set python path to recognize short_url_cli package correctly
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Set the entrypoint
ENTRYPOINT ["poetry", "run", "python", "short_url_cli/cli.py"]
