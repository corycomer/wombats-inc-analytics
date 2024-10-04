from aws_cdk import core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_glue as glue
from aws_cdk import aws_iam as iam

class GlueStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, s3_bucket, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # IAM role for Glue with necessary permissions
        glue_role = iam.Role(self, "GlueRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole")
            ]
        )

        # Add permissions for Glue to read from S3 and write to Redshift
        s3_bucket.grant_read_write(glue_role)

        # Glue Job Definition
        glue_job = glue.CfnJob(self, "DataTransformationJob",
            role=glue_role.role_arn,
            command=glue.CfnJob.JobCommandProperty(
                name="glueetl",
                script_location=f"s3://{s3_bucket.bucket_name}/glue_jobs/transformation_script.py",  # Path to your Glue job script
                python_version="3"
            ),
            default_arguments={
                "--TempDir": f"s3://{s3_bucket.bucket_name}/temp/",
                "--job-bookmark-option": "job-bookmark-enable"
            },
            max_retries=2,
            max_capacity=2  # Adjust as needed based on the data size
        )

        # Output the Glue Job name
        core.CfnOutput(self, "GlueJobName", value=glue_job.ref)
