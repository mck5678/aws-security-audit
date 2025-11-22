# AWS Security Audit Tool

A Python tool that scans your AWS account for common security issues and generates a comprehensive report with severity ratings.

## What It Does

This tool checks your AWS infrastructure for security risks and best practices across 5 key areas.

### Features

 **S3 Bucket Security Check**
- Scans all S3 buckets in your account
- Detects publicly accessible buckets
- Shows which buckets are private (secure) vs public (risk)

 **IAM User Permission Audit**
- Checks all IAM users
- Identifies users with administrator access
- Helps enforce least-privilege principle

 **CloudTrail Logging Status**
- Verifies CloudTrail is enabled
- Checks if trails are actively logging
- Critical for security auditing and compliance

 **EC2 Instance Security**
- Scans running instances
- Detects public IP exposure
- Identifies unencrypted EBS volumes

 **Security Group Analysis**
- Examines firewall rules
- Finds overly permissive rules (0.0.0.0/0)
- Highlights potential unauthorized access vectors

### Additional Features

- **Issue Tracking**: Categorizes findings by severity (Critical, High, Medium, Low)
- **Risk Scoring**: Calculates overall risk level
- **Report Export**: Saves detailed reports to text files
- **Command-Line Arguments**: Customizable output filenames
- **Color-Coded Output**: Easy visual identification of issues
- **Modular Architecture**: Organized code structure for maintainability

## Installation

### Requirements
- Python 3.9 or higher
- AWS CLI configured with valid credentials
- IAM permissions to read S3, IAM, CloudTrail, EC2, and Security Groups

### Setup

1. Clone or download this repository
2. Create virtual environment: `python3 -m venv venv` then `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Configure AWS credentials: `aws configure`

## How to Use

**Basic Usage:**
```bash
python3 security_audit.py
```

**Custom Output File:**
```bash
python3 security_audit.py --output my_report.txt
```

**View All Options:**
```bash
python3 security_audit.py --help
```

## Example Output
```
==================================================
AWS Security Audit Tool
==================================================

=== Checking S3 Buckets ===
✅ SECURE: Bucket 'my-bucket' is PRIVATE
❌ RISK: Bucket 'public-bucket' is PUBLIC

=== Checking IAM Users ===
⚠️  WARNING: User 'admin-user' has ADMIN access

=== Checking CloudTrail Logging ===
❌ CRITICAL: No CloudTrail trails found - logging is DISABLED

=== Checking EC2 Instances ===
⚠️  WARNING: Instance 'i-1234567' has PUBLIC IP: 54.123.45.67
❌ RISK: Volume 'vol-abc123' is NOT ENCRYPTED

=== Checking Security Groups ===
❌ RISK: Security group 'web-sg' allows tcp on port 22 from ANYWHERE (0.0.0.0/0)

==================================================
SECURITY AUDIT SUMMARY
==================================================

Total issues found: 5

CRITICAL Issues (1):
  ❌ No CloudTrail trails found - logging is DISABLED

HIGH Risk Issues (3):
  ⚠️  S3 bucket 'public-bucket' is PUBLIC
  ⚠️  EBS volume 'vol-abc123' is NOT ENCRYPTED
  ⚠️  Security group 'web-sg' allows tcp on port 22 from ANYWHERE

MEDIUM Risk Issues (1):
  ⚠️  IAM user 'admin-user' has ADMIN access

Overall Risk Level: CRITICAL
==================================================

📄 Report saved to: security_audit_report.txt

==================================================
✅ Security audit complete!
==================================================
```

## Project Structure

- **security_audit.py** - Main entry point
- **checks/** - Security check modules
  - __init__.py
  - s3_check.py - S3 bucket security checks
  - iam_check.py - IAM user permission checks
  - cloudtrail_check.py - CloudTrail logging checks
  - ec2_check.py - EC2 instance security checks
  - security_groups_check.py - Security group rule checks
- **utils/** - Utility modules
  - __init__.py
  - issue_tracker.py - Issue tracking system with severity levels
  - report_generator.py - Report generation and file export
- **requirements.txt** - Python dependencies

## Technologies Used

- **Python 3.9+**: Core programming language
- **Boto3**: AWS SDK for Python
- **Colorama**: Terminal color formatting
- **Argparse**: Command-line argument parsing

## What I Learned

This project helped me understand:
- AWS security best practices and common vulnerabilities
- Python modular code organization and package structure
- Working with AWS APIs using Boto3
- Building professional command-line tools
- Error handling and user-friendly output design

## Purpose

The purpose of this project was to learn AWS security best practices, understand common cloud vulnerabilities, and build practical Python automation tools. This security audit tool demonstrates real-world application of AWS APIs and modular code architecture that can be extended for additional security checks.

This project is free to use, extend, or modify.
