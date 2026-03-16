FROM python:3.14 AS frontend

COPY . .

RUN pip install .


CMD ["fastapi", "run", "./main.py", "--port", "80"]