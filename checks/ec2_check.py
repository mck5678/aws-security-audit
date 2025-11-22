import boto3
from colorama import Fore, Style
from utils.issue_tracker import add_issue


def check_ec2_instances():
    """Check EC2 instances for security issues"""
    print(f"\n{Fore.CYAN}=== Checking EC2 Instances ==={Style.RESET_ALL}")
    
    try:
        ec2 = boto3.client('ec2')
        response = ec2.describe_instances()
        
        instance_count = 0
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_count += 1
                instance_id = instance['InstanceId']
                state = instance['State']['Name']
                
                if state != 'running':
                    continue
                
                has_public_ip = instance.get('PublicIpAddress') is not None
                
                if has_public_ip:
                    add_issue('low', f"EC2 instance '{instance_id}' has PUBLIC IP")
                    print(f"{Fore.YELLOW}⚠️  WARNING: Instance '{instance_id}' has PUBLIC IP: {instance['PublicIpAddress']}")
                else:
                    print(f"{Fore.GREEN}✅ Instance '{instance_id}' has no public IP")
                
                for volume in instance.get('BlockDeviceMappings', []):
                    volume_id = volume['Ebs']['VolumeId']
                    
                    try:
                        vol_details = ec2.describe_volumes(VolumeIds=[volume_id])
                        encrypted = vol_details['Volumes'][0]['Encrypted']
                        
                        if not encrypted:
                            add_issue('high', f"EBS volume '{volume_id}' on instance '{instance_id}' is NOT ENCRYPTED")
                            print(f"{Fore.RED}❌ RISK: Volume '{volume_id}' on instance '{instance_id}' is NOT ENCRYPTED")
                        else:
                            print(f"{Fore.GREEN}✅ Volume '{volume_id}' is encrypted")
                    except Exception as e:
                        print(f"{Fore.YELLOW}⚠️  Could not check volume '{volume_id}': {str(e)}")
        
        if instance_count == 0:
            print(f"{Fore.YELLOW}No EC2 instances found")
            
    except Exception as e:
        print(f"{Fore.RED}Error checking EC2 instances: {str(e)}")