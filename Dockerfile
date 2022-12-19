FROM python:3.10-slim-buster

LABEL maintainer="Florian Salfenmoser <florian.salfenmoser.dev@outlook.de>"
LABEL build-date=$BUILD_DATE

# Install DE language
RUN apt-get update && apt-get install -y locales unixodbc unixodbc-dev libxml2 curl && \
	sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && locale-gen \
	&& apt-get clean

# set timezone
ENV TZ Europe/Berlin

# Set DE language
ENV LANG de_DE.UTF-8
ENV LANGUAGE de_DE.UTF-8
ENV LC_ALL de_DE.UTF-8

   # python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.3.0 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    POETRY_VIRTUALENVS_PATH="/app/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$POETRY_VIRTUALENVS_PATH/bin:$PATH"

# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry --version
RUN poetry config virtualenvs.path ${POETRY_VIRTUALENVS_PATH}
# RUN poetry config repositories.internal https://<URL>
RUN poetry config --list

# Create the app dir
RUN mkdir -p /app/app
RUN mkdir -p ${POETRY_VIRTUALENVS_PATH}
#RUN find /app -type d -exec chmod 755 {} \;
#RUN find /app -type f -exec chmod 644 {} \;
#RUN find ${POETRY_VIRTUALENVS_PATH} -type d -exec chmod 755 {} \;
#RUN find ${POETRY_VIRTUALENVS_PATH} -type f -exec chmod 644 {} \;
WORKDIR /app/

# Create the tmp directorys for file processing
RUN mkdir -p /app/tmp/in
RUN mkdir -p /app/tmp/out

# Certificates
# Add Git certs
# ADD certs/this.is.a.crt /usr/local/share/ca-certificates
# RUN update-ca-certificates

# Set the pythonpath and path that python can find the custom modules in the app-folder for import
ENV PATH=$PATH:/app/app
ENV PYTHONPATH=/app/app
# write stdout log messages immediatelly without buffering
ENV PYTHONUNBUFFERED=1
ENV IS_LOCAL=False
# start the webserver https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
# IMPORTANT: Specify 0.0.0.0 not 127.0.0.1 for localhost. The service wont listen to 127.0.0.1 per default.
# Webservice config variables:
ENV GUNICORN_CONF=/gunicorn_conf.py
ENV MODULE_NAME=app.main
ENV VARIABLE_NAME=app
ENV TIMEOUT=120
ENV GRACEFUL_TIMEOUT=120
ENV KEEPALIVE=15
ENV MAX_REQUESTS=0
ENV WEB_CONCURRENCY=1
ENV HOST=0.0.0.0
ENV PORT=8080
ENV LOG_LEVEL=error

# Copy the conda environment infos (the "app"-Folder already exists, use this one to include everythin you need!)
COPY ./poetry.lock poetry.lock
COPY ./pyproject.toml pyproject.toml
# Install the python packages
WORKDIR app/
ENV POETRY_ENV=fastapi-template
RUN poetry install --without dev

# Copy application contents to the container
COPY ./app /app/app
COPY version.txt /app/version.txt
# Set the pythonpath and path that python can find the custom modules in the app-folder for import
ENV PATH=$PATH:/app/app
ENV PYTHONPATH=/app/app
# Environment variables for this docker container (provide defaults or comment out)
# If other global env-variables are needed, set them here.
# Environment dependen variables should be set in the helm/%env%_values.yml files
ENV IS_LOCAL=False
# FastAPI Docker settings:
ENV WEB_CONCURRENCY=1
# Expose the port to the outside to make the API available outside the docker container
EXPOSE $PORT

# https://stackoverflow.com/questions/53763029/gunicorn-not-found-when-running-a-docker-container-with-venv
WORKDIR /app
RUN whoami
#RUN ls -la
CMD /.venv/activate
RUN poetry env info

CMD [ "gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "--config", "/app/app/gunicorn_conf.py", "main:app"]
# Start Gunicorn
#CMD gunicorn -k "$WORKER_CLASS" -c "$GUNICORN_CONF" "$APP_MODULE"