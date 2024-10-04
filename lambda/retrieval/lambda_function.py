import boto3
import json
import logging
import os

# Initialize the Redshift Data API client
redshift_data = boto3.client('redshift-data')

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Redshift cluster details from environment variables
        cluster_id = os.environ['REDSHIFT_CLUSTER_ID']
        database = os.environ['REDSHIFT_DATABASE']
        secret_arn = os.environ['REDSHIFT_SECRET_ARN']  # Secret for Redshift credentials
        table_name = "public.analytics_table"  # The table to query
        
        # Example query: Fetch top 10 records from the analytics table
        sql_statement = f"SELECT * FROM {table_name} LIMIT 10;"
        
        # Execute the SQL statement via Redshift Data API
        response = redshift_data.execute_statement(
            ClusterIdentifier=cluster_id,
            Database=database,
            SecretArn=secret_arn,
            Sql=sql_statement
        )

        # Fetch the query ID to retrieve the results
        query_id = response['Id']
        
        # Get the results of the query
        result = redshift_data.get_statement_result(Id=query_id)
        records = result['Records']
        
        # Format the data to return in JSON
        data = []
        for record in records:
            row = [col['stringValue'] if 'stringValue' in col else col for col in record]
            data.append(row)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Query executed successfully',
                'data': data
            })
        }

    except Exception as e:
        logger.error(f"Error executing query: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error executing query',
                'error': str(e)
            })
        }
