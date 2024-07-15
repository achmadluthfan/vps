FROM python:3.9-slim

WORKDIR /app

# Copy the application code
COPY . /app

# Display Python version and contents of requirements.txt for debugging
RUN python --version
RUN cat requirements.txt

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y build-essential
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 3000
EXPOSE 3000

# Set environment variables
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["python", "run.py"]