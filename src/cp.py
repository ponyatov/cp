import os, sys

## data stack
D = []

## vocabulary
W = {}

## `( n -- )` @returns n
def pop(): return D.pop()

## `( -- n )` append to @ref D
def push(n): D.append(n)

## trace flag: dump command execution
trace = True

## `( -- )` empty command: do nothing
def nop():
    if trace: print('nop')

## `( -- )` stop system
def halt():
    if trace: print('halt')
    sys.exit(0)

## `( -- )` dump system state
def dump():
    if trace: print('dump')
    print(D)

## `( name -- )` make directory
def mkdir():
    name = pop()
    if trace: print('mkdir {name}')
    os.mkdir(name)

## @defgroup lexer
## @{
import ply.lex as lex

tokens = ['INT', 'ID']

t_ignore = ' \t\r'

t_ignore_shebang = '\#!.*'
t_ignore_line_comment = '//.*'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_INT(t):
    r'[+\-]?\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_error(t): raise SyntaxError(t)

lexer = lex.lex()
## @}

## @defgroup parser
## @{
import ply.yacc as yacc

def p_REPL_none(p):
    ' REPL : '
    pass

def p_REPL_recur(p):
    ' REPL : REPL cmd '
    pass

def p_cmd_int(p):
    ' cmd : INT '
    push(int(p[1]))

def p_cmd_id(p):
    ' cmd : ID '
    push(p[1])

def p_error(p): raise SyntaxError(p)

parser = yacc.yacc(debug=False, write_tables=False)
## @}

## `( -- )` Read-Eval-Print-Loop
def repl():
    if trace: print('repl')
    while True:
        try:
            parser.parse(input('> '))
        except EOFError:
            halt()
        dump()

## script entry
if __name__ == '__main__':
    nop()
    halt()
    repl()
