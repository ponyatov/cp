## @file
## metaL: [meta]programming [L]anguage / [L]ayer
##
## (c) Dmitry Ponyatov <<dponyatov@gmail.com>> 2020 MIT

## @defgroup metaL metaL
## object graph database / homoiconic language

import config

import os, sys, re
import datetime as dt

## @defgroup core Core
## @ingroup metaL

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

    ## Python types boxing
    def box(self, that):
        if isinstance(that, Object): return that
        if isinstance(that,    int): return Integer(that)
        if isinstance(that,    str): return String(that)
        if that == None            : return Nil()
        # unknown
        raise TypeError(['box', type(that), that])

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
        if id(self) in cycle: return ret + ' _/'
        else: cycle += [id(self)]
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
        gid = '' if test else ' ' + self.gid()
        return f'{prefix}<{self.tag()}:{self.val()}>{gid}'

    ## `<T:` object class/tag
    def tag(self): return self.__class__.__name__.lower()
    ## `:V>` object value for dump
    def val(self): return f'{self.value}'

    ## @name de/serialize

    ## [g]lobal [id] /unical identifier/
    def gid(self): return f'@{id(self):x}'

    def json(self, depth=0, prefix=''):
        ret = f'{prefix}{tab*depth}{{\n'
        ret += f'{tab*(depth+1)}"type":"{self.__class__.__name__}",\n'
        ret += f'{tab*(depth+1)}"value":"{self.value}",\n'
        # slot{}
        for i in self.slot:
            ret += self[i].json(depth + 1, f'{tab*(depth+1)}"{i}":')
        # nest[]
        ret += f'{tab*(depth+1)}"nest":[\n'
        for j in self.nest:
            ret += j.json(depth + 1)
        ret += f'{tab*(depth+1)}]\n'
        # subtree
        ret += f'{tab*depth}}},\n'
        return ret

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
        that = self.box(that)
        if isinstance(key, str): self.slot[key] = that; return self
        if isinstance(key, int): self.nest[key] = that; return self
        raise TypeError([type(key), key, that])

    ## `A << B -> A[B.type] = B`
    def __lshift__(self, that):
        return self.__setitem__(that.tag(), that)

    ## `A >> B -> A[B.value] = B`
    def __rshift__(self, that):
        return self.__setitem__(that.val(), that)

    ## `A // B -> A.push(B)`
    def __floordiv__(self, that):
        that = self.box(that)
        assert isinstance(that, Object)
        self.nest += [that]; return self

## @}


## @defgroup Primitive Primitive
## @ingroup core
## @{

class Primitive(Object):
    def eval(self, env): return self
    def html(self): return f'{self.value}'

class Nil(Primitive):
    fromstr = ['', '-', '--', '-?-']
    html = '\u2014'
    def __init__(self): super().__init__('')

## @defgroup Number Number
## numbers
## @{

## floating point
class Number(Primitive):
    def __init__(self, V, prec=4):
        if V == None: Primitive.__init__(self, V)
        else: Primitive.__init__(self, float(V))
        ## precision: digits after `.`
        self.prec = prec

    def val(self):
        if self.value == None: return Nil.html
        if isinstance(self.value,float):
            if not self.prec:
                return f'{int(self.value)}'
            else:
                return f'{round(self.value,self.prec)}'
        raise TypeError(['val',type(self.value),self.value])

    ## `+`
    def __add__(self, that):
        if isinstance(that, Number) or isinstance(that, Integer):
            return Number(self.value + that.value)
        raise TypeError([type(that), that])

class Integer(Number):
    def __init__(self, V):
        self.prec = 0
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

    def val(self):
        if self.value == None: return Nil.html
        if isinstance(self.value,int):
            return f'{self.value}'
        raise TypeError(['val',type(self.value),self.value])

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
## measurement unit (physical value)
## @{

class Unit(Number):
    suffix = '?'
    ## rex for removing suffix from some '"1234 suffix"`
    delunitrex = '^$'

    def __init__(self, V=None, prec=4):
        if isinstance(V, str):
            V = re.sub(self.__class__.delunitrex, '', V)
            V = re.sub(r',', r'.', V)
            if V in Nil.fromstr: V = None
        super().__init__(V, prec)

    def __eq__(self, that):
        raise NotImplementedError([Unit, that])

## градус Цельсия
class C(Unit):
    suffix = '\u2103'

## сантиметры
class cm(Unit):
    suffix = 'см'
    delunitrex = r'\s*(см)$'

## метры
class m(Unit):
    suffix = 'м'

## метры в Балтийской системе высот
class mBS(m):
    suffix = 'мБс'
    delunitrex = r'\s*(мБс|мБС)$'

## метры кубические/секунду (?)
class m3c(Unit):
    suffix = 'м\u00B3/c'

## метры/секунду (ветер)
class ms(Unit):
    suffix = 'м/c'

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

## @}

## @defgroup Active Active
## executable data
## @ingroup core
## @{

class Active(Object): pass

## @defgroup Env Env
## environment = namespace
## @{

## environment = namespace
class Env(Active, Map): pass


## global environment
glob = Env('global'); glob << glob >> glob

## @}

class Meta(Object): pass

class S(Meta, String): pass

class Sec(Meta): pass

