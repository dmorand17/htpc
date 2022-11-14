#!/bin/bash

set -ou pipefail

usage() {
    cat <<EOF
1-upload-function.sh

Creates/Updates a lambda function

Usage: 2-upload.sh <function_name>
Options:
    <function_name>         Name of a function e.g. 'MyFunction'
    <zip_file>              Zip file to deploy
    

Examples:
    2-upload.sh MyFunction myfunction.zip
EOF
}

if [[ $# -lt 2 ]]; then
  usage
  exit 1
fi

exe() { echo "\$ $*" ; "$@" ; }

GREEN='\033[0;32m'
NC='\033[0m' # No Color

SCRIPT_DIR=$(dirname "$0")
pushd "$SCRIPT_DIR" &> /dev/null

FUNCTION="$1"
LAMBDA_ZIP="${LAMBDA_ZIP:-$2}"
LAMBDA_RUNTIME="${LAMBDA_RUNTIME:-python3.9}"

shift 2
# Check if lambda function exists
aws lambda get-function --function-name ${FUNCTION} &> /dev/null

if [[ 0 -eq  $? ]]; then
    echo "Updating ${FUNCTION}..."
    exe aws lambda update-function-code \
    --function-name "${FUNCTION}" \
    --zip-file "fileb://${LAMBDA_ZIP}" "$@"
else
    echo "Creating '${FUNCTION}'..."
    ROLE_ID=$(aws iam get-role --role-name ${FUNCTION}-role | jq -r '.Role.Arn')
    if [[ 0 -eq $? ]]; then
        echo "Role '${FUNCTION}-role' already exists..."
    else
        echo "Creating '${FUNCTION}-role' IAM role"
        ROLE_ID=$(aws iam create-role --role-name ${FUNCTION}-role --assume-role-policy-document file://resources/lambda-role.json | jq -r '.Role.Arn')
        echo "📝  Role '${ROLE_ID}' created"
    fi 

    exe aws lambda create-function \
    --role ${ROLE_ID} \
    --function-name "${FUNCTION}" \
    --runtime ${LAMBDA_RUNTIME} \
    --handler lambda_function.lambda_handler \
    --zip-file "fileb://${LAMBDA_ZIP}" "$@"
fi

echo "✨  Finished!"

popd &> /dev/null
