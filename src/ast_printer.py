from tokens import Token
from expr import Expr


class AstPrinter(Expr.Visitor):
    def print(self, expr):
        return expr.accept(self)

    def visit_while_stmt(self, stmt):
        return self.parenthesize2("while", stmt.condition, stmt.body)

    def visit_assign_expr(self, expr):
        return self.parenthesize2("=", expr.name.lexeme, expr.value)

    def visit_binary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_call_expr(self, expr):
        return self.parenthesize2("call", expr.callee, expr.arguments)

    def visit_get_expr(self, expr):
        return self.parenthesize2(".", expr.object, expr.name.lexeme)

    def visit_grouping_expr(self, expr):
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_logical_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_set_expr(self, expr):
        return self.parenthesize2("=", expr.object, expr.name.lexeme, expr.value)

    def visit_super_expr(self, expr):
        return self.parenthesize2("super", expr.method)

    def visit_this_expr(self, expr):
        return "this"

    def visit_unary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visit_variable_expr(self, expr):
        return expr.name.lexeme

    def parenthesize(self, name, *exprs):
        builder = ["(" + name]
        for expr in exprs:
            builder.append(" ")
            builder.append(expr.accept(self))
        builder.append(")")
        return "".join(builder)

    def parenthesize2(self, name, *parts):
        builder = ["(" + name]
        self.transform(builder, *parts)
        builder.append(")")
        return "".join(builder)

    def transform(self, builder, *parts):
        for part in parts:
            builder.append(" ")
            if isinstance(part, Expr):
                builder.append(part.accept(self))
            elif isinstance(part, Token):
                builder.append(part.lexeme)
            elif isinstance(part, list):
                self.transform(builder, *part)
            else:
                builder.append(str(part))
