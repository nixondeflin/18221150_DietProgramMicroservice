FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY diet.py .
COPY diet.json .
COPY userfile.json .

EXPOSE 8000

CMD ["uvicorn", "diet:app", "--host", "0.0.0.0", "--port", "8000"]
