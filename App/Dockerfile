FROM python:3.11

WORKDIR /App

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY . /App

CMD ["uvicorn", "diet:app", "--host", "0.0.0.0", "--port", "8000"]