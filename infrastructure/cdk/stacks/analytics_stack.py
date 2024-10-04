from aws_cdk import core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_iam as iam

class AnalyticsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, redshift_cluster, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # S3 bucket for raw data (with encryption enabled)
        bucket = s3.Bucket(self, 
            "RawDataBucket",
            encryption=s3.BucketEncryption.S3_MANAGED,
            versioned=True,
            removal_policy=core.RemovalPolicy.DESTROY  # Optional: Clear bucket when the stack is destroyed
        )

        # Lambda function for data ingestion (Ingesting data into S3)
        ingestion_lambda = _lambda.Function(
            self, "IngestionLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda/ingestion"),
            environment={
                "BUCKET_NAME": bucket.bucket_name  # Pass S3 bucket name to the Lambda environment
            }
        )

        # Add permissions for Lambda to write to S3
        bucket.grant_put(ingestion_lambda)

        # Define an IAM role for Lambda with least privilege
        ingestion_lambda_role = iam.Role(self, "IngestionLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
            ]
        )

        # Lambda function for data retrieval (Querying data from Redshift)
        retrieval_lambda = _lambda.Function(
            self, "RetrievalLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda/retrieval"),
            environment={
                "REDSHIFT_CLUSTER_ID": redshift_cluster.cluster_identifier,
                "REDSHIFT_DATABASE": "analytics_db",
                "REDSHIFT_SECRET_ARN": "<Your Secret ARN here>"  # Secret ARN to retrieve Redshift credentials
            }
        )

        # Add permissions for the retrieval Lambda to use Redshift Data API
        retrieval_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=["redshift-data:ExecuteStatement", "redshift-data:GetStatementResult"],
            resources=["*"]  # You can restrict this further if necessary
        ))

        # API Gateway for both ingestion and retrieval Lambdas
        api = apigw.RestApi(self, "AnalyticsAPI")

        # Define an endpoint for data ingestion
        ingestion_integration = apigw.LambdaIntegration(ingestion_lambda)
        api.root.add_resource("ingest").add_method("POST", ingestion_integration)

        # Define an endpoint for data retrieval
        retrieval_integration = apigw.LambdaIntegration(retrieval_lambda)
        api.root.add_resource("retrieve").add_method("GET", retrieval_integration)

        # CloudWatch integration for monitoring
        ingestion_lambda.add_environment(
            "LOG_LEVEL", "INFO"  # Can use this for log levels in Lambda function
        )

        # Output the API Gateway URL
        core.CfnOutput(self, "APIEndpoint", value=api.url)
