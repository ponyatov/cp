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

def test_num_11(): assert Number('11').test() == '\n<number:11.0>'

def test_int_11(): assert Integer('11.1').test() == '\n<integer:11>'
# def test_hex_11(): assert Integer('0x11').test() == '\n<hex:17>'
# def test_bin_11(): assert Integer('0b11').test() == '\n<bin:3>'

def test_env():
    assert glob.test() ==\
        '\n<env:global>' +\
        '\n\tenv = <env:global> _/' +\
        '\n\tglobal = <env:global> _/'
