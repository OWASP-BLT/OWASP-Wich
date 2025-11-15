# Contributing to Wich

Thank you for your interest in contributing to Wich! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Release Process](#release-process)

## Code of Conduct

This project adheres to the OWASP Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Python version)
- **Screenshots** if applicable
- **Error messages** or logs

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When suggesting an enhancement:

- **Use a clear title** describing the enhancement
- **Provide detailed description** of the proposed functionality
- **Explain why** this enhancement would be useful
- **Provide examples** of how it would work

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages** (`git commit -m 'Add amazing feature'`)
6. **Push to your fork** (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Git

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/Wich.git
cd Wich

# Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Make the script executable
chmod +x wich.py

# Test it works
./wich.py --help
```

## Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update README.md** with details of changes if applicable
5. **Update version number** following [Semantic Versioning](https://semver.org/)
6. **Request review** from maintainers

### PR Title Format

Use conventional commit format:

- `feat: Add new security check for X`
- `fix: Correct scoring for Y category`
- `docs: Update installation instructions`
- `test: Add tests for Z functionality`
- `refactor: Simplify check logic`
- `chore: Update dependencies`

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some exceptions:

- **Line length**: 100 characters (not 79)
- **Docstrings**: Required for all public functions/classes
- **Type hints**: Encouraged but not required

### Code Organization

```python
# Standard library imports
import os
import sys

# Third-party imports
# (none currently)

# Local imports
from typing import Dict, List

# Constants
MAX_SCORE = 100

# Classes
class ComplianceChecker:
    pass

# Functions
def main():
    pass
```

### Documentation

- Use docstrings for all public functions and classes
- Include parameter types and return types
- Add inline comments for complex logic
- Update README for user-facing changes

### Example Function

```python
def check_security(self, repo_path: str) -> CheckResult:
    """Check security practices in the repository.
    
    Args:
        repo_path: Path to the repository to check
        
    Returns:
        CheckResult with security assessment
        
    Raises:
        ValueError: If repo_path is invalid
    """
    # Implementation
    pass
```

## Testing Guidelines

### Running Tests

```bash
# Run the tool on itself
./wich.py . --verbose

# Test on sample repositories
./wich.py /path/to/test/repo

# Test JSON output
./wich.py . --json
```

### Manual Testing Checklist

Before submitting a PR, test:

- [ ] Script runs without errors
- [ ] All checks execute correctly
- [ ] Scoring is accurate
- [ ] Verbose output is readable
- [ ] JSON output is valid
- [ ] Works on different repository structures
- [ ] Edge cases handled gracefully

### Adding New Checks

When adding a new check:

1. Identify the appropriate category
2. Implement the check method
3. Add to the category's check function
4. Test with repositories that pass and fail
5. Update documentation
6. Verify scoring totals remain correct

## Release Process

Releases are managed by maintainers following this process:

1. **Version bump** in `wich.py` (`--version` flag)
2. **Update CHANGELOG.md** with changes
3. **Create release tag**: `git tag -a v1.0.0 -m "Release v1.0.0"`
4. **Push tag**: `git push origin v1.0.0`
5. **Create GitHub release** with release notes

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

## Questions?

- Open an issue with the `question` label
- Join the OWASP BLT community discussions
- Check existing documentation and issues

## Recognition

Contributors will be:

- Listed in the project README (if desired)
- Mentioned in release notes
- Added to the contributors graph on GitHub

Thank you for contributing to making open-source projects more secure! 🎉
