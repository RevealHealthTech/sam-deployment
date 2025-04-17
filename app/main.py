from fastapi import FastAPI
from app.api.healthcheck import router as healthcheck_router
from app.api.presign import router as presign_router

app = FastAPI(
    title="FastAPI Project",
    description="A FastAPI project with healthcheck endpoint and S3 presign service",
    version="0.1.0"
)

# Include routers
app.include_router(healthcheck_router)
app.include_router(presign_router)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Project"} 