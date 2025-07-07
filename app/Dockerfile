FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download ru_core_news_lg

RUN pip install --no-cache-dir awscli

RUN mkdir -p /app/data

COPY . .

RUN chmod +x run.sh

EXPOSE 8000

CMD ["bash", "run.sh"]
