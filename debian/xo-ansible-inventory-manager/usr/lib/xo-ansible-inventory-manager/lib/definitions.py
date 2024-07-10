from enum import Enum
from ansible_inventory_logger import logger

class TokenType(Enum):
    """Enum representing different types of tokens."""
    VARIABLE            = 1  # Represents a variable or identifier
    COMPARISON_OPERATOR = 2  # Represents a comparison operator (e.g., =, !=, >, etc.)
    CONSTANT            = 3  # Represents a constant value (e.g., a string or number)
    LOGICAL_OPERATOR    = 4  # Represents a logical operator (e.g., AND, OR)
    GROUPING            = 5  # Represents a grouping (e.g., a parenthesis '(' or ')')
    UNARY_OPERATOR      = 6  # Represents an operator that doesn't require a right-hand operand (e.g., ISNULL)
    COLLECTION_OPERATOR = 7  # Represents an operator which performs evaluations on collections.
    COLLECTION_UNARY    = 8  # Represents an operator which performs an operand against a collection.
    NOT_OPERATOR        = 9  # Represents an operator which affects preceding operators. (e.g., NOT)
    IS_OPERATOR         = 10 # Represents the "IS" operator used for conditions like "IS NULL"

    def __str__(self):
        return self.name

class OperatorType(Enum):
    """Enum representing different types of operators."""
    NONE            = 0  # Operator does not have a valid type

    ### COMPARISON_OPERATOR
    EQUAL           = 1  # Equality operator (e.g., =, ==, EQ, EQUALS)
    GREATER         = 2  # Greater than operator (e.g., >, GT)
    GREATER_EQUAL   = 3  # Greater than or equal operator (e.g., >=, GTE)
    LESS            = 4  # Less than operator (e.g., <, LT)
    LESS_EQUAL      = 5  # Less than or equal operator (e.g., <=, LTE)

    ### COMPARISON_OPERATOR - REGEX / LIKE
    MATCH           = 6  # Operand must match regex (e.g., LIKE, MATCH)
    LIKE            = 7  # Operand must match LIKE (e.g., LIKE)

    ### LOGICAL_OPERATOR
    AND             = 8  # Logical AND operator (e.g., AND, &&, &)
    OR              = 9  # Logical OR operator (e.g., OR, ||, |)

    ### UNARY OPERATORS
    NULL            = 10 # Null check operator (e.g., ISNULL, NULL)
    GREATER_ZERO    = 11 # Greater than zero check operator (e.g., GTZ, GT0)
    EQUAL_ZERO      = 12 # Equal to zero check operator (e.g., EQZ, EQ0)
    LESS_ZERO       = 13 # Less than zero check operator (e.g., LTZ, LT0)

    ### COLLECTION_OPERATOR
    IN              = 14 # Validate the operand exists in the collection (e.g., IN, CONTAINS)

    ### COLLECTION_OPERATOR - REGEX / LIKEs
    CMATCH          = 15 # Regex to check if any collection elements match regex (e.g., ANYMATCH, ANY_REGEX_MATCH)

    ### COLLECTION_UNARY
    C_ANY           = 16 # Specified collection must contain elements (e.g., ANY)

    ### NOT_OPERATOR
    NOT             = 17 # Negation operator affecting preceding operators (e.g., NOT)

    ### IS_OPERATOR
    IS              = 18 # "IS" operator for special use cases (e.g., IS NULL)

    ### GROUPING
    GROUPING_START  = 19 # Represents the start of a grouping (e.g., a parenthesis '(')
    GROUPING_END    = 20 # Represents the end of a grouping (e.g., a parenthesis ')')

    def __str__(self):
        return self.name
        
