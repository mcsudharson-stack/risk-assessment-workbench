from fastapi import FastAPI

app = FastAPI(
    title="Risk Assessment Workbench",
    description="AI-assisted financial crime risk assessment platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "application": "Risk Assessment Workbench",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}