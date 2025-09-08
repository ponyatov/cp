import os

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

## `( name -- )` make directory
def mkdir():
    name = pop()
    if trace: print('mkdir {name}')
    os.mkdir(name)

## @defgroup lexer
## @{
import ply.lex as lex
lexer = lex.lex()
## @}

## @defgroup parser
## @{
import ply.yacc as yacc
parser = yacc.yacc(debug=False, write_tables=False)
## @}

## `( -- )` Read-Eval-Print-Loop
def repl():
    if trace: print('repl')
    while True:
        cmd = input('> ')
        if not cmd: break
        parser.parse(cmd)

## script entry
if __name__ == '__main__':
    nop()
    halt()
    repl()
