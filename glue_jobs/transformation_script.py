import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

# Initialize Glue context and job parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Parameters
s3_input_path = "s3://wombats-analytics/raw_data/"
redshift_temp_dir = "s3://wombats-analytics/temp/"
redshift_table = "public.analytics_table"  # Adjust for your Redshift table
redshift_db = "analytics_db"

# Load data from S3
datasource = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [s3_input_path]},
    format="json"
)

# Example transformation function: Filter out entries with null values in a column
def transform_data(df):
    # Apply transformation: Filter out rows with None in 'important_field'
    return df.filter(df["important_field"].isNotNull())

# Convert DynamicFrame to DataFrame for transformation
df = datasource.toDF()

# Call the transformation function
transformed_df = transform_data(df)

# You can apply more transformations here (e.g., renaming columns, type conversions)

# Convert back to DynamicFrame for writing to Redshift
final_frame = DynamicFrame.fromDF(transformed_df, glueContext, "final_frame")

# Write the transformed data to Redshift
glueContext.write_dynamic_frame.from_jdbc_conf(
    frame=final_frame,
    catalog_connection="redshift_connection",
    connection_options={
        "dbtable": redshift_table,
        "database": redshift_db
    },
    redshift_tmp_dir=redshift_temp_dir
)

# Commit the job
job.commit()
