FROM python:3.9
WORKDIR /Eng-FastAPI
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
RUN ["uvicorn", "--host", "0.0.0.0", "main:app"]