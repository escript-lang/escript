import re
from collections import namedtuple

Token = namedtuple('Token', ['type', 'value'])

KEYWORDS = {'print', 'println', 'getString', 'getInt', 'getFloat', 'info'}

TOKEN_SPECIFICATION = [
    ('COMMENT', r'//.*'),
    ('NUMBER', r'\d+(\.\d*)?'), # числа
    ('STRING', r'"[^"\\]*(?:\\.[^"\\]*)*"'),
    ('BOOLEAN', r'True|False'),
    ('TYPE_OP', r':'),
    ('ID', r'[a-zA-Z_][a-zA-Z_0-9]*'), # идентификаторы (переменные)
    ('OP', r'[:]=|==|!=|<=|>=|\*\*|[+\-*/=<>]'), # операции (присвоение и тд)
    ('COMMA', r','),
    ('SKIP', r'[ \t]+'), # пропускать пробелы и табуляции
    ('NEWLINE', r'\n'), # новая строка
    ('LPAREN', r'\('), # открывающая скобка
    ('RPAREN', r'\)'), # закрывающая скобка
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('MISMATCH', r'.'), # всё остальное мисмач (несовпадение)
]

def lexer(code):
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION)
    for match in re.finditer(tok_regex, code):
        kind = match.lastgroup
        value = match.group()

        match kind:
            case 'NUMBER':
                yield Token(kind, float(value) if '.' in value else int(value))
            case 'STRING':
                yield Token(kind, str(value).strip("\""))
            case 'BOOLEAN':
                yield Token(kind, bool(True) if value == 'True' else bool(False))
            case 'ID':
                yield Token(value.upper() if value in KEYWORDS else 'ID', value)
            case 'NEWLINE' | 'SKIP':
                continue
            case 'LPAREN' | 'RPAREN' | 'OP' | 'LBRACE' | 'RBRACE' | 'TYPE_OP':
                yield Token(kind, value)
            case 'MISMATCH':
                raise SyntaxError(f'Unexpected character: {value!r}')