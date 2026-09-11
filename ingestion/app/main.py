from fastapi import FastAPI

app = FastAPI(title="Remembrall Ingestion")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ingestion"}
