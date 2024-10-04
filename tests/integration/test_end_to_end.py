import unittest
import boto3
import json
import os

class TestEndToEnd(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize boto3 clients
        cls.s3 = boto3.client('s3')
        cls.lambda_client = boto3.client('lambda')

    def test_end_to_end_pipeline(self):
        # Check if data was ingested into S3
        bucket_name = 'wombats-analytics'
        object_key = 'raw_data/raw_data.json'  # Adjusted to match the key from the ingestion Lambda
        ingestion_result = self.s3.get_object(Bucket=bucket_name, Key=object_key)
        
        # Verify that the S3 object is not empty
        self.assertIsNotNone(ingestion_result)
        self.assertIn('Body', ingestion_result)
        
        # Parse and check that the S3 data is a valid JSON
        s3_data = json.loads(ingestion_result['Body'].read().decode('utf-8'))
        self.assertIsInstance(s3_data, dict)  # Assuming the ingested data is a dictionary

        # Now test the data retrieval from the Lambda (Redshift query)
        lambda_response = self.lambda_client.invoke(
            FunctionName='retrieval-lambda',  # Adjust to your actual Lambda function name
            Payload=json.dumps({})
        )

        # Check that Lambda executed successfully
        self.assertEqual(lambda_response['StatusCode'], 200)

        # Parse the response payload
        lambda_payload = json.loads(lambda_response['Payload'].read().decode('utf-8'))
        self.assertIn('body', lambda_payload)

        # Check that the response body contains valid JSON data
        response_body = json.loads(lambda_payload['body'])
        self.assertIn('message', response_body)
        self.assertIn('data', response_body)

        # Ensure the data field is a list (the rows returned from Redshift)
        self.assertIsInstance(response_body['data'], list)
        self.assertGreater(len(response_body['data']), 0)  # Check that some data is returned

    @classmethod
    def tearDownClass(cls):
        # Optional: Clean up resources, if necessary (e.g., delete S3 objects, etc.)
        pass

if __name__ == '__main__':
    unittest.main()
