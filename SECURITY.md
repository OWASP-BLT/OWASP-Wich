# Security Policy

## Reporting Security Vulnerabilities

The OWASP BLT team takes security seriously. We appreciate your efforts to responsibly disclose your findings.

### How to Report a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by emailing:

- **Email**: security@owasp.org
- **Subject**: [Wich Security] Brief description of the issue

Please include the following information in your report:

- Type of vulnerability (e.g., XSS, SQL injection, broken authentication)
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### What to Expect

1. **Acknowledgment**: We'll acknowledge receipt of your vulnerability report within 48 hours
2. **Assessment**: We'll assess the vulnerability and determine its severity
3. **Fix**: We'll work on a fix and coordinate a release timeline with you
4. **Disclosure**: We'll publicly disclose the vulnerability after a fix is available
5. **Credit**: We'll credit you in our security advisories (unless you prefer to remain anonymous)

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Security Best Practices

When using Wich:

1. **Keep it Updated**: Always use the latest version
2. **Review Code**: If modifying the tool, review changes for security implications
3. **Safe Repositories**: Only run on repositories you trust
4. **Permissions**: Run with minimal required permissions
5. **CI/CD Security**: Secure your CI/CD pipelines when integrating Wich

## Security Features

Wich helps identify security issues in repositories by checking for:

- Dependency scanning configurations
- Security policies and disclosure practices
- Secure communication protocols
- Authentication and authorization documentation
- Secrets scanning and protection
- Security scanning in CI/CD pipelines

## Responsible Disclosure Timeline

We follow a 90-day disclosure timeline:

1. **Day 0**: Vulnerability reported
2. **Day 1-7**: Assessment and confirmation
3. **Day 8-60**: Fix development and testing
4. **Day 61-90**: Coordinated release and disclosure
5. **Day 90+**: Public disclosure (if not resolved)

## Hall of Fame

We maintain a list of security researchers who have responsibly disclosed vulnerabilities:

- *No vulnerabilities reported yet*

Thank you for helping keep Wich and the OWASP community safe!
