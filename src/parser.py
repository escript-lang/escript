from AST import *

class Parser:

    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0


    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None


    def advance(self):
        self.pos += 1
    
    def unadvance(self):
        self.pos -= 1

    def expect(self, token_type):
        tok = self.peek()
        if tok and tok.type == token_type:
            self.advance()
            return tok
        raise SyntaxError(f'Expected {token_type}, got {tok.type}')


    def parse(self):
        statements = []
        while self.peek():
            statements.append(self.statement())

        return Program(statements)


    def statement(self):
        tok = self.peek()
        if tok.type == 'ID':
            return self.assignment()
        elif tok.type == 'PRINT':
            self.advance()
            expr = self.expr()
            return Print(expr)
        elif tok.type == 'PRINTLN':
            self.advance()
            expr = self.expr()
            return Println(expr)
        elif tok.type == 'INFO':
            self.advance()
            return Information()
        else:
            return self.expr()


    def assignment(self):
        name = self.expect('ID').value
        if (self.peek() and
            self.peek().type == 'OP' and
            self.peek().value == '='):
            self.advance()
            expr = self.expr()
            return Assign(name, expr)

        raise SyntaxError(f'Invalid assignment {name}')


    def expr(self):
        return self._term_tail(self.term())


    def _term_tail(self, left):
        tok = self.peek()
        if tok and tok.type == 'OP' and tok.value in ('+', '-'):
            self.advance()
            right = self.term()
            return self._term_tail(BinAction(left, tok.value, right))

        return left


    def term(self):
        return self._factor_tail(self.factor())


    def _factor_tail(self, left):
        tok = self.peek()
        if tok and tok.type == 'OP' and tok.value in ('*', '/', '**', '>', '<', '<=', '>=', '=='):
            self.advance()
            right = self.factor()
            return self._factor_tail(BinAction(left, tok.value, right))

        return left


    def factor(self):
        tok = self.peek()
        if tok.type == 'NUMBER':
            self.advance()
            return Number(tok.value)
        elif tok.type == 'ID':
            self.advance()
            return Var(tok.value)
        elif tok.type == 'STRING':
            self.advance()
            return String(tok.value)
        elif tok.type == 'BOOLEAN':
            self.advance()
            return Boolean(tok.value)
        elif tok.type == 'GETSTRING':
            self.advance()
            return getString(tok.value)
        elif tok.type == 'GETINT':
            self.advance()
            return getInt(tok.value)
        elif tok.type == 'GETFLOAT':
            self.advance()
            return getFloat(tok.value)
        elif tok.type == 'LPAREN':
            self.advance()
            expr = self.expr()
            self.expect('RPAREN')
            return expr


        raise SyntaxError(f'Unexpected token {tok}')