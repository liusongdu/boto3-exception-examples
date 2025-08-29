import boto3


sts_client = boto3.client('sts')


def assume_role(account_id: str, role) -> Session:
    role_arn = f"arn:{AWS_PARTITION}:iam::{account_id}:role/{role}"

    try:
        assumed_role = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName="ExampleSession"
        )

    # https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html#API_AssumeRole_Errors
    except sts_client.exceptions.ExpiredToken as e:
        logger.error("The web identity token that was passed is expired or is not valid. Get a new identity token from the identity provider and then retry the request.")
        raise e
    except sts_client.exceptions.MalformedPolicyDocument as e:
        logger.error("The request was rejected because the policy document was malformed. The error message describes the specific error.")
        raise e
    except sts_client.exceptions.PackedPolicyTooLarge as e:
        logger.error("The request was rejected because the total packed size of the session policies and session tags combined was too large. An AWS conversion compresses the session policy document, session policy ARNs, and session tags into a packed binary format that has a separate limit. The error message indicates by percentage how close the policies and tags are to the upper size limit. For more information, see Passing Session Tags in AWS STS in the IAM User Guide. You could receive this error even though you meet other defined session policy and session tag limits. For more information, see IAM and AWS STS Entity Character Limits in the IAM User Guide.")
        raise e
    except sts_client.exceptions.RegionDisabled as e:
        logger.error("AWS STS is not activated in the requested region for the account that is being asked to generate credentials. The account administrator must use the IAM console to activate AWS STS in that region. For more information, see Activating and Deactivating AWS STS in an AWS Region in the IAM User Guide.")
        raise e
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"Error code: {error_code}. Error message: {error_message}")

        if error_code == "AccessDeniedException":
            logger.error("AccessDenied")
            raise e
        # Add more exception scenarios as needed
        else:
            logger.error(f"Unknown client error.")
            raise e
    except Exception as e:
        logger.error("An error occurred while assuming role.")
        logger.error(e)
        raise e

    credentials = assumed_role['Credentials']
    session = boto3.session.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )
    # print(f'Assumed remediation session with role: {role_arn} '
    # f'in the target account: {account_id}')
    return session
