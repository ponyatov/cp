
## data stack
D = []

## `( n -- )` @returns n
def pop(): return D.pop()

## `( -- n )` append to @ref D
def push(n): D.append(n)

## trace flag: dump command execution
trace = True


def nop():
    if trace:
        print('nop')


def halt():
    if trace:
        print('halt')


def mkdir():
    name = pop()
    if trace:
        print('mkdir {name}')


if __name__ == '__main__':
    nop()
    halt()
