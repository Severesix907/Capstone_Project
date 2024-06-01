

import boto3
import pandas as pd
from io import StringIO


# create s3 client
s3 = boto3.client('s3')

name = "data-analyst-job-east"
file = "gsearch_jobs.csv"
single_object = s3.get_object(Bucket=name, Key=file)

single_df = pd.read_csv(single_object['Body'])
print(single_df.head())  #etl transformation

