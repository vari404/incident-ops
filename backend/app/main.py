from fastapi import FastAPI


app = FastAPI(
    title="IncidentOps API",
    description="Backend API for the IncidentOps support platform.",
    version="0.1.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "IncidentOps API is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}