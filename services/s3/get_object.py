import boto3


s3_client = boto3.client("s3")


def s3_get_object(bucket, object_key):
    try:
        obj = s3_client.get_object(Bucket=bucket, Key=object_key)

    # https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html
    except s3_client.exceptions.InvalidObjectState as e:
        logger.error(e)
        logger.error("Object is archived and inaccessible until restored. If the object you are retrieving is stored in the S3 Glacier Flexible Retrieval storage class, the S3 Glacier Deep Archive storage class, the S3 Intelligent-Tiering Archive Access tier, or the S3 Intelligent-Tiering Deep Archive Access tier, before you can retrieve the object you must first restore a copy using RestoreObject. Otherwise, this operation returns an InvalidObjectState error. For information about restoring archived objects, see Restoring Archived Objects in the Amazon S3 User Guide.")
        raise e
    except s3_client.exceptions.NoSuchKey as e:
        logger.error(e)
        logger.error("NoSuchKey.")
        raise e

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"Error code: {error_code}. Error message: {error_message}.")

        if error_code == 'AccessDenied':
            logger.error("AccessDenied")
            raise e
        # Add more exception scenarios as needed
        else:
            logger.error(f"Unknown client error.")
            raise e
    except Exception as e:
        logger.error("An error occurred while reading the file from S3.")
        logger.error(e)
        raise e
    return json.loads(obj['Body'].read().decode("utf-8"))
