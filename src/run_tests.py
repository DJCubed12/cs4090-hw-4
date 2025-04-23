import os

import pytest


def run_basic_tests():
    filename = os.path.join(getTestDir(), "test_basic.py")
    run_test(filename)


def run_test(filename):
    pytest.main([filename])


def getTestDir() -> str:
    cwd = os.getcwd()
    outer_dir, inner_dir = os.path.split(cwd)
    if inner_dir == "src":
        # Currently in src/
        return os.path.join(outer_dir, "tests")
    else:
        # Assuming in project root
        return os.path.join(cwd, "tests")


if __name__ == "__main__":
    testDir = getTestDir()
    print("Test dir is", getTestDir())

    run_basic_tests()
