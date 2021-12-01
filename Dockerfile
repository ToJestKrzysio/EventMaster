FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /backend/

COPY Pipfile Pipfile.lock /backend/
RUN pip install pipenv && pipenv install --system

COPY . /backend/

CMD /usr/local/bin/python -m pip install --upgrade pip \
	&& python manage.py migrate \
	&& python manage.py runserver 0.0.0.0:8000
