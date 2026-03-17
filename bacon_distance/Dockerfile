FROM python:3.14 AS backend

COPY . .

RUN pip install .
RUN python ./bacon_distance/db_generate.py

CMD ["fastapi", "run", "./main.py", "--port", "80"]