from abc import ABC, abstractmethod
from typing import List

from tokens import Token


class Expr(ABC):
    class Visitor(ABC):
        @abstractmethod
        def visitAssignExpr(self, expr):
            pass
        @abstractmethod
        def visitBinaryExpr(self, expr):
            pass
        @abstractmethod
        def visitCallExpr(self, expr):
            pass
        @abstractmethod
        def visitGetExpr(self, expr):
            pass
        @abstractmethod
        def visitGroupingExpr(self, expr):
            pass
        @abstractmethod
        def visitLiteralExpr(self, expr):
            pass
        @abstractmethod
        def visitLogicalExpr(self, expr):
            pass
        @abstractmethod
        def visitSetExpr(self, expr):
            pass
        @abstractmethod
        def visitSuperExpr(self, expr):
            pass
        @abstractmethod
        def visitThisExpr(self, expr):
            pass
        @abstractmethod
        def visitUnaryExpr(self, expr):
            pass
        @abstractmethod
        def visitVariableExpr(self, expr):
            pass

    @abstractmethod
    def accept(self, visitor):
        pass


class Assign(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visitAssignExpr(self)

    name: Token
    value: Expr


class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)

    left: Expr
    operator: Token
    right: Expr


class Call(Expr):
    def __init__(self, callee, paren, arguments):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visitCallExpr(self)

    callee: Expr
    paren: Token
    arguments: List[Expr]


class Get(Expr):
    def __init__(self, obj, name):
        self.object = obj
        self.name = name

    def accept(self, visitor):
        return visitor.visitGetExpr(self)

    object: Expr
    name: Token


class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)

    expression: Expr


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)

    value: object


class Logical(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitLogicalExpr(self)

    left: Expr
    operator: Token
    right: Expr


class Set(Expr):
    def __init__(self, object, name, value):
        self.object = object
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visitSetExpr(self)

    object: Expr
    name: Token
    value: Expr


class Super(Expr):
    def __init__(self, keyword, method):
        self.keyword = keyword
        self.method = method

    def accept(self, visitor):
        return visitor.visitSuperExpr(self)

    keyword: Token
    method: Token


class This(Expr):
    def __init__(self, keyword):
        self.keyword = keyword

    def accept(self, visitor):
        return visitor.visitThisExpr(self)

    keyword: Token


class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)

    operator: Token
    right: Expr


class Variable(Expr):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visitVariableExpr(self)

    name: Token