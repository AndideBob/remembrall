from fastapi import FastAPI

app = FastAPI(title="Remembrall LLM Gateway")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "llm-gateway"}
