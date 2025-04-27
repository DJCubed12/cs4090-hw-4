import os

import pytest


def run_basic_tests() -> int:
    """Returns exit code"""
    filename = os.path.join(get_test_dir(), "test_basic.py")
    return run_test(filename)


def run_parameterized_tests() -> int:
    """Returns exit code"""
    filename = os.path.join(get_test_dir(), "test_parameterized.py")
    return run_test(filename)


def run_fixtured_tests() -> int:
    """Returns exit code"""
    filename = os.path.join(get_test_dir(), "test_fixtured.py")
    return run_test(filename)


def run_tdd_tests() -> int:
    """Returns exit code"""
    tdd1 = os.path.join(get_test_dir(), f"test_tdd_feature_1.py")
    tdd2 = os.path.join(get_test_dir(), f"test_tdd_feature_2.py")
    tdd3 = os.path.join(get_test_dir(), f"test_tdd_feature_3.py")
    return pytest.main([tdd1, tdd2, tdd3])


def run_coverage_test() -> int:
    """Returns exit code"""
    root_dir, _ = os.path.split(get_test_dir())
    return pytest.main([root_dir, "--cov"])


def run_test_with_html_report() -> int:
    """Returns the absolute path to the report file"""
    pytest.main([str(get_test_dir()), "--html=report.html"])
    return os.path.join(os.getcwd(), "report.html")


def run_test(filename) -> int:
    """Returns exit code"""
    return pytest.main([filename])


def get_test_dir() -> str:
    cwd = os.getcwd()
    outer_dir, inner_dir = os.path.split(cwd)
    if inner_dir == "src":
        # Currently in src/
        return os.path.join(outer_dir, "tests")
    else:
        # Assuming in project root
        return os.path.join(cwd, "tests")


if __name__ == "__main__":
    testDir = get_test_dir()
    print("Test dir is", get_test_dir())


run_tdd_tests()
