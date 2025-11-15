# Wich

**W**e **I**nspect **C**ompliance **H**olistically

A comprehensive 100-point OWASP-focused compliance checker for evaluating open-source security projects.

## Overview

Wich is a powerful tool designed to evaluate software projects against OWASP security standards and best practices. It provides a systematic, quantitative assessment across 10 critical categories:

- **Legal & Licensing** (10 points) - License compliance, OSI approval, copyright notices
- **Documentation** (10 points) - README quality, security policies, contribution guides
- **Code Quality** (10 points) - Linting, formatting, pre-commit hooks, code structure
- **Security** (10 points) - Dependency scanning, secrets protection, secure communications
- **Governance** (10 points) - Code of conduct, issue/PR templates, maintainer lists
- **CI/CD** (10 points) - Automated builds, testing, security scanning, deployments
- **Testing** (10 points) - Unit tests, integration tests, coverage tracking
- **Performance** (10 points) - Benchmarking, optimization, scalability
- **Logging & Monitoring** (10 points) - Logging frameworks, observability, health checks
- **Community Health** (10 points) - Responsible disclosure, support channels, changelogs

## Features

✅ **Comprehensive Evaluation** - 100-point scoring system across 10 categories  
✅ **Detailed Reports** - Clear breakdown of what's working and what needs improvement  
✅ **Multiple Output Formats** - Terminal-friendly or JSON for CI/CD integration  
✅ **Actionable Insights** - Specific recommendations for improvement  
✅ **Language Agnostic** - Works with any programming language or framework  
✅ **Zero Configuration** - Just point it at a repository and run

## Installation

Wich requires Python 3.7 or higher. No additional dependencies needed!

```bash
# Clone the repository
git clone https://github.com/OWASP-BLT/Wich.git
cd Wich

# Make it executable (Unix/Linux/macOS)
chmod +x wich.py

# Run it
./wich.py /path/to/your/project
```

Or run directly with Python:

```bash
python3 wich.py /path/to/your/project
```

## Usage

### Basic Usage

Check the current directory:
```bash
./wich.py .
```

Check a specific repository:
```bash
./wich.py /path/to/repository
```

### Show Detailed Results

Get a detailed breakdown of every check:
```bash
./wich.py /path/to/repository --verbose
```

### JSON Output

Perfect for CI/CD pipelines and automated processing:
```bash
./wich.py /path/to/repository --json
```

### Help

```bash
./wich.py --help
```

## Example Output

```
======================================================================
OWASP PROJECT COMPLIANCE REPORT
======================================================================

Overall Score: 73/100 (73.0%)
Grade: C (Fair)

----------------------------------------------------------------------
CATEGORY BREAKDOWN
----------------------------------------------------------------------
✓ Legal & Licensing                10/10 (100.0%) [4/4 checks passed]
○ Documentation                     7/10 ( 70.0%) [4/5 checks passed]
✗ Code Quality                      4/10 ( 40.0%) [2/5 checks passed]
✓ Security                          8/10 ( 80.0%) [4/5 checks passed]
○ Governance                        5/10 ( 50.0%) [2/5 checks passed]
✓ CI/CD                             9/10 ( 90.0%) [4/5 checks passed]
○ Testing                           7/10 ( 70.0%) [3/5 checks passed]
✗ Performance                       3/10 ( 30.0%) [1/5 checks passed]
○ Logging & Monitoring              5/10 ( 50.0%) [2/5 checks passed]
✓ Community Health                  9/10 ( 90.0%) [4/5 checks passed]

======================================================================
Fair. Several important areas need attention for better security posture.
======================================================================
```

## Grading Scale

- **A (90-100%)**: Excellent! Meets high OWASP security and quality standards
- **B (80-89%)**: Good work! Minor improvements needed
- **C (70-79%)**: Fair. Several areas need attention
- **D (60-69%)**: Poor. Significant improvements required
- **F (<60%)**: Critical. Lacks fundamental security practices

## CI/CD Integration

### GitHub Actions

