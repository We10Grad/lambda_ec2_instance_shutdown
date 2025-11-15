# Python script to stop all running EC2 instances
import boto3
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambda function to stop all running EC2 instances.
    
    Args:
        event: AWS Lambda event object
        context: AWS Lambda context object
        
    Returns:
        dict: Response with status code and details of stopped instances
    """
    
    # Initialize EC2 client
    ec2 = boto3.client('ec2')
    
    try:
        # Find all running instances
        response = ec2.describe_instances(
            Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': ['running']
                }
            ]
        )
        
        # Extract instance IDs from response
        instance_ids = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_ids.append(instance['InstanceId'])
        
        # Check if there are any running instances
        if not instance_ids:
            logger.info("No running instances found")
            return {
                'statusCode': 200,
                'body': 'No running instances to stop'
            }
        
        # Stop the instances
        logger.info(f"Stopping instances: {instance_ids}")
        stop_response = ec2.stop_instances(InstanceIds=instance_ids)
        
        logger.info(f"Successfully initiated stop for {len(instance_ids)} instance(s)")
        
        return {
            'statusCode': 200,
            'body': f'Successfully stopped {len(instance_ids)} instance(s): {instance_ids}',
            'stopped_instances': instance_ids
        }
        
    except Exception as e:
        logger.error(f"Error stopping instances: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }