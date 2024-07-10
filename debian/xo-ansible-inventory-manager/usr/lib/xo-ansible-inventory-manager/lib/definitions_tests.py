import unittest
from definitions import Definitions, TokenType, OperatorType

class TestDefinitions(unittest.TestCase):
    def test_allowed_transitions(self):
        """
        Test to ensure every token type is listed in ALLOWED_TRANSITIONS and every operator type is listed at least once.
        """
        for token_type in TokenType:
            with self.subTest(token_type=token_type):
                self.assertIn(token_type, Definitions.ALLOWED_TRANSITIONS)

        operator_found = {op: False for op in OperatorType}
        for allowed_tokens in Definitions.ALLOWED_TRANSITIONS.values():
            for token_type in allowed_tokens:
                for operator, replacements in Definitions.TOKEN_OPERATOR_MAPPING.get(token_type, {}).items():
                    operator_found[operator] = True

        for operator, found in operator_found.items():
            if operator != OperatorType.NONE:
                with self.subTest(operator=operator):
                    self.assertTrue(found, f"Operator {operator} not found in any allowed transition.")

    def test_unique_operator_aliases(self):
        """
        Test to ensure there are no multiple aliases for an operator that can be used in the same position.
        """
        for token_type, operators in Definitions.TOKEN_OPERATOR_MAPPING.items():
            seen_aliases = set()
            for operator, aliases in operators.items():
                for alias in aliases:
                    with self.subTest(alias=alias, operator=operator, token_type=token_type):
                        self.assertNotIn(alias, seen_aliases, f"Alias {alias} for operator {operator} in token type {token_type} is duplicated.")
                        seen_aliases.add(alias)

    def test_operator_precedence(self):
        """
        Test to ensure all operators are included in the operator precedence.
        """
        for operator in OperatorType:
            if operator != OperatorType.NONE:
                with self.subTest(operator=operator):
                    self.assertIn(operator, Definitions.OPERATOR_PRECEDENCE)
                    
if __name__ == '__main__':
    unittest.main()