class Class(Meta): pass


## @defgroup IO IO
## @ingroup core
## @{

## input/output
class IO(Object): pass

class Time(IO):
    def __init__(self):
        self.now = dt.datetime.now()
        super().__init__(f'{self.now}')
        self.isodate = self.now.strftime('%Y-%m-%d')
        self.date = self.now.strftime('%Y-%m-%d')
        self.time = self.now.strftime('%H:%M:%S')

    def json(self):
        return {"isodate": self.isodate, "date": self.date, "time": self.time}

## file path
class Path(IO): pass

## directory
class Dir(IO): pass

## file
class File(IO): pass

## @defgroup Net Net
## network
## @{

class Net(IO): pass

class Socket(Net): pass

## IP address
class Ip(Net): pass

## IP Port
class Port(Net, Integer): pass

class EMail(Net):
    def html(self):
        return f'&lt;<a href="mailto:{self.value}">{self.value}</a>&gt;'

class Url(Net):
    def html(self):
        return f'<a href="{self.value}">{self.value}</a>'

## @}

## @defgroup GUI GUI
## abstract graphical user interface
## @{

class GUI(Object):
    def onch(self, event='onchange', getval='this.value'):
        ret = f'{event}="gui_onchange(\'{self.gid()}\',\'{self.value}\',{getval})"'
        return ret

    def grammarly(self, state=False):
        return f'data-gramm={"true" if state else "false"}'


gui = GUI('view'); glob << gui

class View(GUI):
    def __init__(self, htmlid, model=None):
        assert htmlid
        super().__init__(htmlid)
        if isinstance(model, str):
            model = re.sub(r'[ \t\r\n]+$', r'', model, re.S)
            model = re.sub(r'\s*(°C|°С|°)', '\u2009\u2103', model, re.S)
        if model:
            self // model
            try: self.prefix = model.prefix
            except AttributeError: self.prefix = ''
            try: self.suffix = model.suffix
            except AttributeError: self.suffix = ''
        gui[self.gid()] = self # view registry

    def onchange(self, value):
        sio = glob['web']['engine'].sio
        try:
            self[0].value = self[0].__class__(value).value
            sio.emit('gui/changed',[self.gid(),self.value,self[0].val()])
        except ValueError:
            sio.emit('gui/error',[self.gid(),self.value,value])

class TextArea(View):
    def html(self):
        val = ''.join(map(lambda i: i.html(), self))
        rows = max(3, len(val.split('\n')))
        return f'<textarea id="{self.value}" rows={rows} {self.grammarly()} {self.onch()}>{val}</textarea>'

class Input(View):
    def html(self):
        return f'<input id="{self.value}" {self.grammarly()} {self.onch()} value="{self[0].val()}">{self[0].suffix}</input>'

## @}

## @defgroup Web Web
## GIS/Geolocation
## @{

import shapefile as shp



## @}

## @defgroup Web Web
## Web interface
## @ingroup core
## @{

class Web(Net): pass


glob << Web('interface')

import flask
from flask_socketio import SocketIO

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

## Web server engine (back web server + ....)
class Engine(Web): pass

## Flask wrapper
class Flask(Engine):
    def __init__(self):
        super().__init__(self.tag())
        glob['web']['engine'] = self
        self.app = flask.Flask(__name__)
        self.app.config['SECRET_KEY'] = config.SECRET_KEY
        self.sio = SocketIO(self.app)

    def eval(self, env):
        self.route(env)
        self.socket(env)
        self.inotify()
        self.sio.run(self.app, debug=True, host=config.HOST, port=config.PORT)

    def lookup(self, path):
        item = glob
        for i in filter(lambda i: i, path.split('/')): item = item[i]
        return item

    ## classical HTTP
    def route(self, env):
        @self.app.after_request
        def force_no_caching(req):
            req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            req.headers["Pragma"] = "no-cache"
            req.headers["Expires"] = "0"
            req.headers['Cache-Control'] = 'public, max-age=0'
            return req

        @self.app.route('/dump/<path:path>')
        @self.app.route('/dump/')
        def dump(path=''):
            return flask.render_template('dump.html',
                                         glob=glob, env=self.lookup(path),
                                         app=glob['app'], user=glob['app']['user'])

        @self.app.route('/<path:path>')
        @self.app.route('/')
        def html(path=''):
            return flask.render_template('index.html',
                                         glob=glob, env=self.lookup(path),
                                         app=glob['app'], user=glob['app']['user'])

    ## SocketIO messaging
    def socket(self, env):

        @self.sio.on('connect')
        def connect():
            localtime()

        @self.sio.on('localtime')
        def localtime():
            self.sio.emit('localtime', Time().json(), broadcast=True)

        @self.sio.on('gui/onchange')
        def gui_textarea(msg):
            print('gui/onchange', msg)
            gid, name, value = msg
            gui[gid].onchange(value)

    def inotify(self):
        watch = Observer(); sio = self.sio

        class event_handler(FileSystemEventHandler):
            def on_closed(self, event):
                if not event.is_directory:
                    sio.emit('reload', f'{event}')
        watch.schedule(event_handler(), 'static', recursive=True)
        watch.schedule(event_handler(), 'templates', recursive=True)
        watch.start()



