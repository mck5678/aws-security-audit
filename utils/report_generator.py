from colorama import Fore, Style
from utils.issue_tracker import issues, get_total_issues, get_risk_level


def print_summary():
    """Print security audit summary to console"""
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"{Fore.CYAN}SECURITY AUDIT SUMMARY")
    print(f"{Fore.CYAN}{'='*50}\n")
    
    total_issues = get_total_issues()
    
    if total_issues == 0:
        print(f"{Fore.GREEN}🎉 EXCELLENT! No security issues found!")
        print(f"{Fore.GREEN}Your AWS environment is secure.\n")
        return
    
    print(f"Total issues found: {total_issues}\n")
    
    if issues['critical']:
        print(f"{Fore.RED}CRITICAL Issues ({len(issues['critical'])}):")
        for issue in issues['critical']:
            print(f"{Fore.RED}  ❌ {issue}")
        print()
    
    if issues['high']:
        print(f"{Fore.RED}HIGH Risk Issues ({len(issues['high'])}):")
        for issue in issues['high']:
            print(f"{Fore.RED}  ⚠️  {issue}")
        print()
    
    if issues['medium']:
        print(f"{Fore.YELLOW}MEDIUM Risk Issues ({len(issues['medium'])}):")
        for issue in issues['medium']:
            print(f"{Fore.YELLOW}  ⚠️  {issue}")
        print()
    
    if issues['low']:
        print(f"{Fore.YELLOW}LOW Risk Issues ({len(issues['low'])}):")
        for issue in issues['low']:
            print(f"{Fore.YELLOW}  ℹ️  {issue}")
        print()
    
    risk_level = get_risk_level()
    risk_color = Fore.RED if risk_level in ['CRITICAL', 'HIGH'] else Fore.YELLOW
    
    print(f"{risk_color}Overall Risk Level: {risk_level}")
    print(f"{Fore.CYAN}{'='*50}\n")


def save_report_to_file(filename='security_audit_report.txt'):
    """Save security audit report to a text file"""
    try:
        with open(filename, 'w') as f:
            f.write("="*50 + "\n")
            f.write("AWS SECURITY AUDIT REPORT\n")
            f.write("="*50 + "\n\n")
            
            total_issues = get_total_issues()
            
            if total_issues == 0:
                f.write("EXCELLENT! No security issues found!\n")
                f.write("Your AWS environment is secure.\n")
            else:
                f.write(f"Total issues found: {total_issues}\n\n")
                
                if issues['critical']:
                    f.write(f"CRITICAL Issues ({len(issues['critical'])}):\n")
                    for issue in issues['critical']:
                        f.write(f"  - {issue}\n")
                    f.write("\n")
                
                if issues['high']:
                    f.write(f"HIGH Risk Issues ({len(issues['high'])}):\n")
                    for issue in issues['high']:
                        f.write(f"  - {issue}\n")
                    f.write("\n")
                
                if issues['medium']:
                    f.write(f"MEDIUM Risk Issues ({len(issues['medium'])}):\n")
                    for issue in issues['medium']:
                        f.write(f"  - {issue}\n")
                    f.write("\n")
                
                if issues['low']:
                    f.write(f"LOW Risk Issues ({len(issues['low'])}):\n")
                    for issue in issues['low']:
                        f.write(f"  - {issue}\n")
                    f.write("\n")
                
                risk_level = get_risk_level()
                f.write(f"Overall Risk Level: {risk_level}\n")
            
            f.write("="*50 + "\n")
        
        print(f"{Fore.GREEN}📄 Report saved to: {filename}")
        
    except Exception as e:
        print(f"{Fore.RED}Error saving report: {str(e)}")