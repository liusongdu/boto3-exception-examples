import boto3


s3_client = client("s3")


def put_bucket_policy(bucket_policy: str, bucket_name: str, source_account: str) -> None:

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/put_bucket_policy.html
    try:
        s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=bucket_policy
        )

    # https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html#ErrorCodeList
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"Error code: {error_code}. Error message: {error_message}")

        if error_code == 'AccessDenied':
            logger.error("AccessDenied")
            logger.error(f"Access denied when updating bucket policy for '{bucket_name}': {error_message}")
            raise e
        elif error_code == 'NoSuchBucket':
            logger.error(f"Bucket '{bucket_name}' does not exist: {error_message}")
            raise e
        elif error_code == 'MalformedPolicy':
            logger.error(f"Malformed policy document for bucket '{bucket_name}': {error_message}")
            raise e
        # Add more exception scenarios as needed
        else:
            logger.error(f"AWS S3 error updating bucket policy for '{bucket_name}': {error_code} - {error_message}")
            raise e
    except Exception as e:
        logger.error(f"Failed to update bucket policy for '{bucket_name}' in account '{source_account}'.")
        logger.error(e)
        logger.error(f"{type(e).__name__}: {e}")
        raise e
