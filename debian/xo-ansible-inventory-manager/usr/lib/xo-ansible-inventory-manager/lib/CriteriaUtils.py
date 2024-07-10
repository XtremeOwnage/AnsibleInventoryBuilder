from definitions import TokenType, Definitions, OperatorType
from ansible_inventory_logger import logger
from criteria_token import Token

def validate_token_type(in_clause : bool, previous_token_type : TokenType, token_type : TokenType) -> bool:
    """
    Validate a single token to ensure it follows the correct logic.

    Args:
        in_clause (bool): Indicates if we are currently inside a clause.
        previous_token_type (TokenType): The type of the previous token.
        token_type (TokenType): The token type to validate.

    Returns:
        bool: True if the token type is valid, False otherwise.
    """
    if not token_type:
        return False
    
    if not isinstance(token_type, TokenType):
        logger.error(f"{token_type} is not a TokenType")
        return False

    # Ignore invalid token types while inside a clause
    if in_clause and token_type in Definitions.CLAUSE_INVALID_TOKEN_TYPES:
        logger.debug(f"Token {token_type} is not allowed within a clause.")
        return False

    allowed_next_types = get_allowed_token_type(previous_token_type)

    if token_type not in allowed_next_types:
        logger.error(f"Invalid token sequence: {previous_token_type} cannot be followed by {token_type}")
        return False

    # Additional clause-specific validation
    if in_clause and token_type in Definitions.CLAUSE_INVALID_TOKEN_TYPES:
        logger.error(f"Invalid token inside clause: {token_type}")
        return False

    return True

def validate_token(in_clause : bool, previous_token_type : TokenType, token : Token) -> bool:
    """
    Validate a single token to ensure it follows the correct logic.

    Args:
        in_clause (bool): Indicates if we are currently inside a clause.
        previous_token_type (TokenType): The type of the previous token.
        token (Token): The token to validate.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    if not isinstance(token, Token):
        logger.error(f"{token} is not of type Token")
        return False
    
    return validate_token_type(in_clause, previous_token_type, token.type)

def validate_token_sequence(in_clause : bool, previous_token_type : TokenType, TokenTypes : list[TokenType]) -> bool:
    """
    Validate a sequence of token types to ensure they follow the correct logic.

    Args:
        in_clause (bool): Indicates if we are currently inside a clause.
        previous_token_type (TokenType): The type of the previous token.
        tokens (list): List of tokens to validate.

    Returns:
        bool: True if the token sequence is valid, False otherwise.
    """
    if not TokenTypes:
        return False

    for tokenType in TokenTypes:
        if not validate_token_type(in_clause, previous_token_type, tokenType):
            return False
        previous_token_type = tokenType

    return True

def match_operator(value) -> tuple[bool, TokenType, OperatorType]:
    """
    Check if the given value matches any of the operator replacements.

    Args:
    - value (str): The string to check for a match.

    Returns:
    - tuple: (bool, TokenType, OperatorType or None)
        - bool: Indicates if a match was found.
        - TokenType: The type of token if a match was found.
        - OperatorType or None: The operator type if a match was found, else None.
    """
    value = value.strip().upper()
    for token_type, operators in Definitions.TOKEN_OPERATOR_MAPPING.items():
        for operator_type, replacements in operators.items():
            if value in replacements:
                return True, token_type, operator_type
    return False, None, OperatorType.NONE

def get_allowed_token_type(previous_token_type : TokenType) -> list[TokenType]:
    """
    Get the next allowed token types based on the previous token type.

    Args:
    - previous_token_type (TokenType): The previous token type.

    Returns:
    - list: A list of allowed token types.
    """
    return Definitions.ALLOWED_TRANSITIONS.get(previous_token_type, [])

def get_complex_operator(value: str) -> list[tuple[TokenType, OperatorType]]:
    """
    Get the list of replacement operators for deprecated or removed operator types.

    Args:
    - value (str): The deprecated or removed operator string.

    Returns:
    - list[tuple[TokenType, OperatorType]]: A list of tuples with TokenType and OperatorType for replacement operators.
    """
    # Strip any leading/trailing whitespace from the input string and convert it to uppercase
    value = value.strip().upper()
    # Return the list of replacement operators from the COMPLEX_OPERATOR_REPLACEMENTS dictionary
    # If the value is not found in the dictionary, return an empty list
    return Definitions.COMPLEX_OPERATOR_REPLACEMENTS.get(value, [])