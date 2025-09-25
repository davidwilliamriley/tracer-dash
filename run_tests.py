#!/usr/bin/env python3

"""
Test runner script for tracer-dash model tests.

This script provides an easy way to run tests with different configurations.

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py --unit             # Run only unit tests
    python run_tests.py --integration      # Run only integration tests
    python run_tests.py --coverage         # Run with coverage report
    python run_tests.py --help             # Show help
"""

import sys
import subprocess
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Run tracer-dash model tests")
    
    # Test selection options
    parser.add_argument(
        "--unit", 
        action="store_true", 
        help="Run only unit tests"
    )
    parser.add_argument(
        "--integration", 
        action="store_true", 
        help="Run only integration tests"
    )
    parser.add_argument(
        "--smoke", 
        action="store_true", 
        help="Run only smoke tests"
    )
    
    # Output options
    parser.add_argument(
        "--coverage", 
        action="store_true", 
        help="Run tests with coverage report"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Verbose output"
    )
    parser.add_argument(
        "--quiet", "-q", 
        action="store_true", 
        help="Quiet output"
    )
    
    # Test file selection
    parser.add_argument(
        "--file", 
        type=str, 
        help="Run tests from specific file"
    )
    parser.add_argument(
        "--test", 
        type=str, 
        help="Run specific test function"
    )
    
    # Performance options
    parser.add_argument(
        "--no-slow", 
        action="store_true", 
        help="Skip slow tests"
    )
    parser.add_argument(
        "--fast", 
        action="store_true", 
        help="Run only fast tests (excludes integration and slow)"
    )
    
    args = parser.parse_args()
    
    # Build pytest command
    cmd = [sys.executable, "-m", "pytest"]
    
    # Add test file if specified
    if args.file:
        cmd.append(args.file)
    else:
        cmd.append("app/tests/")
    
    # Add specific test if specified
    if args.test:
        if args.file:
            cmd[-1] += f"::{args.test}"
        else:
            cmd.append(f"-k {args.test}")
    
    # Add marker filters
    markers = []
    if args.unit:
        markers.append("unit")
    elif args.integration:
        markers.append("integration")
    elif args.smoke:
        markers.append("smoke")
    elif args.fast:
        markers.append("unit or smoke")
        
    if args.no_slow:
        if markers:
            markers = [f"({' or '.join(markers)}) and not slow"]
        else:
            markers = ["not slow"]
    
    if markers:
        cmd.extend(["-m", " or ".join(markers)])
    
    # Add output options
    if args.verbose:
        cmd.append("-vv")
    elif args.quiet:
        cmd.append("-q")
    
    # Add coverage if requested
    if args.coverage:
        cmd.extend([
            "--cov=app/models",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-report=xml"
        ])
    
    # Print command for debugging
    print("Running command:", " ".join(cmd))
    print("-" * 50)
    
    # Run the tests
    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent)
        return result.returncode
    except KeyboardInterrupt:
        print("\nTest run interrupted by user")
        return 1
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1


def check_dependencies():
    """Check if required testing dependencies are available"""
    try:
        import pytest
        print(f"✓ pytest {pytest.__version__}")
    except ImportError:
        print("✗ pytest not found. Install with: pip install pytest")
        return False
    
    # Check optional dependencies
    try:
        import pytest_cov
        print(f"✓ pytest-cov {pytest_cov.__version__}")
    except ImportError:
        print("○ pytest-cov not found (coverage reports unavailable)")
    
    try:
        import pytest_timeout
        print(f"✓ pytest-timeout available")
    except ImportError:
        print("○ pytest-timeout not found (timeout protection unavailable)")
    
    return True


def show_test_info():
    """Show information about available tests"""
    try:
        cmd = [sys.executable, "-m", "pytest", "--collect-only", "-q", "app/tests/"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("Available tests:")
            print(result.stdout)
        else:
            print("Could not collect test information")
            print(result.stderr)
    except Exception as e:
        print(f"Error collecting test information: {e}")


if __name__ == "__main__":
    print("Tracer-Dash Model Test Runner")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print()
    
    # Show help for no arguments
    if len(sys.argv) == 1:
        print("Running all tests with default settings...")
        print("Use --help for more options")
        print()
    
    # Run tests
    exit_code = main()
    
    if exit_code == 0:
        print("\n✓ All tests passed!")
    else:
        print(f"\n✗ Tests failed (exit code: {exit_code})")
    
    sys.exit(exit_code)