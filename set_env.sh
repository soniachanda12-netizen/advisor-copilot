#!/bin/bash

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    exit 1
fi

# Export environment variables from .env file
export $(cat .env | grep -v '^#' | xargs)

echo "Environment variables set successfully:"
echo "PROJECT_ID=$PROJECT_ID"
echo "LOCATION=$LOCATION"
echo "MODEL_NAME=$MODEL_NAME"
echo "BQ_DATASET=$BQ_DATASET"
