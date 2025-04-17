import json
from mangum import Mangum
from app.main import app

# Create a handler for AWS Lambda
lamda_handler = Mangum(app) 