FROM python:3.10-slim-buster

WORKDIR /backend

# Install build tools if needed
#RUN apt-get update && apt-get install -y build-essential

# Copy everything
COPY . /backend

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["gunicorn", "-w", "4", "-k", "gevent", "-b", "0.0.0.0:8080", "app:app"]
