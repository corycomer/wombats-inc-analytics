import unittest
from unittest.mock import patch, MagicMock
import boto3
from botocore.exceptions import ClientError
from moto import mock_s3
import json
import os
from ingestion.lambda_function import lambda_handler

class TestIngestionLambda(unittest.TestCase):

    @mock_s3
    @patch('requests.get')
    def test_lambda_handler_success(self, mock_get):
        # Mock S3 and setup the environment variable
        s3 = boto3.client('s3', region_name='us-east-1')
        bucket_name = 'test-bucket'
        s3.create_bucket(Bucket=bucket_name)
        os.environ['BUCKET_NAME'] = bucket_name

        # Mock successful API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'key': 'value'}

        # Call the lambda handler
        event = {}
        context = {}
        response = lambda_handler(event, context)

        # Verify the response and S3 upload
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Data successfully ingested to S3', response['body'])

        # Check if the object was uploaded to S3
        result = s3.get_object(Bucket=bucket_name, Key='raw_data/raw_data.json')
        self.assertEqual(json.loads(result['Body'].read().decode('utf-8')), {'key': 'value'})

    @mock_s3
    @patch('requests.get')
    def test_lambda_handler_api_failure(self, mock_get):
        # Mock the S3 and set environment variable
        s3 = boto3.client('s3', region_name='us-east-1')
        bucket_name = 'test-bucket'
        s3.create_bucket(Bucket=bucket_name)
        os.environ['BUCKET_NAME'] = bucket_name

        # Mock failed API response
        mock_get.return_value.status_code = 500

        # Call the lambda handler
        event = {}
        context = {}
        response = lambda_handler(event, context)

        # Verify that the error is properly handled
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Failed to fetch data', response['body'])

    @mock_s3
    @patch('requests.get')
    def test_lambda_handler_s3_upload_failure(self, mock_get):
        # Mock S3 and set environment variable
        s3 = boto3.client('s3', region_name='us-east-1')
        bucket_name = 'test-bucket'
        os.environ['BUCKET_NAME'] = bucket_name

        # Mock successful API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'key': 'value'}

        # Simulate S3 upload failure by raising a ClientError
        with patch('boto3.client.put_object') as mock_s3_put:
            mock_s3_put.side_effect = ClientError(
                error_response={'Error': {'Code': '500', 'Message': 'InternalError'}},
                operation_name='PutObject'
            )

            # Call the lambda handler
            event = {}
            context = {}
            response = lambda_handler(event, context)

            # Verify that the error is properly handled
            self.assertEqual(response['statusCode'], 500)
            self.assertIn('Error uploading data to S3', response['body'])

if __name__ == '__main__':
    unittest.main()
