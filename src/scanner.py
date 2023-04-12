
from error_management import error, report
from typing import List, Optional, Any, Dict
from tokens import Token, TokenType

KEYWORDS: Dict[str, TokenType] = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


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
        # Single character Lexemes
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
        # Two character Lexemes
        elif c == '!':
            self.__add_token(TokenType.BANG_EQUAL if self.__match('=') else TokenType.BANG)
        elif c == '=':
            self.__add_token(TokenType.EQUAL_EQUAL if self.__match('=') else TokenType.EQUAL)
        elif c == '<':
            self.__add_token(TokenType.LESS_EQUAL if self.__match('=') else TokenType.LESS)
        elif c == '>':
            self.__add_token(TokenType.GREATER_EQUAL if self.__match('=') else TokenType.GREATER)
        elif c == '/':
            if self.__match('/'):
                # For comments
                while self.__peek() != '\n' and not self.is_at_end():
                    self.__advance()
            elif self.__match('*'):
                self.__block_comment()
            else:
                self.__add_token(TokenType.SLASH)
        elif c == '\n':
            self.__line += 1
        elif c == ' ' or c == '\r' or c == '\t':
            # Ignore white spase
            pass
        else:
            if self.__is_digit(c):
                self.__number()
            else:
                error(self.__line, f"Unexpected character \"{c}\"")
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

    def __add_token(self, token_type: TokenType) -> None:
        self.__add_literal_token(token_type, None)
    # -----------------------------------------------------

    def __match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.__current] != expected:
            return False
        self.__current += 1
        return True
    # -----------------------------------------------------

    def __peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.__current]
    # -----------------------------------------------------

    def __peek_next(self) -> str:
        if self.__current + 1 >= len(self.source):
            return '\0'
        return self.source[self.__current + 1]
    # -----------------------------------------------------

    def __is_digit(self, c: str) -> bool:
        return c.isdigit()
    # -----------------------------------------------------

    def __is_alpha(self, c: str) -> bool:
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c == '_')
    # -----------------------------------------------------

    def __is_alpha_numeric(self, c: str) -> bool:
        return self.__is_alpha(c) or self.__is_digit(c)
    # -----------------------------------------------------

    def __string(self) -> None:
        while self.__peek() != '"' and not self.is_at_end():
            if self.__peek() == '\n':
                self.__line += 1
            self.__advance()

        if self.is_at_end():
            error(self.__line, "Unterminated string.")
            return

        self.__advance()  # Consume the closing ".

        # Trim the surrounding quotes.
        value = self.source[self.__start+1:self.__current-1]
        self.__add_literal_token(TokenType.STRING, value)
    # -----------------------------------------------------

    def __number(self) -> None:
        while self.__peek().isdigit():
            self.__advance()

        if self.__peek() == '.' and self.__is_digit(self.__peek_next()):
            self.__advance()  # Consume the "."
            while self.__peek().isdigit():
                self.__advance()

        self.__add_literal_token(TokenType.NUMBER, float(self.source[self.__start:self.__current]))
    # -----------------------------------------------------

    def __identifier(self) -> None:
        while self.__is_alpha_numeric(self.__peek()):
            self.__advance()

        text: str = self.source[self.__start:self.__current]
        token_type: TokenType = KEYWORDS.get(text, TokenType.IDENTIFIER)
        self.__add_token(token_type)
    # -----------------------------------------------------

    def __block_comment(self):
        level = 1
        while level > 0:
            if self.is_at_end():
                error(self.__line, "Unterminated block comment.")
                return
            c = self.__advance()
            if c == '/' and self.__peek() == '*':
                level += 1
                self.__advance()
            elif c == '*' and self.__peek() == '/':
                level -= 1
                self.__advance()
            elif c == '\n':
                self.__line += 1
    # -----------------------------------------------------
