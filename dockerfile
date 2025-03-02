# pull official base image
FROM python:3.12.8-bullseye

# Set environment variables for Python and ensure Python outputs everything
# to stdout and stderr without buffering (e.g. for Docker logs)
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install Poetry
RUN pip install poetry

# Set the working directory in the container to /app
WORKDIR /.

# Copy only the dependency files to avoid caching issues
COPY ./ ./

# Something can screw up during the development process, so rebuild lockfile
RUN poetry lock

# Install project dependencies using Poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

CMD ["poetry", "shell"]