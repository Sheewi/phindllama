# Builder
FROM python:3.10 as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime
FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

# Health checks and graceful shutdown
HEALTHCHECK --interval=30s CMD curl -f http://localhost:8000/health || exit 1
STOPSIGNAL SIGTERM

ENV PATH=/root/.local/bin:$PATH
CMD ["gunicorn", "-b", ":8000", "-k", "uvicorn.workers.UvicornWorker", "--timeout", "120", "app.main:app"]