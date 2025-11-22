import boto3
from colorama import Fore, Style, init
import sys
import argparse

# Import all check functions
from checks.s3_check import check_s3_buckets
from checks.iam_check import check_iam_users
from checks.cloudtrail_check import check_cloudtrail
from checks.ec2_check import check_ec2_instances
from checks.security_groups_check import check_security_groups

# Import utility functions
from utils.report_generator import print_summary, save_report_to_file

# Initialize colorama
init(autoreset=True)


def check_aws_credentials():
    """Verify AWS credentials are configured"""
    try:
        sts = boto3.client('sts')
        sts.get_caller_identity()
        return True
    except Exception as e:
        print(f"{Fore.RED}Error: Unable to connect to AWS")
        print(f"Make sure your AWS credentials are configured.")
        print(f"Error details: {str(e)}")
        return False


def main():
    """Main function to run security audit"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='AWS Security Audit Tool - Scan your AWS account for security issues',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 security_audit.py
  python3 security_audit.py --output my_report.txt
  python3 security_audit.py --region us-west-2 --output custom.txt
        """
    )
    parser.add_argument('--region', type=str, help='AWS region to audit (default: configured region)')
    parser.add_argument('--output', type=str, default='security_audit_report.txt', 
                        help='Output filename for report (default: security_audit_report.txt)')
    args = parser.parse_args()
    
    print(f"{Fore.CYAN}{'='*50}")
    print(f"{Fore.CYAN}AWS Security Audit Tool")
    print(f"{Fore.CYAN}{'='*50}\n")
    
    if not check_aws_credentials():
        sys.exit(1)
    
    # Run all security checks
    check_s3_buckets()
    check_iam_users()
    check_cloudtrail()
    check_ec2_instances()
    check_security_groups()
    
    # Print and save summary
    print_summary()
    save_report_to_file(args.output)
    
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"{Fore.GREEN}✅ Security audit complete!")
    print(f"{Fore.CYAN}{'='*50}")


if __name__ == "__main__":
    main()