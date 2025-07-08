FROM python:3.10-slim

WORKDIR /frontend

COPY requirements.txt /frontend

RUN pip install -r requirements.txt

COPY . /frontend

EXPOSE 8001

CMD ["bash", "run.sh"]