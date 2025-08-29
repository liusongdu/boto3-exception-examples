import boto3


secrets_manager_client = boto3.client('secretsmanager')


def get_secret_value(secret_id: str) -> dict:
    get_secret_value_response: dict = {}
    try:
        get_secret_value_response = secrets_manager_client.get_secret_value(
            SecretId=secret_id
        )

    # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    except secrets_manager_client.exceptions.DecryptionFailure as e:
        error_code = e.response.get('Error', {}).get('Code')
        logger.error(f'Error Code: {error_code}')
        logger.info("Secrets Manager can't decrypt the protected secret text using the provided KMS key.")
        raise e
    except secrets_manager_client.exceptions.InternalServiceError as e:
        error_code = e.response.get('Error', {}).get('Code')
        logger.error(f'Error Code: {error_code}')
        logger.info("An error occurred on the server side.")
        raise e
    except secrets_manager_client.exceptions.InvalidParameterException as e:
        error_code = e.response.get('Error', {}).get('Code')
        logger.error(f'Error Code: {error_code}')
        logger.info("The parameter name or value is invalid.")
        raise e
    except secrets_manager_client.exceptions.InvalidRequestException as e:
        error_code = e.response.get('Error', {}).get('Code')
        logger.error(f'Error Code: {error_code}')
        logger.info("A parameter value is not valid for the current state of the resource. Possible causes: (1) The secret is scheduled for deletion. (2) You tried to enable rotation on a secret that doesn't already have a Lambda function ARN configured and you didn't include such an ARN as a parameter in this call. (3) The secret is managed by another service, and you must use that service to update it. For more information, see Secrets managed by other AWS services.")
        raise e
    except secrets_manager_client.exceptions.ResourceNotFoundException as resource_not_found_exception_error:
        error_code = resource_not_found_exception_error.response.get('Error', {}).get('Code')
        logger.error(f'Error Code: {error_code}')
        logger.info("Secrets Manager can't find the resource that you asked for.")
        # logger.error("Error response JSON:\n%s", json.dumps(resource_not_found_exception_error.response, indent=2, sort_keys=True, default=str))
        raise resource_not_found_exception_error

    # https://docs.aws.amazon.com/secretsmanager/latest/apireference/CommonErrors.html
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code')
        logger.error(f'Error Code: {error_code}')
        if e.response['Error']['Code'] == 'AccessDeniedException':
            raise e
        elif e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    except Exception as e:
        logger.error("Unknown error")
        raise e

    return get_secret_value_response
