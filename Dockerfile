FROM python:3.9-slim

WORKDIR /app

COPY diet.py .
COPY diet.json .

RUN pip install fastapi uvicorn

EXPOSE 8000

CMD ["uvicorn", "diet:app", "--host", "0.0.0.0", "--port", "8000"]