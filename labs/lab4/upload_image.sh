#!/bin/bash

LOCAL_FILE="$1"
BUCKET="$2"
EXP_TIME="$3"

aws s3 cp "$LOCAL_FILE" s3://"$BUCKET"/

aws s3 presign --expires-in "$EXP_TIME" s3://"$BUCKET"/"$LOCAL_FILE"
