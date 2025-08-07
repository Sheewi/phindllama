# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc python3-dev && \
    apt-get autoremove -y

# Install runtime dependencies
RUN pip install gunicorn gevent

# Expose port
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

# Run command
CMD ["gunicorn", "-b", "0.0.0.0:8080", "--worker-class", "gevent", "--workers", "4", "app.main:app"]
