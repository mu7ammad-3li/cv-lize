"""
PDF Security Validator
Implements multi-layer PDF validation to prevent malicious file uploads
"""

import re
import hashlib
from typing import Dict, List, Tuple
from io import BytesIO


class PDFSecurityValidator:
    """Validates PDFs for security threats including reverse shells and malicious content"""

    # PDF magic bytes
    PDF_MAGIC_BYTES = b'%PDF'

    # Malicious pattern definitions
    JAVASCRIPT_PATTERNS = [
        rb'/JavaScript\s',
        rb'/JS\s',
        rb'/AA\s',  # Additional Actions (auto-execute)
        rb'/OpenAction\s',  # Execute on document open
        rb'/RichMedia\s',  # Rich media (Flash, etc.)
        rb'eval\s*\(',
        rb'replace\s*\(',
        rb'unescape\s*\(',
        rb'String\.fromCharCode',
        rb'/AcroForm\s'  # Interactive forms with scripts
    ]

    EMBEDDED_FILE_PATTERNS = [
        rb'/EmbeddedFile\s',
        rb'/Launch\s',  # File execution action
        rb'/ObjStm\s',  # Object streams (can hide content)
    ]

    REMOTE_ACCESS_PATTERNS = [
        rb'/GoToR\s',  # Go to remote (SMB credential harvesting)
    ]

    XFA_PATTERNS = [
        rb'/XFA\s',  # XFA forms (XML-based, can be exploited)
    ]

    # Reverse shell patterns
    REVERSE_SHELL_PATTERNS = [
        # Bash reverse shells
        (rb'bash\s+-i\s+>&\s*/dev/(tcp|udp)', 'Bash interactive reverse shell'),
        (rb'/dev/(tcp|udp)/[\d\.\w\-:]+', 'Dev socket connection'),

        # Python reverse shells
        (rb'python\s+-c\s+.*import\s+socket', 'Python reverse shell'),
        (rb'socket\.socket\s*\(\s*socket\.AF_INET', 'Python TCP socket'),
        (rb'os\.system\s*\(\s*[\'"].*bash', 'Python OS system call'),

        # Socat
        (rb'socat\s+exec', 'Socat execution'),
        (rb'socat.*TCP', 'Socat TCP connection'),

        # Netcat variants
        (rb'nc\s+[-nlvp].*bash', 'Netcat backdoor'),
        (rb'nc\s+.*-e\s+/bin/(bash|sh)', 'Netcat execution'),

        # Perl
        (rb'perl\s+.*socket', 'Perl socket'),

        # PHP
        (rb'php.*socket_create', 'PHP socket creation'),
        (rb'fsockopen', 'PHP fsockopen'),

        # PowerShell
        (rb'powershell.*TCPClient', 'PowerShell TCP client'),
        (rb'powershell\s+.*-NoP\s+-NonI\s+-W\s+Hidden', 'PowerShell hidden execution'),

        # Java
        (rb'java\.net\.Socket', 'Java socket'),

        # Ruby
        (rb'require\s+[\'"]socket[\'"]', 'Ruby socket'),

        # Interactive shell indicators
        (rb'bash\s+-i|sh\s+-i', 'Interactive shell flag'),
    ]

    def __init__(self):
        self.issues: List[Dict] = []

    def validate_file_signature(self, content: bytes) -> bool:
        """Validate PDF magic bytes"""
        if not content.startswith(self.PDF_MAGIC_BYTES):
            self.issues.append({
                'type': 'INVALID_SIGNATURE',
                'severity': 'CRITICAL',
                'message': 'File does not have valid PDF signature'
            })
            return False
        return True

    def scan_for_javascript(self, content: bytes) -> List[Dict]:
        """Scan for embedded JavaScript"""
        found_issues = []

        for pattern in self.JAVASCRIPT_PATTERNS:
            if re.search(pattern, content):
                found_issues.append({
                    'type': 'JAVASCRIPT_DETECTED',
                    'severity': 'HIGH',
                    'message': f'JavaScript pattern detected: {pattern.decode("utf-8", errors="ignore")}'
                })

        return found_issues

    def scan_for_embedded_files(self, content: bytes) -> List[Dict]:
        """Scan for embedded files and executables"""
        found_issues = []

        for pattern in self.EMBEDDED_FILE_PATTERNS:
            if re.search(pattern, content):
                found_issues.append({
                    'type': 'EMBEDDED_FILE',
                    'severity': 'CRITICAL',
                    'message': f'Embedded file pattern detected: {pattern.decode("utf-8", errors="ignore")}'
                })

        return found_issues

    def scan_for_remote_access(self, content: bytes) -> List[Dict]:
        """Scan for remote file access (SMB attacks)"""
        found_issues = []

        for pattern in self.REMOTE_ACCESS_PATTERNS:
            if re.search(pattern, content):
                found_issues.append({
                    'type': 'REMOTE_ACCESS',
                    'severity': 'CRITICAL',
                    'message': 'Remote file redirect detected (potential SMB attack)'
                })

        return found_issues

    def scan_for_xfa_forms(self, content: bytes) -> List[Dict]:
        """Scan for XFA forms"""
        found_issues = []

        for pattern in self.XFA_PATTERNS:
            if re.search(pattern, content):
                found_issues.append({
                    'type': 'XFA_FORM',
                    'severity': 'HIGH',
                    'message': 'XFA form detected (potential XXE vulnerability)'
                })

        return found_issues

    def scan_for_reverse_shells(self, content: bytes) -> List[Dict]:
        """Scan for reverse shell patterns"""
        found_issues = []

        for pattern, description in self.REVERSE_SHELL_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                found_issues.append({
                    'type': 'REVERSE_SHELL',
                    'severity': 'CRITICAL',
                    'message': f'Reverse shell pattern detected: {description}'
                })

        return found_issues

    def calculate_file_hash(self, content: bytes) -> str:
        """Calculate SHA-256 hash of file"""
        return hashlib.sha256(content).hexdigest()

    def validate(self, content: bytes) -> Tuple[bool, List[Dict], str]:
        """
        Main validation method

        Returns:
            Tuple of (is_valid, issues, file_hash)
        """
        self.issues = []

        # Calculate hash first
        file_hash = self.calculate_file_hash(content)

        # Layer 1: File signature validation
        if not self.validate_file_signature(content):
            return False, self.issues, file_hash

        # Layer 2: Scan for malicious content
        self.issues.extend(self.scan_for_javascript(content))
        self.issues.extend(self.scan_for_embedded_files(content))
        self.issues.extend(self.scan_for_remote_access(content))
        self.issues.extend(self.scan_for_xfa_forms(content))

        # Layer 3: Scan for reverse shells (CRITICAL)
        self.issues.extend(self.scan_for_reverse_shells(content))

        # Determine if valid (no issues)
        is_valid = len(self.issues) == 0

        return is_valid, self.issues, file_hash

    def get_risk_level(self, issues: List[Dict]) -> str:
        """Calculate overall risk level based on issues"""
        if not issues:
            return 'SAFE'

        severity_counts = {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0
        }

        for issue in issues:
            severity = issue.get('severity', 'LOW')
            if severity in severity_counts:
                severity_counts[severity] += 1

        if severity_counts['CRITICAL'] > 0:
            return 'CRITICAL'
        elif severity_counts['HIGH'] > 2:
            return 'HIGH'
        elif severity_counts['HIGH'] > 0:
            return 'MEDIUM'
        else:
            return 'LOW'


# Create singleton instance
pdf_validator = PDFSecurityValidator()
