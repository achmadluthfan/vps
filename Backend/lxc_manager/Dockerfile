FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0

CMD [ "python", "run.py" ]