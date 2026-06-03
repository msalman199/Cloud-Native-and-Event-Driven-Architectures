# TODO: Choose appropriate Python base image (version 3.9-slim recommended)
FROM python:3.9-slim

# TODO: Set working directory to /app
WORKDIR /app

# TODO: Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# TODO: Copy application code
COPY app.py .

# TODO: Expose the Flask port (5000)
EXPOSE 5000

# TODO: Set the command to run the application
CMD ["python", "app.py"]
