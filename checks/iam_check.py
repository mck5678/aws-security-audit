import boto3
from colorama import Fore, Style
from utils.issue_tracker import add_issue


def check_iam_users():
    """Check IAM users for excessive permissions"""
    print(f"\n{Fore.CYAN}=== Checking IAM Users ==={Style.RESET_ALL}")
    
    try:
        iam = boto3.client('iam')
        users = iam.list_users()
        
        if not users['Users']:
            print(f"{Fore.YELLOW}No IAM users found")
            return
        
        for user in users['Users']:
            username = user['UserName']
            
            try:
                attached_policies = iam.list_attached_user_policies(UserName=username)
                
                has_admin = False
                for policy in attached_policies['AttachedPolicies']:
                    if 'Administrator' in policy['PolicyName'] or policy['PolicyArn'].endswith('AdministratorAccess'):
                        has_admin = True
                        break
                
                if has_admin:
                    add_issue('medium', f"IAM user '{username}' has ADMIN access")
                    print(f"{Fore.RED}⚠️  WARNING: User '{username}' has ADMIN access")
                else:
                    print(f"{Fore.GREEN}✅ User '{username}' has limited permissions")
                    
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️  Could not check user '{username}': {str(e)}")
                
    except Exception as e:
        print(f"{Fore.RED}Error checking IAM users: {str(e)}")