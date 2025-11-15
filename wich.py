#!/usr/bin/env python3
"""
Wich - OWASP Project Compliance Checker

A 100-point OWASP-focused compliance checker evaluating security, documentation,
code quality, governance, CI/CD, testing, performance, logging, community health,
and legal standards.
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict


@dataclass
class CheckResult:
    """Result of a single compliance check."""
    name: str
    passed: bool
    score: int
    max_score: int
    message: str
    category: str


@dataclass
class ComplianceReport:
    """Complete compliance report."""
    total_score: int
    max_score: int
    percentage: float
    checks: List[CheckResult]
    summary: Dict[str, Dict[str, int]]


class ComplianceChecker:
    """OWASP Project Compliance Checker."""
    
    def __init__(self, repo_path: str):
        """Initialize the compliance checker.
        
        Args:
            repo_path: Path to the repository to check
        """
        self.repo_path = Path(repo_path).resolve()
        if not self.repo_path.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")
        
        self.checks: List[CheckResult] = []
        self.categories = {
            "Legal & Licensing": 10,
            "Documentation": 10,
            "Code Quality": 10,
            "Security": 10,
            "Governance": 10,
            "CI/CD": 10,
            "Testing": 10,
            "Performance": 10,
            "Logging & Monitoring": 10,
            "Community Health": 10
        }
    
    def run_all_checks(self) -> ComplianceReport:
        """Run all compliance checks and generate a report.
        
        Returns:
            ComplianceReport with results
        """
        self.checks = []
        
        # Run checks by category
        self._check_legal_licensing()
        self._check_documentation()
        self._check_code_quality()
        self._check_security()
        self._check_governance()
        self._check_cicd()
        self._check_testing()
        self._check_performance()
        self._check_logging_monitoring()
        self._check_community_health()
        
        return self._generate_report()
    
    def _add_check(self, category: str, name: str, passed: bool, 
                   score: int, max_score: int, message: str):
        """Add a check result."""
        self.checks.append(CheckResult(
            name=name,
            passed=passed,
            score=score if passed else 0,
            max_score=max_score,
            message=message,
            category=category
        ))
    
    def _file_exists(self, *paths: str) -> Optional[Path]:
        """Check if any of the given file paths exist (case-insensitive).
        
        Returns:
            Path object if found, None otherwise
        """
        for path in paths:
            # Try exact match first
            full_path = self.repo_path / path
            if full_path.exists():
                return full_path
            
            # Try case-insensitive search in parent directory
            try:
                parent = self.repo_path / Path(path).parent
                filename = Path(path).name.lower()
                if parent.exists():
                    for item in parent.iterdir():
                        if item.name.lower() == filename:
                            return item
            except Exception:
                pass
        
        return None
    
    def _file_contains(self, file_path: Path, patterns: List[str]) -> bool:
        """Check if file contains any of the given patterns (case-insensitive).
        
        Args:
            file_path: Path to the file
            patterns: List of patterns to search for
            
        Returns:
            True if any pattern is found
        """
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore').lower()
            return any(pattern.lower() in content for pattern in patterns)
        except Exception:
            return False
    
    def _count_files_with_extension(self, extensions: List[str]) -> int:
        """Count files with given extensions in the repository.
        
        Args:
            extensions: List of file extensions (e.g., ['.py', '.js'])
            
        Returns:
            Count of matching files
        """
        count = 0
        try:
            for ext in extensions:
                count += len(list(self.repo_path.rglob(f"*{ext}")))
        except Exception:
            pass
        return count
    
    # Legal & Licensing Checks (10 points)
    def _check_legal_licensing(self):
        """Check legal and licensing compliance."""
        category = "Legal & Licensing"
        
        # Check 1: LICENSE file exists (4 points)
        license_file = self._file_exists("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING")
        self._add_check(
            category, "LICENSE File",
            license_file is not None, 4, 4,
            f"LICENSE file {'found' if license_file else 'not found'}"
        )
        
        # Check 2: OSI-approved license (3 points)
        osi_approved = False
        if license_file:
            osi_licenses = [
                "MIT", "Apache", "GPL", "BSD", "ISC", "MPL",
                "LGPL", "AGPL", "EPL", "Creative Commons"
            ]
            osi_approved = self._file_contains(license_file, osi_licenses)
        
        self._add_check(
            category, "OSI-Approved License",
            osi_approved, 3, 3,
            f"OSI-approved license {'detected' if osi_approved else 'not detected'}"
        )
        
        # Check 3: Copyright notices (2 points)
        copyright_found = False
        if license_file:
            copyright_found = self._file_contains(license_file, ["copyright", "©"])
        
        self._add_check(
            category, "Copyright Notices",
            copyright_found, 2, 2,
            f"Copyright notices {'found' if copyright_found else 'not found'}"
        )
        
        # Check 4: Third-party licenses documented (1 point)
        third_party = self._file_exists(
            "THIRD_PARTY_LICENSES", "THIRD_PARTY_LICENSES.md",
            "NOTICE", "NOTICE.txt", "ATTRIBUTION.md"
        )
        self._add_check(
            category, "Third-Party Licenses",
            third_party is not None, 1, 1,
            f"Third-party license documentation {'found' if third_party else 'not found'}"
        )
    
    # Documentation Checks (10 points)
    def _check_documentation(self):
        """Check documentation quality."""
        category = "Documentation"
        
        # Check 1: README exists (2 points)
        readme = self._file_exists("README.md", "README.rst", "README.txt", "README")
        self._add_check(
            category, "README File",
            readme is not None, 2, 2,
            f"README file {'found' if readme else 'not found'}"
        )
        
        # Check 2: README quality (3 points)
        readme_quality = 0
        if readme:
            content = readme.read_text(encoding='utf-8', errors='ignore')
            if len(content) > 500:  # Substantial content
                readme_quality += 1
            if any(section in content.lower() for section in ["installation", "install", "getting started"]):
                readme_quality += 1
            if any(section in content.lower() for section in ["usage", "example", "how to"]):
                readme_quality += 1
        
        self._add_check(
            category, "README Quality",
            readme_quality > 0, readme_quality, 3,
            f"README quality score: {readme_quality}/3"
        )
        
        # Check 3: CONTRIBUTING guide (2 points)
        contributing = self._file_exists(
            "CONTRIBUTING.md", "CONTRIBUTING.rst", "CONTRIBUTING.txt",
            ".github/CONTRIBUTING.md", "docs/CONTRIBUTING.md"
        )
        self._add_check(
            category, "Contributing Guide",
            contributing is not None, 2, 2,
            f"CONTRIBUTING guide {'found' if contributing else 'not found'}"
        )
        
        # Check 4: Security policy (2 points)
        security = self._file_exists(
            "SECURITY.md", "SECURITY.rst", "SECURITY.txt",
            ".github/SECURITY.md", "docs/SECURITY.md"
        )
        self._add_check(
            category, "Security Policy",
            security is not None, 2, 2,
            f"SECURITY.md {'found' if security else 'not found'}"
        )
        
        # Check 5: API/Code documentation (1 point)
        docs_exist = self._file_exists("docs", "documentation", "doc") or \
                     self._count_files_with_extension([".md"]) > 2
        self._add_check(
            category, "Additional Documentation",
            docs_exist, 1, 1,
            f"Additional documentation {'found' if docs_exist else 'not found'}"
        )
    
    # Code Quality Checks (10 points)
    def _check_code_quality(self):
        """Check code quality standards."""
        category = "Code Quality"
        
        # Check 1: Linting configuration (3 points)
        linting_configs = [
            ".eslintrc", ".eslintrc.js", ".eslintrc.json", ".eslintrc.yml",
            ".pylintrc", "pylint.cfg", "setup.cfg", ".flake8",
            ".rubocop.yml", "tslint.json", ".golangci.yml",
            "pyproject.toml"  # Can contain linting config
        ]
        linting = self._file_exists(*linting_configs)
        self._add_check(
            category, "Linting Configuration",
            linting is not None, 3, 3,
            f"Linting config {'found' if linting else 'not found'}"
        )
        
        # Check 2: Code formatting config (2 points)
        formatting_configs = [
            ".prettierrc", ".prettierrc.js", ".prettierrc.json",
            ".editorconfig", ".clang-format", "pyproject.toml",
            ".black", "rustfmt.toml"
        ]
        formatting = self._file_exists(*formatting_configs)
        self._add_check(
            category, "Code Formatting Config",
            formatting is not None, 2, 2,
            f"Formatting config {'found' if formatting else 'not found'}"
        )
        
        # Check 3: .gitignore present (2 points)
        gitignore = self._file_exists(".gitignore")
        gitignore_quality = 0
        if gitignore:
            content = gitignore.read_text(encoding='utf-8', errors='ignore')
            gitignore_quality = 2 if len(content) > 50 else 1
        
        self._add_check(
            category, ".gitignore File",
            gitignore is not None, gitignore_quality, 2,
            f".gitignore {'found with good content' if gitignore_quality == 2 else 'found' if gitignore_quality == 1 else 'not found'}"
        )
        
        # Check 4: Pre-commit hooks (2 points)
        precommit = self._file_exists(".pre-commit-config.yaml", ".pre-commit-config.yml")
        self._add_check(
            category, "Pre-commit Hooks",
            precommit is not None, 2, 2,
            f"Pre-commit hooks {'configured' if precommit else 'not configured'}"
        )
        
        # Check 5: Code has reasonable structure (1 point)
        has_structure = (
            self._file_exists("src") or 
            self._file_exists("lib") or
            self._count_files_with_extension([".py", ".js", ".java", ".go", ".rs"]) > 0
        )
        self._add_check(
            category, "Code Structure",
            has_structure, 1, 1,
            f"Code structure {'present' if has_structure else 'not detected'}"
        )
    
    # Security Checks (10 points)
    def _check_security(self):
        """Check security practices."""
        category = "Security"
        
        # Check 1: Dependency scanning (3 points)
        dep_scanning = self._file_exists(
            "Dependabot.yml", ".github/dependabot.yml",
            "renovate.json", ".renovaterc", "snyk.json"
        )
        self._add_check(
            category, "Dependency Scanning",
            dep_scanning is not None, 3, 3,
            f"Dependency scanning {'configured' if dep_scanning else 'not configured'}"
        )
        
        # Check 2: Secrets scanning prevention (2 points)
        secrets_protection = self._file_exists(
            ".gitguardian.yml", ".gitleaks.toml",
            ".pre-commit-config.yaml"  # Often includes secret scanning
        )
        self._add_check(
            category, "Secrets Protection",
            secrets_protection is not None, 2, 2,
            f"Secrets scanning {'configured' if secrets_protection else 'not configured'}"
        )
        
        # Check 3: Security policy (covered in docs but worth 2 here)
        security_md = self._file_exists("SECURITY.md", ".github/SECURITY.md")
        security_contact = False
        if security_md:
            security_contact = self._file_contains(
                security_md,
                ["report", "vulnerability", "security@", "contact", "disclose"]
            )
        
        self._add_check(
            category, "Security Contact Info",
            security_contact, 2, 2,
            f"Security reporting info {'found' if security_contact else 'not found'}"
        )
        
        # Check 4: HTTPS/TLS requirements documented (1 point)
        https_mentioned = False
        readme = self._file_exists("README.md")
        if readme:
            https_mentioned = self._file_contains(
                readme, ["https://", "TLS", "SSL", "secure"]
            )
        
        self._add_check(
            category, "Secure Communication",
            https_mentioned, 1, 1,
            f"Secure communication {'mentioned' if https_mentioned else 'not mentioned'}"
        )
        
        # Check 5: Authentication/Authorization mentioned (2 points)
        auth_docs = False
        if readme:
            auth_docs = self._file_contains(
                readme,
                ["authentication", "authorization", "auth", "OAuth", "JWT", "API key"]
            )
        
        self._add_check(
            category, "Auth Documentation",
            auth_docs, 2, 2,
            f"Authentication/Authorization {'documented' if auth_docs else 'not documented'}"
        )
    
    # Governance Checks (10 points)
    def _check_governance(self):
        """Check governance and community standards."""
        category = "Governance"
        
        # Check 1: Code of Conduct (3 points)
        coc = self._file_exists(
            "CODE_OF_CONDUCT.md", "CODE_OF_CONDUCT.rst",
            ".github/CODE_OF_CONDUCT.md", "docs/CODE_OF_CONDUCT.md"
        )
        self._add_check(
            category, "Code of Conduct",
            coc is not None, 3, 3,
            f"Code of Conduct {'found' if coc else 'not found'}"
        )
        
        # Check 2: Issue templates (2 points)
        issue_templates = self._file_exists(
            ".github/ISSUE_TEMPLATE", ".github/ISSUE_TEMPLATE.md",
            ".gitlab/issue_templates"
        )
        self._add_check(
            category, "Issue Templates",
            issue_templates is not None, 2, 2,
            f"Issue templates {'found' if issue_templates else 'not found'}"
        )
        
        # Check 3: PR templates (2 points)
        pr_templates = self._file_exists(
            ".github/PULL_REQUEST_TEMPLATE.md",
            ".github/pull_request_template.md",
            ".gitlab/merge_request_templates"
        )
        self._add_check(
            category, "PR Templates",
            pr_templates is not None, 2, 2,
            f"PR templates {'found' if pr_templates else 'not found'}"
        )
        
        # Check 4: Governance documentation (2 points)
        governance = self._file_exists(
            "GOVERNANCE.md", "GOVERNANCE.rst",
            ".github/GOVERNANCE.md", "docs/GOVERNANCE.md"
        )
        self._add_check(
            category, "Governance Documentation",
            governance is not None, 2, 2,
            f"Governance docs {'found' if governance else 'not found'}"
        )
        
        # Check 5: Maintainers file (1 point)
        maintainers = self._file_exists(
            "MAINTAINERS.md", "MAINTAINERS", "CODEOWNERS",
            ".github/CODEOWNERS", "OWNERS"
        )
        self._add_check(
            category, "Maintainers List",
            maintainers is not None, 1, 1,
            f"Maintainers list {'found' if maintainers else 'not found'}"
        )
    
    # CI/CD Checks (10 points)
    def _check_cicd(self):
        """Check CI/CD configuration."""
        category = "CI/CD"
        
        # Check 1: CI configuration exists (4 points)
        ci_configs = [
            ".github/workflows", ".gitlab-ci.yml", "azure-pipelines.yml",
            "Jenkinsfile", ".travis.yml", ".circleci/config.yml",
            "bitbucket-pipelines.yml", ".drone.yml"
        ]
        ci_config = self._file_exists(*ci_configs)
        self._add_check(
            category, "CI Configuration",
            ci_config is not None, 4, 4,
            f"CI configuration {'found' if ci_config else 'not found'}"
        )
        
        # Check 2: Automated builds (2 points)
        has_build = False
        if ci_config and ci_config.is_dir():
            # Check workflow files for build steps
            for workflow in ci_config.glob("*.yml"):
                if self._file_contains(workflow, ["build", "compile", "make"]):
                    has_build = True
                    break
        elif ci_config:
            has_build = self._file_contains(ci_config, ["build", "compile", "make"])
        
        self._add_check(
            category, "Automated Builds",
            has_build, 2, 2,
            f"Automated builds {'configured' if has_build else 'not configured'}"
        )
        
        # Check 3: Automated tests in CI (2 points)
        has_tests = False
        if ci_config and ci_config.is_dir():
            for workflow in ci_config.glob("*.yml"):
                if self._file_contains(workflow, ["test", "pytest", "jest", "junit", "maven test"]):
                    has_tests = True
                    break
        elif ci_config:
            has_tests = self._file_contains(ci_config, ["test", "pytest", "jest", "junit"])
        
        self._add_check(
            category, "Automated Testing",
            has_tests, 2, 2,
            f"Automated testing {'configured' if has_tests else 'not configured'}"
        )
        
        # Check 4: Security scanning in CI (1 point)
        has_security_scan = False
        if ci_config and ci_config.is_dir():
            for workflow in ci_config.glob("*.yml"):
                if self._file_contains(
                    workflow,
                    ["security", "snyk", "trivy", "bandit", "safety", "codeql"]
                ):
                    has_security_scan = True
                    break
        elif ci_config:
            has_security_scan = self._file_contains(
                ci_config, ["security", "snyk", "trivy", "bandit"]
            )
        
        self._add_check(
            category, "Security Scanning",
            has_security_scan, 1, 1,
            f"Security scanning {'configured' if has_security_scan else 'not configured'}"
        )
        
        # Check 5: Deployment automation (1 point)
        has_deploy = False
        if ci_config and ci_config.is_dir():
            for workflow in ci_config.glob("*.yml"):
                if self._file_contains(workflow, ["deploy", "release", "publish"]):
                    has_deploy = True
                    break
        elif ci_config:
            has_deploy = self._file_contains(ci_config, ["deploy", "release", "publish"])
        
        self._add_check(
            category, "Deployment Automation",
            has_deploy, 1, 1,
            f"Deployment automation {'configured' if has_deploy else 'not configured'}"
        )
    
    # Testing Checks (10 points)
    def _check_testing(self):
        """Check testing practices."""
        category = "Testing"
        
        # Check 1: Test files exist (3 points)
        test_dirs = self._file_exists("tests", "test", "__tests__", "spec")
        test_files = (
            self._count_files_with_extension(["_test.py", "_test.go"]) > 0 or
            self._count_files_with_extension([".test.js", ".test.ts"]) > 0 or
            self._count_files_with_extension([".spec.js", ".spec.ts"]) > 0
        )
        has_tests = test_dirs or test_files
        
        self._add_check(
            category, "Test Files Present",
            has_tests, 3, 3,
            f"Test files {'found' if has_tests else 'not found'}"
        )
        
        # Check 2: Test configuration (2 points)
        test_configs = [
            "pytest.ini", "tox.ini", "jest.config.js", "karma.conf.js",
            "phpunit.xml", "go.mod", "package.json"  # package.json often has test scripts
        ]
        test_config = self._file_exists(*test_configs)
        self._add_check(
            category, "Test Configuration",
            test_config is not None, 2, 2,
            f"Test configuration {'found' if test_config else 'not found'}"
        )
        
        # Check 3: Coverage configuration (2 points)
        coverage_configs = [
            ".coveragerc", "coverage.xml", ".coverage",
            "jest.config.js", "codecov.yml", ".codecov.yml"
        ]
        coverage_config = self._file_exists(*coverage_configs)
        self._add_check(
            category, "Coverage Tracking",
            coverage_config is not None, 2, 2,
            f"Coverage tracking {'configured' if coverage_config else 'not configured'}"
        )
        
        # Check 4: Integration/E2E tests (2 points)
        integration_tests = (
            self._file_exists("tests/integration", "tests/e2e", "e2e") or
            self._count_files_with_extension([".integration.test.js", ".e2e.test.js"]) > 0
        )
        self._add_check(
            category, "Integration Tests",
            integration_tests, 2, 2,
            f"Integration tests {'found' if integration_tests else 'not found'}"
        )
        
        # Check 5: Test documentation (1 point)
        test_docs = False
        readme = self._file_exists("README.md")
        if readme:
            test_docs = self._file_contains(readme, ["test", "testing", "pytest", "jest"])
        
        self._add_check(
            category, "Testing Documentation",
            test_docs, 1, 1,
            f"Testing documentation {'found' if test_docs else 'not found'}"
        )
    
    # Performance Checks (10 points)
    def _check_performance(self):
        """Check performance and scalability considerations."""
        category = "Performance"
        
        # Check 1: Performance tests exist (3 points)
        perf_tests = self._file_exists(
            "tests/performance", "tests/perf", "benchmarks",
            "performance"
        ) or self._count_files_with_extension([".bench.js", "_bench.py"]) > 0
        
        self._add_check(
            category, "Performance Tests",
            perf_tests, 3, 3,
            f"Performance tests {'found' if perf_tests else 'not found'}"
        )
        
        # Check 2: Benchmarking configuration (2 points)
        benchmark_configs = [
            "benchmark", ".benchmarkrc", "k6.js", "locust.py",
            "artillery.yml", "jmeter.jmx"
        ]
        benchmark_config = self._file_exists(*benchmark_configs)
        self._add_check(
            category, "Benchmarking Tools",
            benchmark_config is not None, 2, 2,
            f"Benchmarking {'configured' if benchmark_config else 'not configured'}"
        )
        
        # Check 3: Performance documentation (2 points)
        perf_docs = False
        readme = self._file_exists("README.md")
        if readme:
            perf_docs = self._file_contains(
                readme,
                ["performance", "scalability", "optimization", "benchmark"]
            )
        
        self._add_check(
            category, "Performance Documentation",
            perf_docs, 2, 2,
            f"Performance docs {'found' if perf_docs else 'not found'}"
        )
        
        # Check 4: Caching strategy (2 points)
        has_caching = False
        if readme:
            has_caching = self._file_contains(
                readme, ["cache", "caching", "redis", "memcached"]
            )
        
        self._add_check(
            category, "Caching Strategy",
            has_caching, 2, 2,
            f"Caching strategy {'documented' if has_caching else 'not documented'}"
        )
        
        # Check 5: Resource optimization (1 point)
        has_optimization = self._file_exists(
            "Dockerfile", "docker-compose.yml",
            ".dockerignore", "kubernetes", "k8s"
        )
        self._add_check(
            category, "Resource Optimization",
            has_optimization is not None, 1, 1,
            f"Resource optimization {'configured' if has_optimization else 'not configured'}"
        )
    
    # Logging & Monitoring Checks (10 points)
    def _check_logging_monitoring(self):
        """Check logging and monitoring practices."""
        category = "Logging & Monitoring"
        
        # Check 1: Logging framework (3 points)
        has_logging = False
        source_files = list(self.repo_path.rglob("*.py")) + \
                      list(self.repo_path.rglob("*.js")) + \
                      list(self.repo_path.rglob("*.java"))
        
        for source_file in source_files[:10]:  # Check first 10 files
            if self._file_contains(
                source_file,
                ["import logging", "logger", "console.log", "log4j", "winston"]
            ):
                has_logging = True
                break
        
        self._add_check(
            category, "Logging Framework",
            has_logging, 3, 3,
            f"Logging framework {'detected' if has_logging else 'not detected'}"
        )
        
        # Check 2: Monitoring configuration (2 points)
        monitoring_configs = [
            "prometheus.yml", "grafana", "datadog.yml",
            "newrelic.yml", ".elasticapm.yml"
        ]
        monitoring = self._file_exists(*monitoring_configs)
        self._add_check(
            category, "Monitoring Configuration",
            monitoring is not None, 2, 2,
            f"Monitoring {'configured' if monitoring else 'not configured'}"
        )
        
        # Check 3: Error tracking (2 points)
        error_tracking = False
        if readme := self._file_exists("README.md"):
            error_tracking = self._file_contains(
                readme,
                ["sentry", "rollbar", "bugsnag", "error tracking", "error reporting"]
            )
        
        self._add_check(
            category, "Error Tracking",
            error_tracking, 2, 2,
            f"Error tracking {'mentioned' if error_tracking else 'not mentioned'}"
        )
        
        # Check 4: Health check endpoints (2 points)
        has_healthcheck = False
        for source_file in source_files[:20]:
            if self._file_contains(
                source_file,
                ["/health", "/healthz", "/status", "health_check", "healthcheck"]
            ):
                has_healthcheck = True
                break
        
        self._add_check(
            category, "Health Checks",
            has_healthcheck, 2, 2,
            f"Health checks {'implemented' if has_healthcheck else 'not detected'}"
        )
        
        # Check 5: Observability documentation (1 point)
        observability_docs = False
        if readme := self._file_exists("README.md"):
            observability_docs = self._file_contains(
                readme,
                ["observability", "metrics", "tracing", "telemetry", "monitoring"]
            )
        
        self._add_check(
            category, "Observability Docs",
            observability_docs, 1, 1,
            f"Observability docs {'found' if observability_docs else 'not found'}"
        )
    
    # Community Health Checks (10 points)
    def _check_community_health(self):
        """Check community health and engagement."""
        category = "Community Health"
        
        # Check 1: Responsible disclosure policy (3 points)
        disclosure = self._file_exists("SECURITY.md", ".github/SECURITY.md")
        has_disclosure_info = False
        if disclosure:
            has_disclosure_info = self._file_contains(
                disclosure,
                ["report", "disclosure", "vulnerability", "responsible"]
            )
        
        self._add_check(
            category, "Responsible Disclosure",
            has_disclosure_info, 3, 3,
            f"Responsible disclosure {'documented' if has_disclosure_info else 'not documented'}"
        )
        
        # Check 2: Contribution guidelines (2 points)
        contrib_quality = 0
        contributing = self._file_exists("CONTRIBUTING.md", ".github/CONTRIBUTING.md")
        if contributing:
            content = contributing.read_text(encoding='utf-8', errors='ignore')
            if len(content) > 200:
                contrib_quality = 1
            if any(word in content.lower() for word in ["pull request", "code review", "style guide"]):
                contrib_quality = 2
        
        self._add_check(
            category, "Contribution Guidelines",
            contrib_quality > 0, contrib_quality, 2,
            f"Contribution guidelines quality: {contrib_quality}/2"
        )
        
        # Check 3: Support channels (2 points)
        support = self._file_exists("SUPPORT.md", ".github/SUPPORT.md")
        has_support_info = False
        readme = self._file_exists("README.md")
        if support or readme:
            check_file = support if support else readme
            has_support_info = self._file_contains(
                check_file,
                ["support", "help", "discord", "slack", "forum", "mailing list", "chat"]
            )
        
        self._add_check(
            category, "Support Channels",
            has_support_info, 2, 2,
            f"Support channels {'documented' if has_support_info else 'not documented'}"
        )
        
        # Check 4: Changelog (2 points)
        changelog = self._file_exists(
            "CHANGELOG.md", "CHANGELOG.rst", "CHANGELOG.txt",
            "HISTORY.md", "NEWS.md", "RELEASES.md"
        )
        self._add_check(
            category, "Changelog",
            changelog is not None, 2, 2,
            f"Changelog {'found' if changelog else 'not found'}"
        )
        
        # Check 5: Release process documented (1 point)
        release_docs = False
        if contributing := self._file_exists("CONTRIBUTING.md"):
            release_docs = self._file_contains(
                contributing, ["release", "version", "publish"]
            )
        
        self._add_check(
            category, "Release Process",
            release_docs, 1, 1,
            f"Release process {'documented' if release_docs else 'not documented'}"
        )
    
    def _generate_report(self) -> ComplianceReport:
        """Generate the final compliance report.
        
        Returns:
            ComplianceReport with all results
        """
        total_score = sum(check.score for check in self.checks)
        max_score = sum(check.max_score for check in self.checks)
        percentage = (total_score / max_score * 100) if max_score > 0 else 0
        
        # Generate category summary
        summary = {}
        for category in self.categories:
            category_checks = [c for c in self.checks if c.category == category]
            summary[category] = {
                "score": sum(c.score for c in category_checks),
                "max_score": sum(c.max_score for c in category_checks),
                "passed": sum(1 for c in category_checks if c.passed),
                "total": len(category_checks)
            }
        
        return ComplianceReport(
            total_score=total_score,
            max_score=max_score,
            percentage=percentage,
            checks=self.checks,
            summary=summary
        )


def print_report(report: ComplianceReport, verbose: bool = False, json_output: bool = False):
    """Print the compliance report.
    
    Args:
        report: ComplianceReport to print
        verbose: Show detailed check results
        json_output: Output as JSON
    """
    if json_output:
        # Convert to JSON
        report_dict = {
            "total_score": report.total_score,
            "max_score": report.max_score,
            "percentage": round(report.percentage, 2),
            "grade": _get_grade(report.percentage),
            "summary": report.summary,
            "checks": [asdict(check) for check in report.checks]
        }
        print(json.dumps(report_dict, indent=2))
        return
    
    # Terminal output
    print("\n" + "="*70)
    print("OWASP PROJECT COMPLIANCE REPORT")
    print("="*70)
    print(f"\nOverall Score: {report.total_score}/{report.max_score} ({report.percentage:.1f}%)")
    print(f"Grade: {_get_grade(report.percentage)}")
    print("\n" + "-"*70)
    print("CATEGORY BREAKDOWN")
    print("-"*70)
    
    for category, data in report.summary.items():
        percentage = (data['score'] / data['max_score'] * 100) if data['max_score'] > 0 else 0
        status = "✓" if percentage == 100 else "○" if percentage >= 50 else "✗"
        print(f"{status} {category:30s} {data['score']:2d}/{data['max_score']:2d} ({percentage:5.1f}%) "
              f"[{data['passed']}/{data['total']} checks passed]")
    
    if verbose:
        print("\n" + "-"*70)
        print("DETAILED RESULTS")
        print("-"*70)
        
        current_category = None
        for check in report.checks:
            if check.category != current_category:
                current_category = check.category
                print(f"\n{current_category}:")
            
            status = "✓" if check.passed else "✗"
            print(f"  {status} {check.name:40s} {check.score}/{check.max_score} - {check.message}")
    
    print("\n" + "="*70)
    print(_get_recommendation(report.percentage))
    print("="*70 + "\n")


def _get_grade(percentage: float) -> str:
    """Get letter grade based on percentage.
    
    Args:
        percentage: Score percentage
        
    Returns:
        Letter grade
    """
    if percentage >= 90:
        return "A (Excellent)"
    elif percentage >= 80:
        return "B (Good)"
    elif percentage >= 70:
        return "C (Fair)"
    elif percentage >= 60:
        return "D (Poor)"
    else:
        return "F (Failing)"


def _get_recommendation(percentage: float) -> str:
    """Get recommendation based on score.
    
    Args:
        percentage: Score percentage
        
    Returns:
        Recommendation message
    """
    if percentage >= 90:
        return "Excellent! This project meets high OWASP security and quality standards."
    elif percentage >= 80:
        return "Good work! Address the remaining items to achieve excellence."
    elif percentage >= 70:
        return "Fair. Several important areas need attention for better security posture."
    elif percentage >= 60:
        return "Poor. This project needs significant improvements in multiple areas."
    else:
        return "Critical. This project lacks fundamental security and quality practices."


def main():
    """Main entry point for the compliance checker."""
    parser = argparse.ArgumentParser(
        description="Wich - OWASP Project Compliance Checker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/repo                    # Check a repository
  %(prog)s /path/to/repo --verbose          # Show detailed results
  %(prog)s /path/to/repo --json             # Output as JSON
  %(prog)s .                                # Check current directory
        """
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to the repository to check (default: current directory)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed check results"
    )
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    args = parser.parse_args()
    
    try:
        checker = ComplianceChecker(args.path)
        report = checker.run_all_checks()
        print_report(report, verbose=args.verbose, json_output=args.json)
        
        # Exit with appropriate code
        if report.percentage >= 70:
            sys.exit(0)
        else:
            sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
