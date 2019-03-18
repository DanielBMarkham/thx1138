#!/usr/bin/env
# uncomment below to stop script from running
#exit 0

#set -o nounset
set -o errexit
set -o pipefail
[[ "${DEBUG}" == 'true' ]] && set -o xtrace

cd deploy
aws s3 cp airtable-sync-lambda.zip s3://markham-lambda-1

aws s3 cp airtable-sync-lambda.zip s3://markham-lambda-1