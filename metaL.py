## @file
## metaL: [meta]programming [L]anguage / [L]ayer
##
## (c) Dmitry Ponyatov <<dponyatov@gmail.com>> 2020 MIT

## @defgroup metaL metaL
## object graph database / homoiconic language

import config

import os, sys, re
import datetime as dt

## @defgroup core the Core

## @defgroup Object Object
## base object graph node class = Marvin Minsky's Frame
## @ingroup core
## @{

## base object graph node class = Marvin Minsky's Frame
class Object:
    def __init__(self, V):
        if isinstance(V, Object): V = V.value
        ## scalar value: name, number, string
        self.value = V
        ## slot{}s = attributes = namespace = associative array = dict = hash map
        self.slot = {}
        ## nest[]ed subgraphs = ordered container = vector = stack = queue = AST
        self.nest = []

    ## @name text dump

    ## `print` callback
    def __repr__(self): return self.dump()

    ## use dumps w/o hashes
    def test(self): return self.dump(test=True)

    ## full text tree dump
    def dump(self, cycle=[], depth=0, prefix='', test=False):
        # head
        ret = self.pad(depth) + self.head(prefix, test)
        # cycle
        if not depth: cycle = []
        if self in cycle: return ret + ' _/'
        else: cycle += [self]
        # slot{}s
        for i in self.keys():
            ret += self[i].dump(cycle, depth + 1, f'{i} = ', test)
        # nest[]ed
        for j, k in enumerate(self.nest):
            ret += k.dump(cycle, depth + 1, f'{j}: ', test)
        # subtree
        return ret

    ## tree padding
    def pad(self, depth): return '\n' + '\t' * depth

    ## short `<T:V>` header-only dump
    def head(self, prefix='', test=False):
        gid = '' if test else f' @{self.gid()}'
        return f'{prefix}<{self.tag()}:{self.val()}>{gid}'

    ## `<T:` object class/tag
    def tag(self): return self.__class__.__name__.lower()
    ## `:V>` object value for dump
    def val(self): return f'{self.value}'

    ## @name serialization

    def gid(self): return f'@{id(self):x}'

    ## @name operator

    ## `A.keys()` ordered
    def keys(self):
        return sorted(self.slot.keys())

    ## iterator
    def iter(self): return iter(self.nest)

    ## `A[key]`
    def __getitem__(self, key):
        if isinstance(key, str): return self.slot[key]
        if isinstance(key, int): return self.nest[key]
        raise TypeError(key)

    ## `A[key] = B`
    def __setitem__(self, key, that):
        assert isinstance(key, str) or isinstance(key, int)
        if isinstance(that, int): that = Integer(that)
        if isinstance(that, str): that = String(that)
        assert isinstance(that, Object)
        self.slot[key] = that; return self

    ## `A << B -> A[B.type] = B`
    def __lshift__(self, that):
        return self.__setitem__(that.tag(), that)

    ## `A >> B -> A[B.value] = B`
    def __rshift__(self, that):
        return self.__setitem__(that.val(), that)

    ## `A // B -> A.push(B)`
    def __floordiv__(self, that):
        if isinstance(that, str): that = String(that)
        if isinstance(that, int): that = Integer(that)
        assert isinstance(that, Object)
        self.nest += [that]; return self

## @}

class Env(Object): pass


glob = Env('global'); glob << glob >> glob


## @defgroup Primitive Primitive
## @ingroup core
## @{

class Primitive(Object):
    def eval(self, env): return self
    def html(self): return f'{self.value}'

## @defgroup Number Number
## numbers
## @{

## floating point
class Number(Primitive):
    def __init__(self, V, prec=4):
        Primitive.__init__(self, float(V))
        ## precision: digits after `.`
        self.prec = 4

    def val(self): return f'{round(self.value,self.prec)}'

    ## `+`
    def __add__(self, that):
        if isinstance(that, Number) or isinstance(that, Integer):
            return Number(self.value + that.value)
        raise TypeError([type(that), that])

class Integer(Number):
    def __init__(self, V):
        if isinstance(V, int) or isinstance(V, float):
            Primitive.__init__(self, int(V))
        elif '.' in V:
            Primitive.__init__(self, int(float(V)))
        elif 'x' in V:
            Hex.__init__(self, V)
        elif 'b' in V:
            Bin.__init__(self, V)
        else:
            Primitive.__init__(self, int(V))

    def __truediv__(self, that):
        if isinstance(that, Number) or isinstance(that, Integer):
            return Number(self.value / that.value)
        raise TypeError([type(that), that])

class Hex(Integer):
    def __init__(self, V):
        super().__init__(int(V, 0x10))

class Bin(Integer):
    def __init__(self, V):
        super().__init__(int(V, 0x02))


## @}

## @defgroup String String
## @{

class String(Primitive):
    def val(self):
        ret = ''
        for c in self.value:
            if c == '\n': ret += '\\n'
            elif c == '\t': ret += '\\t'
            else: ret += c
        return ret

## @}

## @defgroup Name Name
## variable name
## @{

class Name(Primitive): pass

## @}

## @defgroup Unit Unit
## data container
## @ingroup core
## @{

## @}

## @}

## @defgroup Container Container
## data container
## @ingroup core
## @{


class Container(Object): pass

## ordered container
class Vector(Container): pass

## associative array
class Map(Container): pass

## unical set
class Set(Container): pass

## LIFO
class Stack(Container): pass

## FIFO
class Queue(Container): pass

class Meta(Object):
    pass

class S(Primitive):

class Sec(Primitive):

class Class(Meta):



