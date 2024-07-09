import unittest
from criteria_tokenizer import CriteriaTokenizer
from criteria_token import Token
from definitions import TokenType, OperatorType, Definitions

class TestCriteriaTokenizer(unittest.TestCase):
    def setUp(self):
        """
        Set up the CriteriaTokenizer instance before each test.
        """
        self.tokenizer = CriteriaTokenizer()

    def test_add_token(self):
        """
        Test the add_token method to ensure it correctly adds a token.
        """
        self.tokenizer.add_token("test", TokenType.VARIABLE)
        self.assertEqual(len(self.tokenizer.tokens), 1)
        self.assertEqual(self.tokenizer.tokens[0], Token("test", TokenType.VARIABLE, OperatorType.NONE))

    def test_detect_token_type(self):
        """
        Test the detect_token_type method to ensure it correctly detects token types.
        """
        test_cases = [
            # (PREVIOUS TOKEN TYPE, TOKEN, EXPECTED TOKEN TYPE)
            # First token, can either be start of a grouping, or a variable.
            (None,                     "test",         TokenType.VARIABLE),
            (None,                     '(',            TokenType.GROUPING),
            (None,                     'NOT',          TokenType.NOT_OPERATOR),

            # Variables MUST be followed by a comparison operator, (or unary operator, collection operator, or IS operator)
            (TokenType.VARIABLE,       '=',            TokenType.COMPARISON_OPERATOR),
            (TokenType.VARIABLE,       '==',           TokenType.COMPARISON_OPERATOR),
            (TokenType.VARIABLE,       '>=',           TokenType.COMPARISON_OPERATOR),
            (TokenType.VARIABLE,       '>',            TokenType.COMPARISON_OPERATOR),
            (TokenType.VARIABLE,       'IS',           TokenType.IS_OPERATOR),
            (TokenType.VARIABLE,       'IN',           TokenType.COLLECTION_OPERATOR),
            (TokenType.VARIABLE,       'ISNULL',       TokenType.UNARY_OPERATOR),
            (TokenType.VARIABLE,       'GTZ',          TokenType.UNARY_OPERATOR),

            # Comparison operators, must be followed by a constant.
            (TokenType.COMPARISON_OPERATOR, '"test"',  TokenType.CONSTANT),
            (TokenType.COMPARISON_OPERATOR, 'test',    TokenType.CONSTANT),
            (TokenType.COMPARISON_OPERATOR, '5',       TokenType.CONSTANT),

            # Unary operators, must be followed by either the end of a group, or a logical operator.
            (TokenType.UNARY_OPERATOR, ')',            TokenType.GROUPING),
            (TokenType.UNARY_OPERATOR, 'OR',           TokenType.LOGICAL_OPERATOR),
            (TokenType.UNARY_OPERATOR, 'AND',          TokenType.LOGICAL_OPERATOR),
            (TokenType.UNARY_OPERATOR, '&&',           TokenType.LOGICAL_OPERATOR),
            (TokenType.UNARY_OPERATOR, '||',           TokenType.LOGICAL_OPERATOR),

            # Constants, may be followed by the end of a group, or a logical operator.
            (TokenType.CONSTANT,       ')',            TokenType.GROUPING),
            (TokenType.CONSTANT,       'OR',           TokenType.LOGICAL_OPERATOR),
            (TokenType.CONSTANT,       'AND',          TokenType.LOGICAL_OPERATOR),
            (TokenType.CONSTANT,       '&&',           TokenType.LOGICAL_OPERATOR),
            (TokenType.CONSTANT,       '||',           TokenType.LOGICAL_OPERATOR),

            # The end of a group, can only be followed by a logical operator.
            (TokenType.GROUPING,   'OR',           TokenType.LOGICAL_OPERATOR),
            (TokenType.GROUPING,   'AND',          TokenType.LOGICAL_OPERATOR),
            (TokenType.GROUPING,   '&&',           TokenType.LOGICAL_OPERATOR),
            (TokenType.GROUPING,   '||',           TokenType.LOGICAL_OPERATOR),
        ]

        for previous_token_type, token, expected_token_type in test_cases:
            with self.subTest(previous_token_type=previous_token_type, token=token, expected_token_type=expected_token_type):
                # Set the previous token type in the tokenizer to simulate the current state of the tokenizer.
                self.tokenizer.previous_token_type = previous_token_type
                # Use the tokenizer's detect_token_type method to determine the token type.
                detected_token_type, _ = self.tokenizer.detect_token_type(token)
                # Assert that the detected token type matches the expected token type.
                self.assertEqual(detected_token_type, expected_token_type)

    def test_extract_token(self):
        """
        Test the extract_token method to ensure it correctly extracts tokens.
        """
        test_cases = [
            # Basic cases
            ('"test"',                  0, 'test'),
            ('(test)',                  0, '('),
            ('&&',                      0, '&&'),
            ('test_var',                0, 'test_var'),
            ('>=',                      0, '>='),
            ('test123',                 0, 'test123'),
            ('3',                       0, '3'),
            ('!=',                      0, '!='),
            ('bare-metal',              0, 'bare-metal'),
            ('ISNULL',                  0, 'ISNULL'),
            ('IS_NOT_NULL',             0, 'IS_NOT_NULL'),

            # IP addresses  
            ('10.1.2.3:913',            0, '10.1.2.3:913'),
            ("'10.1.2.3:913'",          0, '10.1.2.3:913'),
            ('"10.1.2.3:913"',          0, '10.1.2.3:913'),

            # HTTP addresses
            ('http://example.com',      0, 'http://example.com'),
            ("'http://example.com'",    0, 'http://example.com'),
            ('"http://example.com"',    0, 'http://example.com'),

            # Words, symbols, and spaces inside single quotes
            ("'hello world!'",          0, 'hello world!'),
            ("'symbol_test!@#'",        0, 'symbol_test!@#'),

            # Words, symbols, and spaces inside double quotes
            ('"hello world!"',          0, 'hello world!'),
            ('"symbol_test!@#"',        0, 'symbol_test!@#'),

            # %, or * are valid inside of constants, due to being used as wildcards.
            ('proxm%',                  0, 'proxm%'),
            ('proxm*',                  0, 'proxm*'),
        ]
        for criteria, initial_index, expected_token in test_cases:
            with self.subTest(criteria=criteria, initial_index=initial_index, expected_token=expected_token):
                self.tokenizer.criteria = criteria
                self.tokenizer.i = initial_index
                self.assertEqual(self.tokenizer.extract_token(), expected_token)

    def test_tokenize_criteria_complex(self):
        """
        Test the tokenize_criteria method with complex criteria to ensure it correctly tokenizes the criteria.
        """
        criteria = 'NOT count is null OR count is not null OR hosts cmatch .* OR host LIKE myhost*'
        tokens = self.tokenizer.tokenize_criteria(criteria)
        expected_tokens = [
            Token("NOT", TokenType.NOT_OPERATOR, OperatorType.NOT),
            Token("count", TokenType.VARIABLE, OperatorType.NONE),
            Token("IS", TokenType.IS_OPERATOR, OperatorType.IS),
            Token("NULL", TokenType.UNARY_OPERATOR, OperatorType.NULL),
            Token("OR", TokenType.LOGICAL_OPERATOR, OperatorType.OR),
            Token("count", TokenType.VARIABLE, OperatorType.NONE),
            Token("IS", TokenType.IS_OPERATOR, OperatorType.IS),
            Token("NOT", TokenType.NOT_OPERATOR, OperatorType.NOT),
            Token("NULL", TokenType.UNARY_OPERATOR, OperatorType.NULL),
            Token("OR", TokenType.LOGICAL_OPERATOR, OperatorType.OR),
            Token("hosts", TokenType.VARIABLE, OperatorType.NONE),
            Token("CMATCH", TokenType.COLLECTION_OPERATOR, OperatorType.CMATCH),
            Token(".*", TokenType.CONSTANT, OperatorType.NONE),
            Token("OR", TokenType.LOGICAL_OPERATOR, OperatorType.OR),
            Token("host", TokenType.VARIABLE, OperatorType.NONE),
            Token("LIKE", TokenType.COMPARISON_OPERATOR, OperatorType.LIKE),
            Token("myhost*", TokenType.CONSTANT, OperatorType.NONE),
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_tokenize_criteria_various(self):
        """
        Test the tokenize_criteria method with various criteria to ensure it correctly tokenizes different scenarios.
        """
        criteria = 'count NOT null'
        tokens = self.tokenizer.tokenize_criteria(criteria)
        expected_tokens = [
            Token("count", TokenType.VARIABLE, OperatorType.NONE),
            Token("NOT", TokenType.NOT_OPERATOR, OperatorType.NOT),
            Token("NULL", TokenType.UNARY_OPERATOR, OperatorType.NULL),
        ]
        self.assertEqual(tokens, expected_tokens)

        criteria = 'count NULL'
        tokens = self.tokenizer.tokenize_criteria(criteria)
        expected_tokens = [
            Token("count", TokenType.VARIABLE, OperatorType.NONE),
            Token("NULL", TokenType.UNARY_OPERATOR, OperatorType.NULL),
        ]
        self.assertEqual(tokens, expected_tokens)

        criteria = '(count NULL) OR (count NOT NULL) OR (NOT count IS NULL)'
        tokens = self.tokenizer.tokenize_criteria(criteria)
        expected_tokens = [
            Token("(", TokenType.GROUPING, OperatorType.GROUPING_START),
            Token("count", TokenType.VARIABLE, OperatorType.NONE),
            Token("NULL", TokenType.UNARY_OPERATOR, OperatorType.NULL),
            Token(")", TokenType.GROUPING, OperatorType.GROUPING_END),
            Token("OR", TokenType.LOGICAL_OPERATOR, OperatorType.OR),
            Token("(", TokenType.GROUPING, OperatorType.GROUPING_START),
            Token("count", TokenType.VARIABLE, OperatorType.NONE),
            Token("NOT", TokenType.NOT_OPERATOR, OperatorType.NOT),
            Token("NULL", TokenType.UNARY_OPERATOR, OperatorType.NULL),
            Token(")", TokenType.GROUPING, OperatorType.GROUPING_END),
            Token("OR", TokenType.LOGICAL_OPERATOR, OperatorType.OR),
            Token("(", TokenType.GROUPING, OperatorType.GROUPING_START),
            Token("NOT", TokenType.NOT_OPERATOR, OperatorType.NOT),
            Token("count", TokenType.VARIABLE, OperatorType.NONE),
            Token("IS", TokenType.IS_OPERATOR, OperatorType.IS),
            Token("NULL", TokenType.UNARY_OPERATOR, OperatorType.NULL),
            Token(")", TokenType.GROUPING, OperatorType.GROUPING_END),
        ]
        self.assertEqual(tokens, expected_tokens)

        criteria = 'count gtz OR count_2 LIKE *'
        tokens = self.tokenizer.tokenize_criteria(criteria)
        expected_tokens = [
            Token("count", TokenType.VARIABLE, OperatorType.NONE),
            Token("GTZ", TokenType.UNARY_OPERATOR, OperatorType.GREATER_ZERO),
            Token("OR", TokenType.LOGICAL_OPERATOR, OperatorType.OR),
            Token("count_2", TokenType.VARIABLE, OperatorType.NONE),
            Token("LIKE", TokenType.COMPARISON_OPERATOR, OperatorType.LIKE),
            Token("*", TokenType.CONSTANT, OperatorType.NONE),
        ]
        self.assertEqual(tokens, expected_tokens)
    
    def test_detect_complex_operator(self):
        """
        Test the detect_complex_operator method to ensure it correctly detects and handles complex operators.
        """

        # //ToDo - This test could be much better...
        for token, expected_replacement in Definitions.COMPLEX_OPERATOR_REPLACEMENTS.items():
            # Reset the tokenizer
            self.tokenizer.tokens = []
            self.tokenizer.previous_token_type = TokenType.VARIABLE
            self.tokenizer.clause_buffer = None 
            with self.subTest(token=token):
                # Call the detect_complex_operator method
                was_replaced, finalToken = self.tokenizer.detect_complex_operator(token)
                
                # Check if the complex operator was correctly detected and replaced
                self.assertTrue(was_replaced, f"Failed to replace token: {token}")

                tokenType, operatorType = finalToken
                self.tokenizer.add_token(token, tokenType, operatorType)
                


    def test_invalid_token(self):
        """
        Test the tokenize_criteria method with invalid tokens to ensure it raises a ValueError.
        """
        criteria = 'invalid_token @'
        with self.assertRaises(ValueError):
            self.tokenizer.tokenize_criteria(criteria)

if __name__ == '__main__':
    unittest.main()
