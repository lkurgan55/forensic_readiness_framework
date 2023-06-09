import json

log = {'eventVersion': '1.08', 
       'userIdentity': {
           'type': 'Root', 'principalId': '631835917390', 'arn': 'arn:aws:iam::631835917390:root', 
           'accountId': '631835917390', 'accessKeyId': 'ASIAZGHC27RHHLN7VD4J', 
           'sessionContext': {'sessionIssuer': {}, 'webIdFederationData': {}, 'attributes': {'creationDate': '2023-05-27T14:54:58Z', 'mfaAuthenticated': 'false'}}
           }, 
           'eventTime': '2023-05-27T15:35:54Z', 
           'eventSource': 'notifications.amazonaws.com', 
           'eventName': 'ListNotificationHubs', 
           'awsRegion': 'us-east-1', 
           'sourceIPAddress': '195.3.128.49', 
           'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36', 
           'requestParameters': None, 'responseElements': None, 'requestID': 'a0cdee96-4547-4999-9108-1e77619dab32', 
           'eventID': '0c189c2e-b13b-4548-a138-c5f3f362bd1a', 
           'readOnly': True, 'eventType': 'AwsApiCall', 'managementEvent': True, 'recipientAccountId': '631835917390', 'eventCategory': 'Management'}

def analyze_log(log, **custom_params):
    score = 0

    user_identity_type = log.get('userIdentity', '').get('type', '')
    if user_identity_type:
        score += 10 if user_identity_type in ['Root'] + custom_params.get('user_identities', []) else 0

    source_ip = log.get('sourceIPAddress', '')
    if source_ip:
        score += 2 if source_ip not in custom_params.get('trusted_ips', []) else 0

    event_name = log.get('eventName', '')
    if event_name:
        score += 5 if any(
            key_word in event_name 
            for key_word in ['Create', 'Update', 'Delete', 'Change', 'Deactivate', 'Activate' 'Attach', 'Upload'] 
            + custom_params.get('event_names', [])
            ) else 0

    event_type = log.get('eventType', '')
    if event_type:
        score += 5 if event_type in ['AwsConsoleSignIn', 'AwsConsoleAction'] \
            + custom_params.get('user_identities', []) else 0

    read_only = log.get('readOnly', True)
    if not read_only:
        score += 7

    return score


custom_params = {
    'trusted_ips': ['195.3.128.49'],
    'event_names': ['List', 'Submit', 'Stop']
}

print(analyze_log(log, **custom_params))