class Definitions:
    """Class holding definitions and utility methods for token and operator mappings."""
    TOKEN_OPERATOR_MAPPING: dict[TokenType, dict[OperatorType, list[str]]] = {
        TokenType.COMPARISON_OPERATOR: {
            OperatorType.EQUAL          : ['=', '==', 'EQ', 'EQUALS'],
            OperatorType.GREATER        : ['>', 'GT'],
            OperatorType.GREATER_EQUAL  : ['>=', 'GTE'],
            OperatorType.LESS           : ['<', 'LT'],
            OperatorType.LESS_EQUAL     : ['<=', 'LTE'],
            OperatorType.MATCH          : ['MATCH', 'REX', 'REGEX'],
            OperatorType.LIKE           : ['LIKE']
        },
        TokenType.UNARY_OPERATOR: {
            OperatorType.NULL           : ['ISNULL', 'NULL', 'NONE'],
            OperatorType.GREATER_ZERO   : ['GTZ', 'GT0'],
            OperatorType.EQUAL_ZERO     : ['EQZ', 'EQ0'],
            OperatorType.LESS_ZERO      : ['LTZ', 'LT0']
        },
        TokenType.LOGICAL_OPERATOR: {
            OperatorType.AND            : ['AND', '&&', '&'],
            OperatorType.OR             : ['OR', '||', '|']
        },
        TokenType.COLLECTION_OPERATOR: {
            OperatorType.IN             : ['IN', 'CONTAINS'],
            OperatorType.CMATCH         : ['CLIKE', 'CMATCH']
        },
        TokenType.COLLECTION_UNARY: {
            OperatorType.C_ANY          : ['ANY']
        },
        TokenType.GROUPING: {
            OperatorType.GROUPING_START : ['('],
            OperatorType.GROUPING_END   : [')']
        },
        TokenType.NOT_OPERATOR: {
            OperatorType.NOT            : ['NOT']
        },
        TokenType.IS_OPERATOR: {
            OperatorType.IS             : ['IS']
        }
    }


    """
    Defines the precedence of operators used in logical and comparison expressions.
    This is used by the shunting yard algorithm to correctly parse and evaluate
    expressions in infix notation. Operators with higher precedence values are 
    evaluated before operators with lower precedence values. Logical OR has the 
    lowest precedence, followed by logical AND. Comparison operators all have the 
    same precedence level, higher than logical operators. This ensures that in an 
    expression, comparisons are evaluated before logical operations.
    """
    OPERATOR_PRECEDENCE: dict[OperatorType,int] = {
        OperatorType.OR             : 1,  # Precedence for logical OR
        OperatorType.AND            : 2,  # Precedence for logical AND
        OperatorType.NOT            : 3,  # Precedence for logical NOT (negation)
        OperatorType.EQUAL          : 4,  # Precedence for equality
        OperatorType.GREATER        : 4,  # Precedence for greater than
        OperatorType.GREATER_EQUAL  : 4,  # Precedence for greater than or equal to
        OperatorType.LESS           : 4,  # Precedence for less than
        OperatorType.LESS_EQUAL     : 4,  # Precedence for less than or equal to
        OperatorType.MATCH          : 4,  # Precedence for regex match
        OperatorType.LIKE           : 4,  # Precedence for LIKE match
        OperatorType.NULL           : 4,  # Precedence for null check
        OperatorType.C_ANY          : 4,  # Precedence for collection ANY
        OperatorType.IN             : 4,  # Precedence for collection IN
        OperatorType.CMATCH         : 4,  # Precedence for collection regex match any
        OperatorType.GREATER_ZERO   : 4,  # Precedence for greater than zero
        OperatorType.EQUAL_ZERO     : 4,  # Precedence for equal to zero
        OperatorType.LESS_ZERO      : 4,  # Precedence for less than zero
        OperatorType.IS             : 4,  # Precedence for IS operator
        OperatorType.GROUPING_START : 5,  # Precedence for grouping start '('
        OperatorType.GROUPING_END   : 5   # Precedence for grouping end ')'
    }
    """
    Defines operator precedence inside of the shunting yard algorithm.
    """
    # Token types that start a clause
    CLAUSE_STARTING_TOKEN_TYPES: list[TokenType] = [
        TokenType.VARIABLE,
    ]
    """
    This is the list of token types which starts a new clause.
    """
    # Token types that end a clause
    CLAUSE_ENDING_TOKEN_TYPES: list[TokenType] = [
        TokenType.CONSTANT,
        TokenType.UNARY_OPERATOR,
        TokenType.COLLECTION_UNARY
    ]
    """
    List of TokenTypes which ends a clause.
    """

    # Token types not allowed while inside a clause
    CLAUSE_INVALID_TOKEN_TYPES: list[TokenType] = [
        TokenType.VARIABLE,
        TokenType.LOGICAL_OPERATOR,
        TokenType.GROUPING
    ]
    """
    List of Token Types which are not valid while inside of a clause.
    """

    # ALLOWED_TRANSITIONS defines the valid transitions between token types in the state machine for tokenization.
    #
    # This dictionary maps the current TokenType to a list of permissible TokenTypes that can follow it.
    # The purpose of this variable is to ensure the tokenizer adheres to the correct syntax structure 
    # and sequence of tokens when parsing the input criteria.
    #
    # The state machine relies on these transitions to validate and guide the tokenization process, 
    # ensuring that each token appears in a logical and syntactically correct order.
    # 
    # For example:
    # - The state machine can start with either a VARIABLE or GROUPING_START.
    # - After encountering a VARIABLE, the next expected token type is a COMPARISON_OPERATOR.
    # - After a COMPARISON_OPERATOR, the next token should be either a CONSTANT, LOGICAL_OPERATOR, or GROUPING_END.
    # - This ensures that logical operators only follow valid expressions and that groupings are properly nested.
    #
    # The ALLOWED_TRANSITIONS dictionary helps maintain the integrity of the tokenization process 
    # by enforcing these syntactic rules, preventing invalid token sequences from being generated 
    # and facilitating the correct parsing of logical expressions.


    # Adjusting the ALLOWED_TRANSITIONS and OPERATOR_PRECEDENCE to match the new definitions.
    ALLOWED_TRANSITIONS: dict[TokenType, list[TokenType]] = {
        None:                           [TokenType.VARIABLE, TokenType.GROUPING, TokenType.NOT_OPERATOR],  # Start with a variable, grouping, or a modifier operator
        TokenType.VARIABLE:             [TokenType.NOT_OPERATOR, TokenType.COMPARISON_OPERATOR, 
                                        TokenType.UNARY_OPERATOR, TokenType.COLLECTION_UNARY, 
                                        TokenType.COLLECTION_OPERATOR, TokenType.IS_OPERATOR],                 # After a variable, expect a modifier operator, comparison operator, unary operator, collection unary, collection operator, or "IS" operator
        TokenType.COMPARISON_OPERATOR:  [TokenType.CONSTANT],                                           # After a comparison operator, expect a constant
        TokenType.UNARY_OPERATOR:       [TokenType.LOGICAL_OPERATOR, TokenType.GROUPING],           # After a unary operator, expect a logical operator or grouping
        TokenType.CONSTANT:             [TokenType.LOGICAL_OPERATOR, TokenType.GROUPING],           # After a constant, expect a logical operator or grouping
        TokenType.LOGICAL_OPERATOR:     [TokenType.VARIABLE, TokenType.GROUPING, TokenType.NOT_OPERATOR],  # After a logical operator, expect a variable, grouping, or modifier operator
        TokenType.GROUPING:             [TokenType.LOGICAL_OPERATOR, TokenType.GROUPING, TokenType.NOT_OPERATOR, TokenType.VARIABLE],  # After a grouping, expect a variable, another grouping, or modifier operator
        TokenType.COLLECTION_OPERATOR:  [TokenType.CONSTANT],                                           # After a collection operator, expect a constant
        TokenType.COLLECTION_UNARY:     [TokenType.LOGICAL_OPERATOR, TokenType.GROUPING],               # After a collection unary operator, expect a logical operator or grouping
        TokenType.NOT_OPERATOR:         [TokenType.VARIABLE, TokenType.CONSTANT, TokenType.GROUPING, TokenType.UNARY_OPERATOR, TokenType.COLLECTION_UNARY, TokenType.COMPARISON_OPERATOR, TokenType.COLLECTION_OPERATOR],   # After a modifier operator, expect a variable or grouping
        TokenType.IS_OPERATOR:          [TokenType.UNARY_OPERATOR, TokenType.NOT_OPERATOR, TokenType.COLLECTION_UNARY]                                       # After an "IS" operator, expect a unary operator
    }
    """
    This sets the allowed transition types from Token type to Token type. 
    """

    # List of symbols allowed in a variable name, or constant. 
    # If the tokenizer hits one of these symbols, it will keep processing as part of the same token.
    TOKENIZER_ALLOWED_SYMBOLS: list[str] = ['_', '-', '.', ':', '/', '\\', '*', '#', '%']
    """
    These symbols are valid inside variable, and constant names
    """

    # If the tokenizer hits one of these symbols while parsing out tokens, 
    # it signifies the end of the current token.
    TOKENIZER_STOP_SYMBOLS: list[str] = [' ', '(', ')', '"', "'"]
    """
    These symbols indicate an immediate stop when parsing tokens.
    """

    # If the tokenizer hits one of these symbols, 
    # it will consider everything between the current position and the next instance of this symbol as a single token.
    TOKENIZER_QUOTE_SYMBOLS: list[str] = ['"', "'"]
    """
    List of symbols which indicates the start of a quoted string.
    """

    WILDCARD_SYMBOLS: list[str] = ['%', '*']
    """
    List of symbols used as wildcards in patterns.
    """

    ## This is a list of complex operator replacement types.
    # 
    # The COMPLEX_OPERATOR_REPLACEMENTS dictionary is used to handle complex operators that consist
    # of multiple simple operators. Each complex operator is replaced with a sequence of simpler
    # operators to facilitate easier parsing and evaluation. This is especially useful for operators
    # that include negation or combinations of multiple conditions.
    #
    # The keys of the dictionary represent the complex operators as strings.
    # The values are lists of tuples, where each tuple contains:
    #   - TokenType: The type of the token (e.g., NOT_OPERATOR, COMPARISON_OPERATOR, etc.).
    #   - OperatorType: The specific operator type (e.g., NOT, EQUAL, MATCH, etc.).

    COMPLEX_OPERATOR_REPLACEMENTS: dict[str, list[tuple[TokenType, OperatorType]]] = {
        'NOTMATCH': [(TokenType.NOT_OPERATOR, OperatorType.NOT), (TokenType.COMPARISON_OPERATOR, OperatorType.MATCH)],
        # Replaces 'NOTMATCH' with a NOT operator followed by a MATCH operator.

        'NE': [(TokenType.NOT_OPERATOR, OperatorType.NOT), (TokenType.COMPARISON_OPERATOR, OperatorType.EQUAL)],
        # Replaces 'NE' (Not Equal) with a NOT operator followed by an EQUAL operator.

        '!=': [(TokenType.NOT_OPERATOR, OperatorType.NOT), (TokenType.COMPARISON_OPERATOR, OperatorType.EQUAL)],
        # Replaces '!=' (Not Equal) with a NOT operator followed by an EQUAL operator.

        'ISNOTNULL': [(TokenType.NOT_OPERATOR, OperatorType.NOT), (TokenType.UNARY_OPERATOR, OperatorType.NULL)],
        # Replaces 'ISNOTNULL' with a NOT operator followed by a NULL unary operator.

        'NOTNULL': [(TokenType.NOT_OPERATOR, OperatorType.NOT), (TokenType.UNARY_OPERATOR, OperatorType.NULL)],
        # Replaces 'NOTNULL' with a NOT operator followed by a NULL unary operator.

        'NOTIN': [(TokenType.NOT_OPERATOR, OperatorType.NOT), (TokenType.COLLECTION_OPERATOR, OperatorType.IN)],
        # Replaces 'NOTIN' with a NOT operator followed by an IN collection operator.

        'NOMATCH': [(TokenType.NOT_OPERATOR, OperatorType.NOT), (TokenType.COLLECTION_OPERATOR, OperatorType.CMATCH)],
        # Replaces 'NOMATCH' with a NOT operator followed by a CMATCH collection operator.
    }