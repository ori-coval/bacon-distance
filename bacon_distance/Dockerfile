FROM python:3.14 AS backend

COPY . .

RUN pip install .

CMD ["sh", "-c", "python -m bacon_distance.db_generate && fastapi run ./main.py --port 80"]