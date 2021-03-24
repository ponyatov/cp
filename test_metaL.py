from metaL import *

hello = Object('hello')
def test_hello(): assert hello.test() == '\n<object:hello>'

world = Object('world')
def test_world():
    assert world.test() == '\n<object:world>'
    assert (hello // world).test() == '\n<object:hello>\n\t0: <object:world>'


left = Object('left')
def test_lshift():
    assert (hello << left).test(
    ) == '\n<object:hello>\n\tobject = <object:left>\n\t0: <object:world>'

