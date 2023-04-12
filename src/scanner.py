
from typing import List, Optional, Any
from tokens import Token, TokenType


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.__tokens: List[Token] = []
        self.__start = 0
        self.__current = 0
        self.__line = 1

    def is_at_end(self) -> bool:
        return self.__current >= len(self.source)
    # -----------------------------------------------------

    def scan_token(self) -> None:
        c = self.__advance()
        if c == '(':
            self.__add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self.__add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.__add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self.__add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.__add_token(TokenType.COMMA)
        elif c == '.':
            self.__add_token(TokenType.DOT)
        elif c == '-':
            self.__add_token(TokenType.MINUS)
        elif c == '+':
            self.__add_token(TokenType.PLUS)
        elif c == ';':
            self.__add_token(TokenType.SEMICOLON)
        elif c == '*':
            self.__add_token(TokenType.STAR)
    # -----------------------------------------------------

    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            # We are at the beginning of the next lexeme.
            start = self.__current
            self.scan_token()
        self.__tokens.append(Token(TokenType.EOF, "", None, self.__line))
        return self.__tokens
    # -----------------------------------------------------

    def __advance(self) -> str:
        self.__current += 1
        return self.source[self.__current - 1]
    # -----------------------------------------------------

    def __add_literal_token(self, token_type: TokenType, literal: Optional[Any] = None) -> None:
        lexeme: str = self.source[self.__start:self.__current]
        self.__tokens.append(Token(token_type, lexeme, literal, self.__line))
    # -----------------------------------------------------

    def __add_token(self, token_type: TokenType):
        self.__add_literal_token(token_type, None)
    # -----------------------------------------------------