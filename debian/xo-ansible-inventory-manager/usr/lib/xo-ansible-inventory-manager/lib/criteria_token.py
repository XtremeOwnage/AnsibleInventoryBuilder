from definitions import OperatorType, TokenType

class Token:
    """
    A class representing a token used in criteria evaluation. 

    Attributes:
        value (str): The value of the token.
        type (TokenType): The type of the token (e.g., VARIABLE, CONSTANT, etc.).
        operator_type (OperatorType, optional): The operator type if the token is an operator.
    """

    def __init__(self, value : str, token_type : TokenType, operator_type : OperatorType = None):
        """
        Initialize a Token instance.

        Args:
            value (str): The value of the token.
            token_type (TokenType): The type of the token.
            operator_type (OperatorType, optional): The operator type if the token is an operator.
        """
        self.value = value
        self.type = token_type
        self.operator_type = operator_type

    def __repr__(self):
        """
        Return a string representation of the token.

        Returns:
            str: A string representation of the token.
        """
        return self.__str__()

    def __str__(self):
        """
        Return a string representation of the token, intended for human-readable output.

        Returns:
            str: A human-readable string representation of the token.
        """
        if self.type:
            if self.type in [TokenType.CONSTANT, TokenType.VARIABLE]:
                return f"[{self.type.name}: {self.value}]"
            elif self.operator_type:
                return f"[{self.type.name}, {self.operator_type.name}]"
        return f"[{self.type.name}]"

    def __eq__(self, other):
        """
        Compare two tokens for equality.

        Args:
            other (Token): The other token to compare to.

        Returns:
            bool: True if the tokens are equal, False otherwise.
        """
        return (self.value == other.value and
                self.type == other.type and
                self.operator_type == other.operator_type)
