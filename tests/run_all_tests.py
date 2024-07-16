import sys
import unittest

def main():
    try:
        # Dynamically import test cases
        from utils_tests import TestUtils
        from definitions_tests import TestDefinitions
        from criteria_tokenizer_tests import TestCriteriaTokenizer
        from criteria_evaluator_tests import TestCriteriaEvaluator
        from ansible_inventory_loader_tests import TestAnsibleInventoryLoader
        from ansible_inventory_logger_tests import TestInventoryLogger
        from CriteriaUtils_tests import TestCriteriaUtils
        from ansible_inventory_cache_tests import TestAnsibleInventoryCache
        # Create a test suite
        # Note- these tests are sorted in order, from bottom up.
        # We want to fail if bottom-level functionality is impacted, as that will affect everything above it.
        test_suite = unittest.TestSuite()
        test_suite.addTest(unittest.makeSuite(TestUtils))
        test_suite.addTest(unittest.makeSuite(TestDefinitions))
        test_suite.addTest(unittest.makeSuite(TestCriteriaTokenizer))
        test_suite.addTest(unittest.makeSuite(TestCriteriaUtils))
        test_suite.addTest(unittest.makeSuite(TestCriteriaEvaluator))
        test_suite.addTest(unittest.makeSuite(TestAnsibleInventoryLoader))
        test_suite.addTest(unittest.makeSuite(TestInventoryLogger))
        test_suite.addTest(unittest.makeSuite(TestAnsibleInventoryCache))
        
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
