#!/bin/bash

set -eou pipefail

usage() {
    cat <<EOF
1-package

Packages a lambda function

Usage: 1-package.sh <directory>
Options:
    <directory>             Name of a function e.g. 'MyFunction'

Examples:
    1-package.sh lambda-directory
EOF
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

GREEN='\033[0;32m'
NC='\033[0m' # No Color

LAMBDA_ZIP="${LAMBDA_ZIP:-lambda-package.zip}"
LAMDA_DIRECTORY="$1"
SCRIPT_DIR=$(dirname "$0")
pushd "$SCRIPT_DIR" &> /dev/null

if [[ ! -d "${LAMDA_DIRECTORY}" ]]; then
    echo "${LAMDA_DIRECTORY} does not exist!"
    exit 1
fi

echo "🛠  Packaging Lambda..."
pushd "${LAMDA_DIRECTORY}" &> /dev/null

if [[ -f "requirements.txt" ]]; then
    rm -rf package && mkdir package
    echo -e "✏️  Installing dependencies...\n"
    pip3 install --target ./package -r requirements.txt
    pushd package &> /dev/null
    zip -r ../../"${LAMBDA_ZIP}" .
    popd &> /dev/null
    rm -rf package
fi

# Add lambda_function.py to package
zip ../"${LAMBDA_ZIP}" lambda_function.py
printf "\nPackage: ${GREEN}${LAMBDA_ZIP}${NC} created...\n"
echo "✨  Finished!"
popd +1 &> /dev/null
