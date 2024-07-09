from ansible_inventory_logger import logger
from definitions import TokenType, OperatorType, Definitions
from criteria_token import Token
from utils import extract_quoted_string, skip_whitespace
from CriteriaUtils import *

class CriteriaTokenizer:
    """
    A class used to tokenize criteria expressions into meaningful parts for further processing.
    """
    
    previous_token_type : TokenType = None
    clause_buffer : list[Token] = []
    tokens : list[Token] = []
    i : int = 0


    def __init__(self):
        """
        Initialize the CriteriaTokenizer.
        """
        self.tokens = []
        self.criteria = ''
        self.i = 0
        self.previous_token_type = None
        self.clause_buffer = []  # Buffer to keep track of the current clause
        logger.debug("Initialized CriteriaTokenizer")

    def add_token(self, value : str, token_type : TokenType, operator_type : OperatorType =OperatorType.NONE):
        """
        Add a token to the token list.

        Args:
            value (str): The token value.
            token_type (TokenType): The type of the token.
            operator_type (OperatorType): The type of the operator (default is OperatorType.NONE).
        """

        if not token_type in [TokenType.CONSTANT, TokenType.VARIABLE]:
            logger.verbose(f"Converting {token_type} to uppercase.")
            value = value.upper()

        token = Token(value, token_type, operator_type)
        self.previous_token_type = token_type        
        self.tokens.append(token)

        if token_type == TokenType.VARIABLE or self.clause_buffer:
            logger.verbose(f"Appending {token} to clause. Clause: {self.clause_buffer}")
            self.clause_buffer.append(token)
        logger.debug(f"Added token: {token}")
    
    def detect_token_type(self, token_string : str) -> tuple[TokenType, OperatorType]:
        """
        Detect the token type based on the given token.

        Args:
            token (str): The token to detect the type of.

        Returns:
            tuple: (TokenType, OperatorType)
                - TokenType: The detected token type.
                - OperatorType: The detected operator type (default is OperatorType.NONE).
        """
        allowed_token_types = get_allowed_token_type(self.previous_token_type)
        in_clause = bool(self.clause_buffer)
        token_string = token_string.strip()

        logger.debug(f"Detecting token type for '{token_string}', allowed token types after {self.previous_token_type}: {allowed_token_types}")

        # region - Match Operator
        match, token_type, operator_type = match_operator(token_string)
        logger.verbose(f"'{token_string}', IsMatch: {match}, Type: {token_type}, OPType: {operator_type}")
        # Ignore invalid token types while inside a clause
        if match and not validate_token_type(in_clause, self.previous_token_type, token_type):
            logger.verbose(f"Discarding token_type as {token_type} is not allowed within a clause.")
            token_type = None
            operator_type = None 
        elif not match:
            token_type = None
            operator_type = None  
        else:   
            logger.debug(f"Detected token type: {token_type} with operator type: {operator_type}")
            return token_type, operator_type       
        # endregion


        for allowed_token_type in allowed_token_types:
            if allowed_token_type == TokenType.VARIABLE and not self.clause_buffer:
                if any(symbol in token_string for symbol in Definitions.TOKENIZER_ALLOWED_SYMBOLS) or token_string.isalnum():
                    token_type = TokenType.VARIABLE
                    operator_type = OperatorType.NONE
                    break
            elif allowed_token_type == TokenType.CONSTANT:
                if token_string.startswith(tuple(Definitions.TOKENIZER_QUOTE_SYMBOLS)) and token_string.endswith(tuple(Definitions.TOKENIZER_QUOTE_SYMBOLS)):
                    token_type = TokenType.CONSTANT
                    operator_type = OperatorType.NONE
                    break
                elif any(symbol in token_string for symbol in Definitions.TOKENIZER_ALLOWED_SYMBOLS) or token_string.isalnum():
                    token_type = TokenType.CONSTANT
                    operator_type = OperatorType.NONE
                    break
        else:
            logger.error(f"Unexpected token {token_string} at position {self.i}")
            raise ValueError(f"Unexpected token {token_string} at position {self.i}")

        if validate_token_type(bool(self.clause_buffer), self.previous_token_type, token_type):
            logger.debug(f"Detected token type: {token_type} with operator type: {operator_type}")
            return token_type, operator_type
        else:
            logger.error(f"Invalid token sequence for token {token_string} with previous token type {self.previous_token_type}")
            raise ValueError(f"Invalid token sequence for token {token_string} with previous token type {self.previous_token_type}")

    def extract_token(self):
        """
        Extract an entire token from the criteria.

        Returns:
            str: The extracted token.
        """
        start_index = self.i

        # Handle quoted strings
        if self.criteria[self.i] in Definitions.TOKENIZER_QUOTE_SYMBOLS:
            token, self.i = extract_quoted_string(self.criteria, self.i)
        # Handle stop symbols directly
        elif self.criteria[self.i] in Definitions.TOKENIZER_STOP_SYMBOLS:
            token = self.criteria[self.i]
            self.i += 1
        else:
            # Handle alphanumeric and allowed symbols
            if self.criteria[self.i].isalnum() or self.criteria[self.i] in Definitions.TOKENIZER_ALLOWED_SYMBOLS:
                while self.i < len(self.criteria) and (self.criteria[self.i].isalnum() or self.criteria[self.i] in Definitions.TOKENIZER_ALLOWED_SYMBOLS):
                    self.i += 1
                token = self.criteria[start_index:self.i]
            else:
                # Handle non-alphanumeric and non-allowed symbols (not being too greedy)
                while self.i < len(self.criteria) and self.criteria[self.i] not in Definitions.TOKENIZER_STOP_SYMBOLS and not self.criteria[self.i].isalnum():
                    self.i += 1
                token = self.criteria[start_index:self.i]

        logger.verbose(f"Preparing to strip {token}")
        token = token.strip()
        logger.debug(f"Extracted token: '{token}' at position {start_index}-{self.i}")
        logger.debug(f"Remaining criteria to parse: '{self.criteria[self.i:]}'")
        return token

    def validate_clause(self):
        """
        Validate the current clause structure to ensure it starts with a NOT or VARIABLE and ends with a UNARY_OPERATOR or CONSTANT.

        Returns:
            bool: True if the clause is valid, False otherwise.
        """

        # ToDo - Fix logic. needs to be better.
        if not self.clause_buffer:
            return True

        first_token = self.clause_buffer[0]
        last_token = self.clause_buffer[-1]

        if first_token.type not in Definitions.CLAUSE_STARTING_TOKEN_TYPES:
            return False

        if last_token.type not in Definitions.CLAUSE_ENDING_TOKEN_TYPES:
            return False

        return True

    def finalize_clause(self):
        """
        Finalize the current clause by validating it and clearing the buffer.
        """
        if not self.validate_clause():
            logger.error("Invalid clause structure detected.")
            raise ValueError("Invalid clause structure detected.")
        self.clause_buffer.clear()

    def detect_complex_operator(self, token: str) -> tuple[bool, tuple[TokenType, OperatorType]]:
        """
        Detect and handle complex operators comprised of multiple characters.

        Args:
        - token (str): The operator token to be checked.

        Returns:
        - tuple[bool, tuple[TokenType, OperatorType]]: A tuple containing a boolean indicating
        if the complex operator is valid and a tuple of TokenType and OperatorType for
        the complex operator if valid.
        """
        # Get the list of replacement operators for the given token
        replacement_operators = get_complex_operator(token)
        
        # Check if there are any replacement operators
        if replacement_operators:
            # Log that we are validating the replacement operator
            logger.info(f"Validating complex operator: {token}")
            
            # Extract the TokenType from each tuple in the replacement operators list
            tknList = [t[0] for t in replacement_operators]
            
            # Validate the sequence of tokens based on the current state of the clause buffer and the previous token type
            if validate_token_sequence(bool(self.clause_buffer), self.previous_token_type, tknList):
                # Log that the replacement operator is valid
                logger.debug(f"Complex operator is valid: {token}")
                
                # Enumerate through each replacement operator, except the last one
                for idx, (tokenType, operatorType) in enumerate(replacement_operators[:-1]):
                    # Add each token to the internal token buffer
                    self.add_token('', tokenType, operatorType)
                    
                # Return True indicating the complex operator is valid, along with the last operator in the list
                return True, replacement_operators[-1]
            else:
                # Log that the replacement operator is not valid
                logger.debug(f"Complex operator is not valid: {token}")
                return False, None

        # If no replacement operators are found, return False and None
        return False, None

    def tokenize_criteria(self, criteria ):
        """
        Tokenize the criteria into meaningful parts.

        Args:
            criteria (str): The criteria to tokenize.

        Returns:
            list: A list of tokens.
        """
        logger.debug(f"Tokenizing Expression: {criteria}")

        self.tokens = []
        self.criteria = criteria
        self.i = 0
        self.previous_token_type = None
        self.clause_buffer = []

        while self.i < len(criteria):
            self.i = skip_whitespace(criteria, self.i)
            if self.i >= len(criteria):
                break

            token = self.extract_token()
            logger.debug(f"Extracted token: {token}")

            # Attempt to detect a complex operator
            was_replaced, replacement = self.detect_complex_operator(token)

            # If no complex operator was detected, fall back to detecting the current token and operator type
            if not was_replaced:
                token_type, operator_type = self.detect_token_type(token)
            else:
                token_type, operator_type = replacement             

            self.add_token(token, token_type, operator_type)

            if token_type in Definitions.CLAUSE_ENDING_TOKEN_TYPES:
                logger.debug(f"Clause Complete. Contents: {self.clause_buffer}")
                self.finalize_clause()

            logger.debug(f"Tokenizing progress: {self.tokens}")

        logger.info("Closing final clause")
        self.finalize_clause()  # Final clause validation
        logger.debug(f"Tokenization complete: {self.tokens}")
        return self.tokens
