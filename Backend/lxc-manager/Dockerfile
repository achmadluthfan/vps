FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y build-essential
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

EXPOSE 3000

# Run the application
CMD ["python", "run.py"]