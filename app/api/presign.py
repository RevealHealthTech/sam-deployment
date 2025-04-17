from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import Optional
import boto3
from moto import mock_s3
import uuid
import os
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs

router = APIRouter(tags=["presign"])

# Mock S3 configuration from environment variables
MOCK_BUCKET_NAME = os.environ.get("MOCK_BUCKET_NAME", "mock-bucket")
MOCK_REGION = os.environ.get("MOCK_REGION", "us-east-1")

class PresignedUrlResponse(BaseModel):
    uploadUrl: str
    key: str

@router.get("/presign", response_model=PresignedUrlResponse)
def get_presigned_url(
    id: str = Query(..., description="Unique identifier for the upload"),
    filename: str = Query(..., description="Name of the file to upload")
):
    """
    Generate a mock S3 presigned URL for file upload.
    
    This endpoint simulates the creation of an S3 presigned URL without actually
    connecting to AWS S3. It creates a realistic-looking URL based on the provided
    ID and filename.
    """
    # Create the S3 key using the ID and filename
    s3_key = f"{id}/{filename}"
    
    # Generate a mock presigned URL that looks realistic
    mock_presigned_url = create_mock_presigned_url(s3_key)
    
    return PresignedUrlResponse(
        uploadUrl=mock_presigned_url,
        key=s3_key
    )

def create_mock_presigned_url(s3_key: str) -> str:
    """
    Create a realistic-looking mock S3 presigned URL.
    
    In a real environment, this would use boto3 to generate an actual presigned URL.
    Since we're mocking, we'll create a URL that has the same structure as a real one.
    """
    # Generate a mock signature
    mock_signature = str(uuid.uuid4()).replace('-', '')
    
    # Generate expiration (15 minutes from now)
    expiration = int((datetime.now() + timedelta(minutes=15)).timestamp())
    
    # Create a realistic-looking presigned URL
    mock_url = (
        f"https://{MOCK_BUCKET_NAME}.s3.{MOCK_REGION}.amazonaws.com/{s3_key}"
        f"?X-Amz-Algorithm=AWS4-HMAC-SHA256"
        f"&X-Amz-Credential=AKIAIOSFODNN7EXAMPLE%2F{datetime.now().strftime('%Y%m%d')}%2F{MOCK_REGION}%2Fs3%2Faws4_request"
        f"&X-Amz-Date={datetime.now().strftime('%Y%m%dT%H%M%SZ')}"
        f"&X-Amz-Expires=900"
        f"&X-Amz-SignedHeaders=host"
        f"&X-Amz-Signature={mock_signature}"
    )
    
    return mock_url



# Optional: If you want to actually test with moto
@router.get("/presign-moto", response_model=PresignedUrlResponse)
@mock_s3
def get_presigned_url_with_moto(
    id: str = Query(..., description="Unique identifier for the upload"),
    filename: str = Query(..., description="Name of the file to upload")
):
    """
    Generate a presigned URL using moto's mock S3 implementation.
    
    This is a more realistic mock that actually uses the moto library to simulate
    AWS S3 behavior locally.
    """
    # Create a mock S3 client
    s3_client = boto3.client('s3', region_name=MOCK_REGION)
    
    # Create a mock bucket (this would normally be done during setup)
    try:
        s3_client.create_bucket(Bucket=MOCK_BUCKET_NAME)
    except s3_client.exceptions.BucketAlreadyExists:
        pass
    
    # Create the S3 key using the ID and filename
    s3_key = f"{id}/{filename}"
    
    # Generate a presigned URL using moto's mock S3
    presigned_url = s3_client.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': MOCK_BUCKET_NAME,
            'Key': s3_key,
            'ContentType': 'application/octet-stream'
        },
        ExpiresIn=900  # 15 minutes
    )
    
    return PresignedUrlResponse(
        uploadUrl=presigned_url,
        key=s3_key
    ) 