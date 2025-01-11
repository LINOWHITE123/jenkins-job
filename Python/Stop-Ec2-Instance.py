
import boto3

def stop_ec2_instances(vpc_id, exclude_instance_id, region='us-east-1'):
    """
    Stop EC2 instances in a specific VPC while excluding a specific instance.

    :param vpc_id: The VPC ID containing the instances to stop.
    :param exclude_instance_id: The instance ID to exclude from stopping.
    :param region: AWS region where the VPC and instances are located.
    """
    # Initialize EC2 client
    ec2_client = boto3.client('ec2', region_name=region)
    
    try:
        # Retrieve all running instances in the specified VPC
        response = ec2_client.describe_instances(
            Filters=[
                {'Name': 'vpc-id', 'Values': [vpc_id]},
                {'Name': 'instance-state-name', 'Values': ['running']}  # Only running instances
            ]
        )
        
        # Extract instance IDs, excluding the specified instance
        instance_ids = [
            instance['InstanceId']
            for reservation in response['Reservations']
            for instance in reservation['Instances']
            if instance['InstanceId'] != exclude_instance_id
        ]
        
        # Stop the instances if there are any to stop
        if instance_ids:
            stop_response = ec2_client.stop_instances(InstanceIds=instance_ids)
            print(f"Stopped instances: {', '.join(instance_ids)}")
        else:
            print("No instances to stop or all are excluded.")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Example usage
if __name__ == "__main__":
    VPC_ID = "vpc-00c29728063d5bdef"  # Replace with your VPC ID
    EXCLUDE_INSTANCE_ID = "i-0193957f72e6b01ee"  # Replace with the instance ID to exclude
    REGION = "us-east-2"  # Replace with your region if different

    stop_ec2_instances(VPC_ID, EXCLUDE_INSTANCE_ID, REGION)