```yaml
name: OWASP Compliance Check
on: [push, pull_request]

jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Check OWASP Compliance
        run: |
          curl -O https://raw.githubusercontent.com/OWASP-BLT/Wich/main/wich.py
          chmod +x wich.py
          ./wich.py . --verbose
```

### GitLab CI

```yaml
owasp-compliance:
  script:
    - curl -O https://raw.githubusercontent.com/OWASP-BLT/Wich/main/wich.py
    - chmod +x wich.py
    - python3 wich.py . --verbose
  allow_failure: true
```

## What Gets Checked?

<details>
<summary><b>Legal & Licensing (10 points)</b></summary>

- LICENSE file exists (4 pts)
- OSI-approved license (3 pts)
- Copyright notices (2 pts)
- Third-party licenses documented (1 pt)
</details>

<details>
<summary><b>Documentation (10 points)</b></summary>

- README exists (2 pts)
- README quality - installation, usage (3 pts)
- CONTRIBUTING guide (2 pts)
- SECURITY policy (2 pts)
- Additional documentation (1 pt)
</details>

<details>
<summary><b>Code Quality (10 points)</b></summary>

- Linting configuration (3 pts)
- Code formatting config (2 pts)
- .gitignore file (2 pts)
- Pre-commit hooks (2 pts)
- Code structure (1 pt)
</details>

<details>
<summary><b>Security (10 points)</b></summary>

- Dependency scanning (3 pts)
- Secrets protection (2 pts)
- Security contact info (2 pts)
- HTTPS/TLS documentation (1 pt)
- Auth documentation (2 pts)
</details>

<details>
<summary><b>Governance (10 points)</b></summary>

- Code of Conduct (3 pts)
- Issue templates (2 pts)
- PR templates (2 pts)
- Governance docs (2 pts)
- Maintainers list (1 pt)
</details>

<details>
<summary><b>CI/CD (10 points)</b></summary>

- CI configuration (4 pts)
- Automated builds (2 pts)
- Automated tests (2 pts)
- Security scanning (1 pt)
- Deployment automation (1 pt)
</details>

<details>
<summary><b>Testing (10 points)</b></summary>

- Test files present (3 pts)
- Test configuration (2 pts)
- Coverage tracking (2 pts)
- Integration tests (2 pts)
- Testing docs (1 pt)
</details>

<details>
<summary><b>Performance (10 points)</b></summary>

- Performance tests (3 pts)
- Benchmarking tools (2 pts)
- Performance docs (2 pts)
- Caching strategy (2 pts)
- Resource optimization (1 pt)
</details>

<details>
<summary><b>Logging & Monitoring (10 points)</b></summary>

- Logging framework (3 pts)
- Monitoring config (2 pts)
- Error tracking (2 pts)
- Health checks (2 pts)
- Observability docs (1 pt)
</details>

<details>
<summary><b>Community Health (10 points)</b></summary>

- Responsible disclosure (3 pts)
- Contribution guidelines (2 pts)
- Support channels (2 pts)
- Changelog (2 pts)
- Release process (1 pt)
</details>

## Use Cases

- **Before Open Sourcing**: Ensure your project meets industry standards
- **Security Audits**: Quick assessment of security posture
- **Code Reviews**: Systematic evaluation of project health
- **Compliance**: Verify adherence to OWASP guidelines
- **CI/CD Gates**: Automated quality checks in pipelines
- **Project Maturity**: Track improvements over time

## Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) guide (once created) for details.

## Security

For security issues, please see our [SECURITY.md](SECURITY.md) policy (once created).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Developed for the OWASP BLT project to promote security best practices in open-source software.

## Related Projects

- [OWASP BLT](https://github.com/OWASP-BLT) - Bug Logging Tool
- [OWASP SAMM](https://owaspsamm.org/) - Software Assurance Maturity Model
- [OpenSSF Scorecard](https://github.com/ossf/scorecard) - Security health metrics

## Support

- Open an issue on GitHub
- Join the OWASP BLT community

---

Made with ❤️ for the OWASP community
