import re
from ansible_inventory_logger import logger
from criteria_tokenizer import CriteriaTokenizer
from definitions import TokenType, OperatorType, Definitions
from globals import DEBUG_EVALUATOR_SHUNTING_YARD

class CriteriaEvaluator:
    """
    A class to evaluate criteria for assigning hosts to groups based on specific variables.
    
    Attributes:
        host_vars (dict): A dictionary containing host variables.
        group_vars (dict): A dictionary containing group variables.
        group_criteria_var (str): The variable name that contains criteria for host assignment.
        tokenizer (CriteriaTokenizer): A tokenizer for parsing criteria strings.
    """

    def __init__(self, host_vars, group_vars, group_criteria_var):
        """
        Initialize the CriteriaEvaluator with host and group variables, and the criteria variable name.
        
        Args:
            host_vars (dict): Dictionary of host variables.
            group_vars (dict): Dictionary of group variables.
            group_criteria_var (str): The variable name that contains criteria for host assignment.
        """
        self.host_vars = host_vars
        self.group_vars = group_vars
        self.group_criteria_var = group_criteria_var
        self.tokenizer = CriteriaTokenizer()
        logger.debug(f"Initialized CriteriaEvaluator with group_criteria_var: {group_criteria_var}")

    def evaluate_criteria(self, criteria, host):
        """
        Evaluate the criteria for a specific host to determine if it should be assigned to a group.
        
        Args:
            criteria (str): The criteria string to evaluate.
            host (str): The host name to evaluate against the criteria.
        
        Returns:
            bool: True if the host meets the criteria, False otherwise.
        """
        logger.debug(f"Evaluating criteria: {criteria} for host: {host}")
        
        tokens = self.tokenizer.tokenize_criteria(criteria)
        logger.debug(f"Tokens: {tokens}")
        
        rpn_tokens = self.shunting_yard(tokens)
        logger.debug(f"RPN Tokens: {rpn_tokens}")
        
        result = self._evaluate_tokens(rpn_tokens, host)
        logger.debug(f"Evaluation result for host {host}: {result}")
        
        return result

    def shunting_yard(self, tokens):
        """
        Convert infix tokens to postfix using the Shunting Yard algorithm.
        
        Args:
            tokens (list): List of tokens in infix notation.
        
        Returns:
            list: List of tokens in postfix notation.
        """
        logger.debug("Converting tokens to RPN using Shunting Yard algorithm.")
        
        output_queue = []
        operator_stack = []

        for token in tokens:
            if DEBUG_EVALUATOR_SHUNTING_YARD:
                logger.debug(f"Processing token: {token}")

            if token.type in [TokenType.VARIABLE, TokenType.CONSTANT]:
                output_queue.append(token)
            elif token.type in [TokenType.COMPARISON_OPERATOR, TokenType.LOGICAL_OPERATOR, TokenType.UNARY_OPERATOR, TokenType.NOT_OPERATOR, TokenType.COLLECTION_OPERATOR]:
                while (operator_stack and operator_stack[-1].type in [TokenType.COMPARISON_OPERATOR, TokenType.LOGICAL_OPERATOR, TokenType.UNARY_OPERATOR, TokenType.COLLECTION_OPERATOR] and
                    Definitions.OPERATOR_PRECEDENCE[operator_stack[-1].operator_type] >= Definitions.OPERATOR_PRECEDENCE[token.operator_type]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token.type == TokenType.GROUPING:
                if token.operator_type == OperatorType.GROUPING_START:
                    operator_stack.append(token)
                elif token.operator_type == OperatorType.GROUPING_END:
                    while operator_stack and operator_stack[-1].operator_type != OperatorType.GROUPING_START:
                        output_queue.append(operator_stack.pop())
                    if not operator_stack:
                        logger.error("Mismatched parentheses detected")
                        raise ValueError("Mismatched parentheses detected")
                    operator_stack.pop()  # Remove the GROUPING_START
            else:
                logger.error(f"Unsupported TokenType: {token.type}")
                raise ValueError(f"Unsupported TokenType: {token.type}")

            if DEBUG_EVALUATOR_SHUNTING_YARD:
                logger.debug(f"Output queue: {output_queue}")
                logger.debug(f"Operator stack: {operator_stack}")

        while operator_stack:
            top = operator_stack.pop()
            if top.type == TokenType.GROUPING:
                logger.error("Mismatched parentheses detected")
                raise ValueError("Mismatched parentheses detected")
            output_queue.append(top)

        if DEBUG_EVALUATOR_SHUNTING_YARD:
            logger.debug(f"Final output queue: {output_queue}")

        return output_queue

    def _evaluate_tokens(self, tokens, host):
        """
        Evaluate the RPN tokens to determine if the criteria is met for the host.
        
        Args:
            tokens (list): List of tokens in postfix notation.
            host (str): The host name to evaluate.
        
        Returns:
            bool: True if the criteria is met, False otherwise.
        """
        logger.debug(f"Evaluating tokens: {tokens}")
        
        stack = []
        for token in tokens:
            if token.type == TokenType.VARIABLE:
                value = self.get_host_var(host, token.value)
                stack.append(value)
            elif token.type == TokenType.CONSTANT:
                stack.append(token.value)
            elif token.type in [TokenType.COMPARISON_OPERATOR]:
                if len(stack) < 2:
                    logger.error("Insufficient values in stack for comparison")
                    raise ValueError("Insufficient values in stack for comparison")
                right_value = stack.pop()
                left_value = stack.pop()
                comparison_result = self._evaluate_condition(left_value, token.operator_type, right_value)
                stack.append(comparison_result)
            elif token.type == TokenType.LOGICAL_OPERATOR:
                if len(stack) < 2:
                    logger.error("Insufficient values in stack for logical operation")
                    raise ValueError("Insufficient values in stack for logical operation")
                right_result = stack.pop()
                left_result = stack.pop()
                logical_result = self._apply_logical_operator(left_result, token.operator_type, right_result)
                stack.append(logical_result)
            elif token.type == TokenType.UNARY_OPERATOR:
                if len(stack) < 1:
                    logger.error("Insufficient values in stack for unary operation")
                    raise ValueError("Insufficient values in stack for unary operation")
                operand = stack.pop()
                unary_result = self._evaluate_condition(operand, token.operator_type)
                stack.append(unary_result)
            elif token.type == TokenType.NOT_OPERATOR:
                if len(stack) < 1:
                    logger.error("Insufficient values in stack for NOT operation")
                    raise ValueError("Insufficient values in stack for NOT operation")
                operand = stack.pop()
                not_result = not operand
                stack.append(not_result)
            elif token.type == TokenType.COLLECTION_OPERATOR:
                if len(stack) < 2:
                    logger.error("Insufficient values in stack for collection operation")
                    raise ValueError("Insufficient values in stack for collection operation")
                right_value = stack.pop()
                left_value = stack.pop()
                collection_result = self._evaluate_collection_condition(left_value, token.operator_type, right_value)
                stack.append(collection_result)
            else:
                logger.error(f"Unsupported TokenType: {token.type}")
                raise ValueError(f"Unsupported TokenType: {token.type}")

            logger.debug(f"Stack after processing token: {stack}")

        if len(stack) != 1:
            logger.error("Invalid RPN expression")
            raise ValueError("Invalid RPN expression")

        final_result = stack[0]
        logger.debug(f"Final result: {final_result}")
        return final_result

    def _evaluate_condition(self, left_value, operator, right_value=None):
        """
        Evaluate a comparison or unary condition.
        
        Args:
            left_value (Any): The left operand.
            operator (OperatorType): The operator to apply.
            right_value (Any, optional): The right operand. Defaults to None for unary operators.
        
        Returns:
            bool: The result of the condition.
        """
        logger.debug(f"Evaluating condition: {left_value} {operator.name} {right_value}")

        if operator == OperatorType.NULL:
            result = left_value is None
        elif operator == OperatorType.GREATER_ZERO:
            result = float(left_value) > 0
        elif operator == OperatorType.EQUAL_ZERO:
            result = float(left_value) == 0
        elif operator == OperatorType.LESS_ZERO:
            result = float(left_value) < 0
        else:
            if left_value is None:
                return False

            try:
                left_value = float(left_value)
                right_value = float(right_value)
                comparison_mode = 'numeric'
            except (ValueError, TypeError):
                comparison_mode = 'alphanumeric'

            if comparison_mode == 'numeric':
                if operator == OperatorType.EQUAL:
                    result = left_value == right_value
                elif operator == OperatorType.GREATER:
                    result = left_value > right_value
                elif operator == OperatorType.GREATER_EQUAL:
                    result = left_value >= right_value
                elif operator == OperatorType.LESS:
                    result = left_value < right_value
                elif operator == OperatorType.LESS_EQUAL:
                    result = left_value <= right_value
                else:
                    result = False
            else:
                if operator == OperatorType.EQUAL:
                    result = str(left_value) == str(right_value)
                elif operator == OperatorType.GREATER:
                    result = str(left_value) > str(right_value)
                elif operator == OperatorType.GREATER_EQUAL:
                    result = str(left_value) >= str(right_value)
                elif operator == OperatorType.LESS:
                    result = str(left_value) < str(right_value)
                elif operator == OperatorType.LESS_EQUAL:
                    result = str(left_value) <= str(right_value)
                elif operator == OperatorType.MATCH:
                    result = bool(re.match(right_value, left_value))
                elif operator == OperatorType.LIKE:
                    result = self._wildcard_match(left_value, right_value)
                else:
                    result = False

        logger.debug(f"Result of condition: {result}")
        return result

    def _evaluate_collection_condition(self, left_value, operator_type, right_value):
        """
        Evaluate collection condition between left_value and right_value based on operator_type.
        
        Args:
            left_value: The left operand.
            operator_type: The type of collection operator.
            right_value: The right operand.
        
        Returns:
            bool: Result of the collection operation.
        """
        if operator_type == OperatorType.IN:
            return right_value in left_value
        elif operator_type == OperatorType.CMATCH:
            return any(re.match(right_value, item) for item in left_value)
        elif operator_type == OperatorType.ANY:
            return bool(left_value)  # Assuming ANY means the collection is not empty
        else:
            logger.error(f"Unsupported OperatorType: {operator_type}")
            raise ValueError(f"Unsupported OperatorType: {operator_type}")

    def _wildcard_match(self, value, pattern):
        """
        Match a value against a wildcard pattern.

        Args:
            value (str): The value to match.
            pattern (str): The wildcard pattern to match against.

        Returns:
            bool: True if the value matches the pattern, False otherwise.
        """
        regex_pattern = "^" + re.escape(pattern)
        for wildcard in Definitions.WILDCARD_SYMBOLS:
            regex_pattern = regex_pattern.replace(re.escape(wildcard), ".*")
        regex_pattern += "$"
        return bool(re.match(regex_pattern, value))

    def _apply_logical_operator(self, left, operator, right):
        """
        Apply a logical operator to two boolean values.
        
        Args:
            left (bool): The left operand.
            operator (OperatorType): The logical operator to apply.
            right (bool): The right operand.
        
        Returns:
            bool: The result of the logical operation.
        """
        logger.debug(f"Applying logical operator {operator.value}: left {left}, right {right}")

        if operator == OperatorType.AND:
            result = left and right
        elif operator == OperatorType.OR:
            result = left or right
        else:
            result = False

        logger.debug(f"Result of logical operator {operator.value}: {result}")
        return result

    def get_host_var(self, host, key):
        """
        Retrieve a variable for a specific host.
        
        Args:
            host (str): The host name.
            key (str): The variable key.
        
        Returns:
            Any: The value of the variable for the host.
        """
        value = self.host_vars.get(host, {}).get(key, None)
        logger.debug(f"Retrieved host variable: [HOST: '{host}', KEY: '{key}', VALUE: '{value}']")
        return value
