import unittest
from utils import quote_for_json, extract_quoted_string, skip_whitespace  # Make sure to replace 'your_module_name' with the actual name of your Python module.

class TestUtils(unittest.TestCase):
    def test_values(self):
        # An array of test cases, each case is a tuple (input, expected_output)
        test_cases = [
            ('Hello "world"!', '"Hello \\"world\\"!"'),  # Test string with special characters to ensure proper escaping
            ('hello', '"hello"'),                        # Test simple string to ensure it is quoted correctly
            (42, '42'),                                  # Test integer to ensure it remains unquoted
            (3.14, '3.14'),                              # Test float to ensure it remains unquoted
            (True, 'true'),                              # Test boolean True to ensure it converts to lowercase 'true'
            (False, 'false'),                            # Test boolean False to ensure it converts to lowercase 'false'
            (None, 'null'),                              # Test None to ensure it converts to 'null'
            ([1, 2, 3], '1, 2, 3'),                      # Test simple list to check proper stripping of brackets
            ([1, [2, 3], 4], '1, [2, 3], 4'),            # Test nested list to ensure inner lists remain intact
            ({'key': 'value'}, '"key": "value"'),        # Test simple dictionary to check proper handling of key-value pairs
            ({'key': {'inner_key': 'inner_value'}}, '"key": {"inner_key": "inner_value"}'), # Test nested dictionary
            ((1, 2, 3), '1, 2, 3'),                      # Test tuple to ensure it's treated like a list
            ([], ''),                                    # Test empty list to ensure it results in an empty string
            ({}, ''),                                    # Test empty dictionary to ensure it results in an empty string
            ('', '""')                                   # Test empty string to ensure it is correctly quoted
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input_value=input_value):
                self.assertEqual(quote_for_json(input_value), expected_output)

    def test_skip_whitespace(self):
        """
        Test the skip_whitespace method to ensure it correctly skips whitespace.
        """
        test_cases = [
            ("  test", 0, 2),
            ("test", 0, 0),
            ("   ", 0, 3),
            (" test ", 0, 1),
            ("test test", 4, 5),
        ]
        for criteria, initial_index, expected_index in test_cases:
            with self.subTest(criteria=criteria, initial_index=initial_index, expected_index=expected_index):
                index = initial_index
                new_index = skip_whitespace(criteria, index)
                self.assertEqual(new_index, expected_index)

    def test_extract_quoted_string(self):
        """
        Test the extract_quoted_string method to ensure it correctly extracts strings enclosed in quotes.
        """
        test_cases = [
            ('"Hello world!"', 0, ('Hello world!', 14)),
            ("'Hello world!'", 0, ('Hello world!', 14)),
            ('"Quoted \\"string\\""', 0, ('Quoted "string"', 19)),
            ("'Another \\'quoted\\' string'", 0, ("Another 'quoted' string", 27)),
        ]
        for criteria, start_index, expected_output in test_cases:
            with self.subTest(criteria=criteria, start_index=start_index, expected_output=expected_output):
                extracted_string, new_index = extract_quoted_string(criteria, start_index)
                self.assertEqual((extracted_string, new_index), expected_output)

if __name__ == '__main__':
    unittest.main()
