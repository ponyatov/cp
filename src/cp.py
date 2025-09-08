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

if __name__ == '__main__':
    nop()
    halt()
