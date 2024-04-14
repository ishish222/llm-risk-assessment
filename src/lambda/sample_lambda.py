import boto3

def get_secret(secret_arn):
    """Retrieve secret from AWS Secrets Manager."""
    client = boto3.client('secretsmanager')
    get_secret_value_response = client.get_secret_value(SecretId=secret_arn)
    secret = get_secret_value_response['SecretString']
    return secret

def lambda_handler(event, context):
    secret_arn = os.environ['SECRET_API_KEY_ARN']
    secret_key = get_secret(secret_arn)

    print(event)

