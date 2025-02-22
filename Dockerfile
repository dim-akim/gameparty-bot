FROM python:3.12.7-slim AS builder

WORKDIR /app
ENV VIRTUAL_ENV=/app/.venv
COPY requirements.txt requirements.txt
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --no-cache-dir -U -r requirements.txt

FROM python:3.12.7-slim

WORKDIR /app
COPY --from=builder /app .
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH=/app
COPY bot bot

CMD ["python", "bot"]
