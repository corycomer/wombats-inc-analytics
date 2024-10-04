
# Wombats Inc. Analytics Page

This repository contains the code and infrastructure for **Wombats Inc.'s internal analytics page**, built using AWS services such as **Lambda**, **S3**, **Redshift**, **API Gateway**, and **AWS Glue**. The system handles data ingestion, transformation, storage, and retrieval to provide analytics for internal use.

## Project Overview

The project is divided into three main components:
1. **Data Ingestion**: AWS Lambda functions ingest raw data into S3.
2. **Data Transformation**: AWS Glue jobs transform and load the data into Redshift for analytics.
3. **Data Retrieval**: AWS Lambda functions query Redshift and expose the analytics data via an API Gateway.

## Project Structure

- **`lambda/`**: Contains all AWS Lambda functions:
  - **`ingestion/`**: Lambda function responsible for ingesting data from an external API into S3.
  - **`transformation/`**: (Optional Lambda for transformation, but mainly handled by AWS Glue) Processes and transforms raw data.
  - **`retrieval/`**: Lambda function that queries Redshift and returns analytics data via API Gateway.

- **`glue_jobs/`**: Contains the AWS Glue job script for transforming and loading data from S3 into Redshift.

- **`infrastructure/`**: Infrastructure as Code (IaC) defined using **AWS CDK**. This folder contains stacks for provisioning S3, Redshift, Lambda functions, Glue jobs, and API Gateway.

- **`tests/`**: Contains:
  - **Unit tests** for the Lambda functions.
  - **Integration tests** to validate the end-to-end data pipeline.

- **`scripts/`**: SQL scripts for managing Redshift:
  - **`create_redshift_tables.sql`**: Script to create necessary Redshift tables.
  - **`load_sample_data.sql`**: (Optional) Script for loading sample data into Redshift.
  
- **`.github/workflows/`**: Contains CI/CD pipeline configuration using GitHub Actions to automate testing and deployment.

## Prerequisites

To run this project, you’ll need:
- **AWS CLI** configured with the necessary credentials and permissions.
- **AWS CDK** installed (`npm install -g aws-cdk`).
- **Docker** if using the local development environment for Lambda functions and Redshift.
- **Python 3.8** installed along with the required dependencies listed in the `requirements.txt` files.

## Getting Started

Follow these steps to set up the infrastructure, run the code, and test the system.

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/wombats-inc-analytics.git
cd wombats-inc-analytics
```

### 2. Install Dependencies

Install the Python dependencies for both Lambda functions and development/testing.

```bash
# Install Lambda runtime dependencies
pip install -r ingestion/requirements.txt
pip install -r retrieval/requirements.txt

# Install development/testing dependencies
pip install -r requirements-dev.txt
```

### 3. Deploy the Infrastructure using AWS CDK

You can deploy the entire infrastructure using AWS CDK. Make sure your AWS credentials are configured.

```bash
# Bootstrap the environment (if not done already)
npx cdk bootstrap

# Deploy all the stacks (Lambda, S3, Redshift, Glue, API Gateway)
npx cdk deploy --all --require-approval never
```

### 4. Running Unit Tests

Unit tests are located in the `tests/unit/` directory and can be executed using **pytest**.

```bash
# Run unit tests for Lambda functions
pytest tests/unit/
```

### 5. Running Integration Tests

Integration tests validate the end-to-end data flow from ingestion to retrieval. These tests are located in `tests/integration/`.

```bash
# Run integration tests
pytest tests/integration/
```

### 6. Local Development using Docker Compose

You can run local instances of **Redshift** and **S3** (MinIO) using Docker Compose.

```bash
# Start local Redshift and S3 (MinIO) services
docker-compose up -d
```

### 7. Triggering the Glue Job

The AWS Glue job can be triggered manually via the AWS Management Console or automated in the CDK as part of your deployment pipeline.

```bash
# Trigger AWS Glue Job manually from AWS Console or CLI
```

## Testing the End-to-End Data Pipeline

1. **Ingestion**: Trigger the ingestion Lambda function to pull data from an external API and store it in S3.
   
2. **Transformation**: The Glue job processes data from S3, performs transformations, and loads the data into Redshift.

3. **Retrieval**: The retrieval Lambda function queries Redshift and returns analytics data via the API Gateway.

## CI/CD Pipeline

The repository includes a **GitHub Actions** CI/CD pipeline (`.github/workflows/ci-cd-pipelines.yml`) that automatically:
- Installs dependencies.
- Runs unit and integration tests.
- Deploys the AWS infrastructure using CDK on the `main` branch.

The pipeline runs on every **push** or **pull request** to the `main` branch.

## Clean Up

To remove all the resources created by this project, use the following command:

```bash
npx cdk destroy --all
```

## Conclusion

This project demonstrates how to build an analytics pipeline using AWS Lambda, S3, Redshift, Glue, and API Gateway. By following the steps above, you can deploy, run, and test the entire system.

Feel free to contribute by submitting pull requests or raising issues if you encounter any problems!
