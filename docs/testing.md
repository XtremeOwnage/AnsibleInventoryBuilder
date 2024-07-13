# Testing

## Overview

This document provides details on how to test the Ansible Dynamic Inventory Script to ensure it is functioning correctly.

## Running Tests

There is a script in the root of this repository named `run-tests` that will automatically run all of the tests to detect any issues.

### Steps to Run Tests

1. **Navigate to the Repository Root**: Ensure you are in the root directory of the repository.
   
   ```sh
   cd /path/to/repository
   ```

2. **Run the Test Script**: Execute the `run-tests` script to run all the tests.
   
   ```sh
   ./run-tests
   ```

This script will execute all the test cases and output the results, helping you identify any issues that need to be addressed.

## Adding New Tests

### Naming Convention

Each new test file should have the same name as the file it is testing, with an additional suffix `tests`.

**Example**:
- If you are testing `utils.py`, the test file should be named `utils_tests.py`.
- If you are testing `criteria_tokenizer.py`, the test file should be named `criteria_tokenizer_tests.py`.

### Adding Tests

1. **Create the Test File**:
   - Create a new file in the same directory as the file you are testing.
   - Name the file following the naming convention described above.

2. **Write Your Tests**:
   - Use the `unittest` framework to write your tests.
   - Ensure that each test class inherits from `unittest.TestCase`.

**Example**:
```python
import unittest
from utils import some_function_to_test

class TestUtils(unittest.TestCase):
    def test_some_function(self):
        self.assertEqual(some_function_to_test(), expected_result)
```

3. **Add the Test to the Test Runner**:
   - Open `run_all_tests.py`.
   - Import your new test class.
   - Add your test class to the test suite.

**Example**:
```python
import sys
import unittest

def main():
    try:
        # Dynamically import test cases
        from utils_tests import TestUtils
        ...
        from your_new_tests import TestYourNewClass  # Add this line

        # Create a test suite
        test_suite = unittest.TestSuite()
        test_suite.addTest(unittest.makeSuite(TestUtils))
        ...
        test_suite.addTest(unittest.makeSuite(TestYourNewClass))  # Add this line

        # Create and configure the test runner
        test_runner = unittest.TextTestRunner(verbosity=2, failfast=True)
        result = test_runner.run(test_suite)

        if not result.wasSuccessful():
            sys.exit(1)  # Exit with status code 1 to indicate error

    except ImportError as e:
        print(f"Failed to import a test module: {e}")
        sys.exit(1)  # Exit with status code 1 to indicate error

if __name__ == '__main__':
    main()
```