import boto3
from colorama import Fore, Style
from utils.issue_tracker import add_issue


def check_s3_buckets():
    """Check S3 buckets for public access"""
    print(f"\n{Fore.CYAN}=== Checking S3 Buckets ==={Style.RESET_ALL}")
    
    try:
        s3 = boto3.client('s3')
        buckets = s3.list_buckets()
        
        if not buckets['Buckets']:
            print(f"{Fore.YELLOW}No S3 buckets found")
            return
        
        for bucket in buckets['Buckets']:
            bucket_name = bucket['Name']
            
            try:
                acl = s3.get_bucket_acl(Bucket=bucket_name)
                
                is_public = False
                for grant in acl['Grants']:
                    grantee = grant.get('Grantee', {})
                    if grantee.get('Type') == 'Group':
                        uri = grantee.get('URI', '')
                        if 'AllUsers' in uri or 'AuthenticatedUsers' in uri:
                            is_public = True
                            break
                
                if is_public:
                    add_issue('high', f"S3 bucket '{bucket_name}' is PUBLIC")
                    print(f"{Fore.RED}❌ RISK: Bucket '{bucket_name}' is PUBLIC")
                else:
                    print(f"{Fore.GREEN}✅ SECURE: Bucket '{bucket_name}' is PRIVATE")
                    
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️  Could not check bucket '{bucket_name}': {str(e)}")
                
    except Exception as e:
        print(f"{Fore.RED}Error checking S3 buckets: {str(e)}")