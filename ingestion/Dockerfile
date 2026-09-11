# --- base: shared runtime (system deps, runtime packages, app code) ---------
FROM python:3.12-slim AS base

WORKDIR /app

# libmagic is required by python-magic for content-based file type detection.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libmagic1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

# --- dev: adds test tooling and the test suite (never used in production) ----
FROM base AS dev

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY pyproject.toml .
COPY tests ./tests

CMD ["pytest"]

# --- production: default build target; clean, no test tooling ----------------
FROM base AS production

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
