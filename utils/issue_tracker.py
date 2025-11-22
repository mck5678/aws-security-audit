# Global variables to track issues
issues = {
    'critical': [],
    'high': [],
    'medium': [],
    'low': []
}


def add_issue(severity, message):
    """Add a security issue to the tracker"""
    issues[severity].append(message)


def get_total_issues():
    """Get total count of all issues"""
    return sum(len(issues[severity]) for severity in issues)


def get_risk_level():
    """Calculate overall risk level based on issues found"""
    if issues['critical']:
        return 'CRITICAL'
    elif issues['high']:
        return 'HIGH'
    elif issues['medium']:
        return 'MEDIUM'
    elif issues['low']:
        return 'LOW'
    else:
        return 'NONE'


def reset_issues():
    """Clear all tracked issues"""
    for severity in issues:
        issues[severity] = []