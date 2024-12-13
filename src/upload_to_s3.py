import boto3
import os
import sys
import config
from logger import logger

"""
TODO: Infrastructure check
"""

region_name = os.getenv("REGION_NAME")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")


run_date_str = config.execution_date_str    
YEAR = run_date_str[:4]


def main():
    s3 = connect_to_s3()
    config_bucket(s3, config.AWS_BUCKET_NAME)
    upload_csv_to_s3(s3, config.AWS_BUCKET_NAME, f'posts_stats/{YEAR}/{config.POSTS_STATS_FILE_NAME}{run_date_str}.csv',f"{config.TMP_FILE_PATH}{config.POSTS_STATS_FILE_NAME}{run_date_str}.csv")


def connect_to_s3():
    try:
        s3 = boto3.resource(
            's3',
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        return s3
    except Exception as e:
        logger.exception(f"Can't connect to S3. Error: ")
        sys.exit(1)
        
def config_bucket(s3, bucket_name):
    client = s3.meta.client
    response = client.put_bucket_lifecycle_configuration(
        Bucket=bucket_name,
        LifecycleConfiguration={
            'Rules': [
                {
                    'ID': 'Delete-after-one-year',
                    'Status': 'Enabled',
                    'Prefix': '', 
                    'Expiration': {'Days': 366}
                }
            ]
        }
    )
        
def upload_csv_to_s3(s3, bucket_name, s3_path, csv_file):
    print(f"Started uploading csv to S3 {bucket_name}")
    s3.Bucket(bucket_name).upload_file(csv_file,s3_path)
    
       
    
if __name__ == "__main__":
    main()
    


