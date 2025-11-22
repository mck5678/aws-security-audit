import boto3
from colorama import Fore, Style
from utils.issue_tracker import add_issue


def check_cloudtrail():
    """Check CloudTrail logging status"""
    print(f"\n{Fore.CYAN}=== Checking CloudTrail Logging ==={Style.RESET_ALL}")
    
    try:
        cloudtrail = boto3.client('cloudtrail')
        trails = cloudtrail.describe_trails()
        
        if not trails['trailList']:
            add_issue('critical', "No CloudTrail trails found - logging is DISABLED")
            print(f"{Fore.RED}❌ CRITICAL: No CloudTrail trails found - logging is DISABLED")
            return
        
        for trail in trails['trailList']:
            trail_name = trail['Name']
            
            try:
                status = cloudtrail.get_trail_status(Name=trail['TrailARN'])
                
                if status['IsLogging']:
                    print(f"{Fore.GREEN}✅ SECURE: Trail '{trail_name}' is LOGGING")
                else:
                    add_issue('high', f"CloudTrail trail '{trail_name}' is NOT logging")
                    print(f"{Fore.RED}❌ RISK: Trail '{trail_name}' is NOT logging")
                    
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️  Could not check trail '{trail_name}': {str(e)}")
                
    except Exception as e:
        print(f"{Fore.RED}Error checking CloudTrail: {str(e)}")