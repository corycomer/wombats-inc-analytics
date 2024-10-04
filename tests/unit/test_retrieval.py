import unittest
from unittest.mock import patch, MagicMock
import boto3
import json
import os
from retrieval.lambda_function import lambda_handler

class TestRetrievalLambda(unittest.TestCase):

    @patch('boto3.client')
    def test_lambda_handler_success(self, mock_boto3_client):
        # Mock Redshift Data API client and environment variables
        os.environ['REDSHIFT_CLUSTER_ID'] = 'test-cluster'
        os.environ['REDSHIFT_DATABASE'] = 'analytics_db'
        os.environ['REDSHIFT_SECRET_ARN'] = 'arn:aws:secretsmanager:region:account-id:secret:test'

        mock_redshift = MagicMock()
        mock_boto3_client.return_value = mock_redshift

        # Mock Redshift Data API successful execution and results
        mock_redshift.execute_statement.return_value = {'Id': 'test-query-id'}
        mock_redshift.get_statement_result.return_value = {
            'Records': [[{'stringValue': 'value1'}, {'stringValue': 'value2'}]]
        }

        # Call the lambda handler
        event = {}
        context = {}
        response = lambda_handler(event, context)

        # Verify the response
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Query executed successfully', response['body'])

        # Check the returned data format
        body = json.loads(response['body'])
        self.assertEqual(body['data'], [['value1', 'value2']])

    @patch('boto3.client')
    def test_lambda_handler_query_failure(self, mock_boto3_client):
        # Mock Redshift Data API client and environment variables
        os.environ['REDSHIFT_CLUSTER_ID'] = 'test-cluster'
        os.environ['REDSHIFT_DATABASE'] = 'analytics_db'
        os.environ['REDSHIFT_SECRET_ARN'] = 'arn:aws:secretsmanager:region:account-id:secret:test'

        mock_redshift = MagicMock()
        mock_boto3_client.return_value = mock_redshift

        # Simulate an exception when executing the query
        mock_redshift.execute_statement.side_effect = Exception('Query Error')

        # Call the lambda handler
        event = {}
        context = {}
        response = lambda_handler(event, context)

        # Verify the error handling in response
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Error executing query', response['body'])

if __name__ == '__main__':
    unittest.main()
