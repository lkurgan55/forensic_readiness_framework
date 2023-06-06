import boto3

s3_client = boto3.client(
    's3',
    region_name = 'us-east-1', 
    aws_access_key_id = 'AKIAZGHC27RHKHS2DBVM',
    aws_secret_access_key = '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'
)
s3_client.download_file('test-bucket-lkurgan', 'AWSLogs/631835917390/CloudTrail/us-east-1/2023/06/06/631835917390_CloudTrail_us-east-1_20230606T0310Z_CbClVchPXm8iKiSh.json.gz', 'file_name') 
