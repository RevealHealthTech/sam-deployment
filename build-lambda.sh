#!/bin/bash

# Build the Docker image
docker build -t lambda-builder -f Dockerfile.lambda .

# Create a container from the image
container_id=$(docker create lambda-builder)

# Copy the deployment package from the container
docker cp $container_id:/var/task/ ./deployment/

# Create deployment ZIP
cd deployment
zip -r ../lambda-deployment-package.zip .
cd ..

# Cleanup
docker rm $container_id
rm -rf deployment/

echo "Created lambda-deployment-package.zip ready for deployment" 