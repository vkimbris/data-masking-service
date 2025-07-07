#!/usr/bin/env bash
set -e

aws s3 cp s3://masking/data/names.txt   /app/data/names.txt   --endpoint-url "$AWS_ENDPOINTURL"
aws s3 cp s3://masking/data/surnames.txt /app/data/surnames.txt --endpoint-url "$AWS_ENDPOINTURL"
aws s3 cp s3://masking/data/midnames.txt /app/data/midnames.txt --endpoint-url "$AWS_ENDPOINTURL"

uvicorn main:app --host 0.0.0.0 --port 8000
