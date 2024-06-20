import json
from lambda_function import lambda_handler

def test_lambda_handler():
    event = {
        "bucket_name": "your-s3-bucket-name",
        "file_key": "path/to/data.json"
    }
    result = lambda_handler(event, None)
    assert result['statusCode'] == 200
    body = json.loads(result['body'])
    assert 'summary' in body
