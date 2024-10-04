import boto3
import requests
import json
import logging
from botocore.exceptions import ClientError

# Initialize S3 client outside the handler for better performance
s3 = boto3.client('s3')

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Specify the bucket name and key dynamically via environment variables
    bucket_name = os.environ['BUCKET_NAME']
    key = "raw_data/raw_data.json"  # Adjust based on your data structure needs

    try:
        # Fetch data from an external API
        response = requests.get("https://api.example.com/data", timeout=10)
        
        # Check for successful response
        if response.status_code != 200:
            logger.error(f"Failed to fetch data: {response.status_code}")
            return {
                'statusCode': response.status_code,
                'body': f"Failed to fetch data: {response.status_code}"
            }
        
        # Parse the JSON response
        data = response.json()

        # Optional: Validate or preprocess data if needed
        if not isinstance(data, dict):
            logger.error("Unexpected data format, expected a JSON object.")
            return {
                'statusCode': 500,
                'body': 'Invalid data format received from API'
            }

        # Convert the data to JSON and upload it to S3
        s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(data))
        
        logger.info(f"Successfully ingested data to S3 at s3://{bucket_name}/{key}")

        return {
            'statusCode': 200,
            'body': 'Data successfully ingested to S3'
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from the API: {e}")
        return {
            'statusCode': 500,
            'body': 'Error fetching data from the API'
        }

    except ClientError as e:
        logger.error(f"Error uploading data to S3: {e}")
        return {
            'statusCode': 500,
            'body': 'Error uploading data to S3'
        }
