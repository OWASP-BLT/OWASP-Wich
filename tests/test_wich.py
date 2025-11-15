#!/usr/bin/env python3
"""
Unit tests for Wich compliance checker.
"""

import sys
import os
import json
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path to import wich
sys.path.insert(0, str(Path(__file__).parent.parent))

from wich import ComplianceChecker, ComplianceReport


class TestComplianceChecker:
    """Test suite for ComplianceChecker."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create a temporary directory for test repositories
        self.test_dir = tempfile.mkdtemp()
        self.test_repo = Path(self.test_dir) / "test_repo"
        self.test_repo.mkdir()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_checker_initialization(self):
        """Test that checker initializes correctly."""
        checker = ComplianceChecker(str(self.test_repo))
        assert checker.repo_path == self.test_repo
        assert len(checker.categories) == 10
        assert sum(checker.categories.values()) == 100
    
    def test_checker_invalid_path(self):
        """Test that checker raises error for invalid path."""
        try:
            ComplianceChecker("/nonexistent/path")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "does not exist" in str(e)
    
    def test_empty_repository_scoring(self):
        """Test scoring for an empty repository."""
        checker = ComplianceChecker(str(self.test_repo))
        report = checker.run_all_checks()
        
        # Empty repo should have low score
        assert isinstance(report, ComplianceReport)
        assert report.total_score < report.max_score
        assert report.max_score == 100
        assert 0 <= report.percentage <= 100
    
    def test_license_file_detection(self):
        """Test LICENSE file detection."""
        # Create LICENSE file
        license_file = self.test_repo / "LICENSE"
        license_file.write_text("MIT License\n\nCopyright (c) 2025 Test")
        
        checker = ComplianceChecker(str(self.test_repo))
        report = checker.run_all_checks()
        
        # Should detect LICENSE and copyright
        license_checks = [c for c in report.checks if c.category == "Legal & Licensing"]
        assert any(c.passed and "LICENSE" in c.name for c in license_checks)
    
    def test_readme_detection(self):
        """Test README file detection."""
        # Create README
        readme = self.test_repo / "README.md"
        readme.write_text("# Test Project\n\n" + "x" * 600 + "\n\n## Installation\n\n## Usage\n")
        
        checker = ComplianceChecker(str(self.test_repo))
        report = checker.run_all_checks()
        
        # Should detect README with quality
        doc_checks = [c for c in report.checks if c.category == "Documentation"]
        readme_checks = [c for c in doc_checks if "README" in c.name]
        assert any(c.passed for c in readme_checks)
    
    def test_security_policy_detection(self):
        """Test SECURITY.md detection."""
        # Create SECURITY.md
        security = self.test_repo / "SECURITY.md"
        security.write_text("# Security Policy\n\nTo report vulnerabilities, email security@example.com")
        
        checker = ComplianceChecker(str(self.test_repo))
        report = checker.run_all_checks()
        
        # Should detect security policy
        security_checks = [c for c in report.checks if "Security" in c.name or "security" in c.name.lower()]
        assert any(c.passed for c in security_checks)
    
    def test_gitignore_detection(self):
        """Test .gitignore detection."""
        # Create .gitignore
        gitignore = self.test_repo / ".gitignore"
        gitignore.write_text("*.pyc\n__pycache__/\n.venv/\n" + "*.log\n" * 20)
        
        checker = ComplianceChecker(str(self.test_repo))
        report = checker.run_all_checks()
        
        # Should detect .gitignore
        code_checks = [c for c in report.checks if c.category == "Code Quality"]
        gitignore_checks = [c for c in code_checks if "gitignore" in c.name.lower()]
        assert any(c.passed for c in gitignore_checks)
    
    def test_code_of_conduct_detection(self):
        """Test CODE_OF_CONDUCT.md detection."""
        # Create CODE_OF_CONDUCT.md
        coc = self.test_repo / "CODE_OF_CONDUCT.md"
        coc.write_text("# Code of Conduct\n\nBe respectful and inclusive.")
        
        checker = ComplianceChecker(str(self.test_repo))
        report = checker.run_all_checks()
        
        # Should detect Code of Conduct
        gov_checks = [c for c in report.checks if c.category == "Governance"]
        coc_checks = [c for c in gov_checks if "Code of Conduct" in c.name]
        assert any(c.passed for c in coc_checks)
    
    def test_ci_config_detection(self):
        """Test CI configuration detection."""
        # Create GitHub Actions workflow
        workflows_dir = self.test_repo / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        workflow = workflows_dir / "test.yml"
        workflow.write_text("name: Test\non: push\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - run: make test")
        
        checker = ComplianceChecker(str(self.test_repo))
        report = checker.run_all_checks()
        
        # Should detect CI configuration
        ci_checks = [c for c in report.checks if c.category == "CI/CD"]
        assert any(c.passed for c in ci_checks)
    
    def test_report_summary(self):
        """Test report summary generation."""
        checker = ComplianceChecker(str(self.test_repo))
        report = checker.run_all_checks()
        
        # Check summary structure
        assert len(report.summary) == 10
        for category, data in report.summary.items():
            assert "score" in data
            assert "max_score" in data
            assert "passed" in data
            assert "total" in data
            assert data["score"] <= data["max_score"]
            assert data["passed"] <= data["total"]
    
    def test_case_insensitive_detection(self):
        """Test case-insensitive file detection."""
        # Create readme with different case
        readme = self.test_repo / "readme.MD"
        readme.write_text("# Test Project\n" + "x" * 600)
        
        checker = ComplianceChecker(str(self.test_repo))
        report = checker.run_all_checks()
        
        # Should detect README regardless of case
        doc_checks = [c for c in report.checks if c.category == "Documentation"]
        readme_checks = [c for c in doc_checks if "README" in c.name]
        assert any(c.passed for c in readme_checks)
    
    def test_test_directory_detection(self):
        """Test that test directories are detected."""
        # Create tests directory
        tests_dir = self.test_repo / "tests"
        tests_dir.mkdir()
        test_file = tests_dir / "test_example.py"
        test_file.write_text("def test_something():\n    assert True")
        
        checker = ComplianceChecker(str(self.test_repo))
        report = checker.run_all_checks()
        
        # Should detect test files
        test_checks = [c for c in report.checks if c.category == "Testing"]
        test_file_checks = [c for c in test_checks if "Test Files" in c.name]
        assert any(c.passed for c in test_file_checks)


def run_tests():
    """Run all tests."""
    import inspect
    
    test_class = TestComplianceChecker()
    test_methods = [
        method for method in dir(test_class)
        if method.startswith('test_') and callable(getattr(test_class, method))
    ]
    
    passed = 0
    failed = 0
    
    print("Running tests...\n")
    
    for method_name in test_methods:
        try:
            test_class.setup_method()
            method = getattr(test_class, method_name)
            method()
            test_class.teardown_method()
            print(f"✓ {method_name}")
            passed += 1
        except Exception as e:
            print(f"✗ {method_name}: {e}")
            failed += 1
    
    print(f"\n{passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
