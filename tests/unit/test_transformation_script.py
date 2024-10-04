import unittest
from unittest.mock import patch, MagicMock
from pyspark.sql import SparkSession
from pyspark.sql import Row
import glue_jobs.transformation_script as script  # Adjust the import path based on your project structure

class TestGlueTransformation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize a local PySpark session for testing
        cls.spark = SparkSession.builder.master("local[1]").appName("GlueTest").getOrCreate()

    @patch('glue_jobs.transformation_script.GlueContext')  # Mock GlueContext
    @patch('glue_jobs.transformation_script.DynamicFrame')  # Mock DynamicFrame
    def test_transformation_logic(self, mock_dynamic_frame, mock_glue_context):
        # Prepare sample data for testing
        raw_data = [
            Row(important_field="value1", other_field="ignore1"),
            Row(important_field=None, other_field="ignore2"),
            Row(important_field="value2", other_field="ignore3")
        ]

        # Create a Spark DataFrame from the sample data
        df = self.spark.createDataFrame(raw_data)

        # Mock the GlueContext and DynamicFrame
        mock_glue_context.return_value.create_dynamic_frame.from_options.return_value = mock_dynamic_frame
        mock_dynamic_frame.toDF.return_value = df

        # Call the transformation function from the script (filtered data)
        transformed_df = script.transform_data(df)

        # Collect the results
        result = transformed_df.collect()

        # Check that the transformation removed rows with None in the important_field
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].important_field, "value1")
        self.assertEqual(result[1].important_field, "value2")

    def tearDownClass(cls):
        # Stop the Spark session after all tests are done
        cls.spark.stop()

if __name__ == '__main__':
    unittest.main()
