FROM python:3.10-slim

WORKDIR /server

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download ru_core_news_lg

COPY . .

EXPOSE 8000
CMD ["bash", "run.sh"]