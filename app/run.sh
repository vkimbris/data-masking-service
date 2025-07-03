#!/usr/bin/env bash
set -e

aws s3 cp s3://masking/data/names.txt   /server/data/names.txt   --endpoint-url "$AWS_ENDPOINTURL"
aws s3 cp s3://masking/data/surnames.txt /server/data/surnames.txt --endpoint-url "$AWS_ENDPOINTURL"
aws s3 cp s3://masking/data/midnames.txt /server/data/midnames.txt --endpoint-url "$AWS_ENDPOINTURL"

uvicorn main:app --host 0.0.0.0 --port 8000
