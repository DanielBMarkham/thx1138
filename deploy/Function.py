'''
    fetch data from AirTable API and write to a file on S3

    set as environment variables for Lambda function

    required:
    - AIRTABLE_APP - AirTable app id (from https://airtable.com/api)
    - AIRTABLE_TABLE - AirTable table id (from https://airtable.com/api)
    - AIRTABLE_TOKEN - API token (from https://airtable.com/api)
    - S3_BUCKET - destination bucket

    optional (will use defaults if not set):
    - S3_FILENAME - destination filename (default airtable.json)
    - ACL - access control for S3 file (default public-read)
    - CACHE_HOURS - set Expires header to this many hours in future (default 6)
'''

from datetime import datetime, timedelta
import json
import os

import boto3
from botocore.vendored import requests

ssm = boto3.client('ssm')
AIRTABLE_TOKEN=ssm.get_parameter(Name='/dev/airtable-token', WithDecryption=True)['Parameter']['Value']
AIRTABLE_APP=ssm.get_parameter(Name='/dev/airtable-app', WithDecryption=True)['Parameter']['Value']

API_URL = 'https://api.airtable.com/v0/%s/%s' % (
    AIRTABLE_APP, 'Entries')
'''
AUTH = {'Authorization': 'Bearer %s' % os.environ['AIRTABLE_TOKEN']}
FILENAME = os.environ.get('S3_FILENAME', 'airtable.json')
'''
FILENAME = 'Entries.json'
AUTH = {'Authorization': 'Bearer %s' % AIRTABLE_TOKEN}
BUCKET = os.environ['S3_BUCKET']

def load_data():
    '''
        load data from AirTable, fetching additional pages if needed
    '''
    rval = {'updated': datetime.now().isoformat()}
    params = {}
    if os.environ.get('AIRTABLE_VIEW', None):
        params['view'] = os.environ['AIRTABLE_VIEW']
    req = requests.get(API_URL, headers=AUTH, params=params)
    rval = req.json()
    data = req.json()
    while data.get('offset'):
        params['offset'] = data['offset']
        req = requests.get(API_URL, headers=AUTH, params=params)
        print('offset=%s url=%s request=%s' % (params['offset'], API_URL, req))
        data = req.json()
        rval['records'] += data.get('records', [])
    print('loaded %s records' % (len(rval.get('records', []))))
    return rval


def write_json(data):
    '''
        write to S3 bucket
    '''
    s3 = boto3.resource('s3')
    print('put %s/%s' % (BUCKET, FILENAME))
    hours = int(os.environ.get('CACHE_HOURS', 6))
    expires_dt = (datetime.now() + timedelta(hours=hours))
    s3.Object(BUCKET, FILENAME).put(
        Body=json.dumps(data),
        ContentType='application/json',
        ACL=os.environ.get('ACL', 'public-read'),
        Expires=expires_dt
    )


def lambda_handler(event, context):
    write_json(load_data())

    global FILENAME
    FILENAME = 'Tags'
    global API_URL
    API_URL = 'https://api.airtable.com/v0/%s/%s' % (
        AIRTABLE_APP,'Tags')
    write_json(load_data())


    FILENAME = 'Categories'
    API_URL = 'https://api.airtable.com/v0/%s/%s' % (
        AIRTABLE_APP, 'Categories')
    write_json(load_data())


    FILENAME = 'Media'
    API_URL = 'https://api.airtable.com/v0/%s/%s' % (
        AIRTABLE_APP, 'Media')
    write_json(load_data())


    FILENAME = 'Authors'
    API_URL = 'https://api.airtable.com/v0/%s/%s' % (
        AIRTABLE_APP, 'Authors')
    write_json(load_data())

    FILENAME = 'Questions'
    API_URL = 'https://api.airtable.com/v0/%s/%s' % (
      AIRTABLE_APP, 'Questions')
    write_json(load_data())


if __name__ == '__main__':
    print('get data from %s and write to %s/%s' % (API_URL, BUCKET, FILENAME))
    write_json(load_data())

