FROM python:3.10-alpine3.21

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements /tmp/requirements
COPY ./scripts /scripts
COPY ./app /app
WORKDIR /app
EXPOSE 8000

RUN python -m venv /py
RUN /py/bin/pip install --upgrade pip

RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps
RUN apk add --update --no-cache build-base postgresql-dev gcc libc-dev linux-headers

RUN /py/bin/pip install -r /tmp/requirements/development.txt
RUN apk del .tmp-build-deps

RUN chmod -R +x /scripts

ENV PATH='/scripts:/py/bin:/bin:$PATH'

ENTRYPOINT ["entrypoint.sh"]