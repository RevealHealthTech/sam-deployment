import json
from mangum import Mangum
from app.main import app

# Create a handler for AWS Lambda
lambda_handler = Mangum(app, lifespan="off") 