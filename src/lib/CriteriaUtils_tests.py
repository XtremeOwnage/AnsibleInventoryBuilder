import unittest
from CriteriaUtils import *
from definitions import Definitions, TokenType, OperatorType

class TestCriteriaUtils(unittest.TestCase):
    def test_get_replacement_operators(self):
        """
        Test the get_replacement_operators method to ensure it returns the correct replacement operators.
        """
        test_cases = [
            ('NOTMATCH', [(TokenType.NOT_OPERATOR, OperatorType.NOT), (TokenType.COMPARISON_OPERATOR, OperatorType.MATCH)]),
            ('NOTIN', [(TokenType.NOT_OPERATOR, OperatorType.NOT), (TokenType.COLLECTION_OPERATOR, OperatorType.IN)]),
            ('NE', [(TokenType.NOT_OPERATOR, OperatorType.NOT), (TokenType.COMPARISON_OPERATOR, OperatorType.EQUAL)]),
            ('NOTNULL', [(TokenType.NOT_OPERATOR, OperatorType.NOT), (TokenType.UNARY_OPERATOR, OperatorType.NULL)]),
        ]

        for value, expected_replacements in test_cases:
            with self.subTest(value=value):
                replacements = get_complex_operator(value)
                self.assertEqual(replacements, expected_replacements)


    def test_match_operator(self):
        test_cases = [
            # Comparison Operators
            ('=',           True, TokenType.COMPARISON_OPERATOR, OperatorType.EQUAL        ),
            ('==',          True, TokenType.COMPARISON_OPERATOR, OperatorType.EQUAL        ),
            ('EQ',          True, TokenType.COMPARISON_OPERATOR, OperatorType.EQUAL        ),
            ('EQUALS',      True, TokenType.COMPARISON_OPERATOR, OperatorType.EQUAL        ),
            ('>',           True, TokenType.COMPARISON_OPERATOR, OperatorType.GREATER      ),
            ('GT',          True, TokenType.COMPARISON_OPERATOR, OperatorType.GREATER      ),
            ('>=',          True, TokenType.COMPARISON_OPERATOR, OperatorType.GREATER_EQUAL),
            ('GTE',         True, TokenType.COMPARISON_OPERATOR, OperatorType.GREATER_EQUAL),
            ('<',           True, TokenType.COMPARISON_OPERATOR, OperatorType.LESS         ),
            ('LT',          True, TokenType.COMPARISON_OPERATOR, OperatorType.LESS         ),
            ('<=',          True, TokenType.COMPARISON_OPERATOR, OperatorType.LESS_EQUAL   ),
            ('LTE',         True, TokenType.COMPARISON_OPERATOR, OperatorType.LESS_EQUAL   ),
            ('LIKE',        True, TokenType.COMPARISON_OPERATOR, OperatorType.LIKE         ),
            ('MATCH',       True, TokenType.COMPARISON_OPERATOR, OperatorType.MATCH        ),

            # Unary Operators
            ('ISNULL',      True, TokenType.UNARY_OPERATOR, OperatorType.NULL              ),
            ('NULL',        True, TokenType.UNARY_OPERATOR, OperatorType.NULL              ),
            ('NONE',        True, TokenType.UNARY_OPERATOR, OperatorType.NULL              ),
            ('GTZ',         True, TokenType.UNARY_OPERATOR, OperatorType.GREATER_ZERO      ),
            ('GT0',         True, TokenType.UNARY_OPERATOR, OperatorType.GREATER_ZERO      ),
            ('EQZ',         True, TokenType.UNARY_OPERATOR, OperatorType.EQUAL_ZERO        ),
            ('EQ0',         True, TokenType.UNARY_OPERATOR, OperatorType.EQUAL_ZERO        ),
            ('LTZ',         True, TokenType.UNARY_OPERATOR, OperatorType.LESS_ZERO         ),
            ('LT0',         True, TokenType.UNARY_OPERATOR, OperatorType.LESS_ZERO         ),

            # Logical Operators
            ('AND',         True, TokenType.LOGICAL_OPERATOR, OperatorType.AND    ),
            ('&&',          True, TokenType.LOGICAL_OPERATOR, OperatorType.AND    ),
            ('&',           True, TokenType.LOGICAL_OPERATOR, OperatorType.AND    ),
            ('OR',          True, TokenType.LOGICAL_OPERATOR, OperatorType.OR     ),
            ('||',          True, TokenType.LOGICAL_OPERATOR, OperatorType.OR     ),
            ('|',           True, TokenType.LOGICAL_OPERATOR, OperatorType.OR     ),

            # Collection Operators
            ('IN',          True, TokenType.COLLECTION_OPERATOR, OperatorType.IN           ),
            ('CONTAINS',    True, TokenType.COLLECTION_OPERATOR, OperatorType.IN           ),
            ('CLIKE',       True, TokenType.COLLECTION_OPERATOR, OperatorType.CMATCH       ),
            ('CMATCH',      True, TokenType.COLLECTION_OPERATOR, OperatorType.CMATCH        ),

            # Collection Unary
            ('ANY',         True, TokenType.COLLECTION_UNARY, OperatorType.C_ANY           ),

            # Grouping
            ('(',           True, TokenType.GROUPING, OperatorType.GROUPING_START     ),
            (')',           True, TokenType.GROUPING, OperatorType.GROUPING_END       ),

            # Modifier Operator
            ('NOT',         True, TokenType.NOT_OPERATOR, OperatorType.NOT   ),

            # IS Operator
            ('IS',          True, TokenType.IS_OPERATOR, OperatorType.IS   ),

            # Invalid Cases
            ('UNKNOWN',     False, None, OperatorType.NONE    ),
            (' ',           False, None, OperatorType.NONE    ),
            ('123',         False, None, OperatorType.NONE    ),
        ]


        for value, expected_match, expected_token_type, expected_operator_type in test_cases:
            with self.subTest(value=value):
                match, token_type, operator_type = match_operator(value)
                self.assertEqual(match, expected_match)
                self.assertEqual(token_type, expected_token_type)
                self.assertEqual(operator_type, expected_operator_type)

if __name__ == '__main__':
    unittest.main()