import json
import gzip
 
# Opening JSON file
with gzip.open('aws_logs/2023_05_27/631835917390_CloudTrail_us-east-1_20230527T2000Z_gU9u5rZaxhP7jjzO.json.gz') as json_file:
    data = json.load(json_file)

print(data['Records'])