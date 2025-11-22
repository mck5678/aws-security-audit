import boto3
from colorama import Fore, Style
from utils.issue_tracker import add_issue


def check_security_groups():
    """Check security groups for overly permissive rules"""
    print(f"\n{Fore.CYAN}=== Checking Security Groups ==={Style.RESET_ALL}")
    
    try:
        ec2 = boto3.client('ec2')
        security_groups = ec2.describe_security_groups()
        
        if not security_groups['SecurityGroups']:
            print(f"{Fore.YELLOW}No security groups found")
            return
        
        found_issues = False
        
        for sg in security_groups['SecurityGroups']:
            sg_name = sg['GroupName']
            sg_id = sg['GroupId']
            
            has_open_rule = False
            
            for permission in sg.get('IpPermissions', []):
                for ip_range in permission.get('IpRanges', []):
                    cidr = ip_range.get('CidrIp', '')
                    
                    if cidr == '0.0.0.0/0':
                        has_open_rule = True
                        found_issues = True
                        from_port = permission.get('FromPort', 'All')
                        to_port = permission.get('ToPort', 'All')
                        protocol = permission.get('IpProtocol', 'All')
                        
                        if from_port == to_port:
                            port_info = f"port {from_port}"
                        else:
                            port_info = f"ports {from_port}-{to_port}"
                        
                        add_issue('high', f"Security group '{sg_name}' allows {protocol} on {port_info} from ANYWHERE")
                        print(f"{Fore.RED}❌ RISK: Security group '{sg_name}' ({sg_id}) allows {protocol} on {port_info} from ANYWHERE (0.0.0.0/0)")
            
            if not has_open_rule:
                print(f"{Fore.GREEN}✅ Security group '{sg_name}' ({sg_id}) has restricted access")
        
        if not found_issues:
            print(f"{Fore.GREEN}No overly permissive security group rules found!")
                        
    except Exception as e:
        print(f"{Fore.RED}Error checking security groups: {str(e)}")