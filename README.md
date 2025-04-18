# FastAPI Lambda Project

A FastAPI project with healthcheck and presign service endpoints, containerized and deployed to AWS Lambda using Docker.

## Project Structure

```
fastapi-project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── api/
│       ├── __init__.py
│       ├── healthcheck.py
│       └── presign.py
├── Dockerfile
├── Dockerfile.lambda
├── lambda_function.py
├── template.yaml
├── build-lambda.sh
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Features

- FastAPI framework with async support
- Health check endpoint
- Mock S3 presign URL service
- AWS Lambda deployment with Docker
- API Gateway integration
- Poetry for dependency management
- SAM template for infrastructure as code

## Prerequisites

- Python 3.9+
- Docker
- AWS CLI configured
- AWS SAM CLI
- Poetry (optional, for local development)

## Local Development

1. **Install dependencies with Poetry**:
   ```bash
   poetry install
   ```

2. **Run the application locally**:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

3. **Access local endpoints**:
   - API documentation: http://localhost:8000/docs
   - Health check: http://localhost:8000/health
   - Presign service: http://localhost:8000/presign?id=12345&filename=test.txt

## Docker Build and Deployment

### Option 1: Using SAM CLI

1. **Build the application**:
   ```bash
   sam build
   ```

2. **Deploy to AWS**:
   ```bash
   sam deploy --guided
   ```

### Option 2: Manual Docker Build

1. **Make the build script executable**:
   ```bash
   chmod +x build-lambda.sh
   ```

2. **Run the build script**:
   ```bash
   ./build-lambda.sh
   ```

3. **Deploy using AWS CLI**:
   ```bash
   aws lambda update-function-code \
       --function-name fastapi-presign-service \
       --zip-file fileb://lambda-deployment-package.zip
   ```

## API Endpoints

### Health Check
- **GET** `/health`
- Returns service health status and timestamp

### Presign URL Service
- **GET** `/presign`
- Query Parameters:
  - `id`: Unique identifier for the upload
  - `filename`: Name of the file to upload
- Returns a mock S3 presigned URL

### API Documentation
- **GET** `/docs`
- Swagger UI documentation
- **GET** `/redoc`
- ReDoc documentation

## Environment Variables

- `MOCK_BUCKET_NAME`: Name of the mock S3 bucket (default: "mock-bucket")
- `MOCK_REGION`: AWS region for mock S3 (default: "us-east-1")

## AWS Infrastructure

The application is deployed as a Lambda function with:
- API Gateway integration
- x86_64 architecture
- 128MB memory
- 30-second timeout
- Environment variables for configuration

## Development Notes

### Architecture
- Uses FastAPI for the web framework
- Mangum for AWS Lambda integration
- Docker for consistent builds
- SAM for infrastructure management

### Local Testing
```bash
# Run tests (if implemented)
poetry run pytest

# Test the API locally
curl http://localhost:8000/health
curl "http://localhost:8000/presign?id=12345&filename=test.txt"
```

### Deployment Testing
```bash
# Test deployed endpoints
curl https://your-api-id.execute-api.region.amazonaws.com/Prod/health
curl "https://your-api-id.execute-api.region.amazonaws.com/Prod/presign?id=12345&filename=test.txt"
```

## Troubleshooting

1. **Architecture Issues**:
   - Using Docker ensures correct x86_64 builds on any development machine

2. **Lambda Deployment**:
   - Check CloudWatch logs for errors
   - Verify Lambda handler matches: `lambda_function.lambda_handler`
   - Ensure all dependencies are included in the Docker build

3. **API Gateway**:
   - Verify proxy integration is configured correctly
   - Check binary media types settings if serving non-JSON responses

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
