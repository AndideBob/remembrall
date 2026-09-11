from fastapi import FastAPI

app = FastAPI(title="Remembrall API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "api"}
