FROM python:3.10-slim-buster

WORKDIR /backend

COPY . /backend

COPY templates/ /backend/templates

COPY static/ /backend/static

RUN pip install -r requirements.txt

CMD ["python3", "app.py"]