from fastapi import APIRouter, status
from datetime import datetime

router = APIRouter(tags=["healthcheck"])

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Healthcheck endpoint to verify the service is running
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
    } 