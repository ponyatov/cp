# \ var
MODULE  = $(notdir $(CURDIR))
OS      = $(shell uname -s)
MACHINE = $(shell uname -m)
NOW     = $(shell date +%d%m%y)
REL     = $(shell git rev-parse --short=4 HEAD)
CORES   = $(shell grep processor /proc/cpuinfo| wc -l)
# / var

# \ dir
CWD     = $(CURDIR)
BIN     = $(CWD)/bin
DOC     = $(CWD)/doc
TMP     = $(CWD)/tmp
SRC     = $(CWD)/src
GZ      = $(HOME)/gz
# / dir

# \ tool
CURL    = curl -L -o
PY      = bin/python3
PIP     = bin/pip3
PEP     = bin/autopep8
PYT     = bin/pytest
ERL     = erl
ERLC    = erlc
MIX     = mix
IEX     = iex
NIMB    = nimble
NIMP	= nimpretty
# / tool

# \ src
P      += config.py
Y      += $(MODULE).py test_$(MODULE).py
Y      += metaL.py test_metaL.py
Y      += EDS.py
N      += src/$(MODULE).nim src/metainfo.nim
N      += src/syntax/generic.nim src/syntax/Nim.nim
N      += src/syntax/Makefile.nim src/syntax/Python.nim
N      += src/syntax/metaL.nim src/parser.nim
S      += $(MODULE).nimble nim.cfg
S      += $(Y) $(N)
# / src

# \ obj
# / obj
# \ cfg
# / cfg

# \ all
.PHONY: all
all: $(PY) metaL.py
	$^ $@
all:
	time $(NIMB) build --usenimcache --nimcache:$(TMP)/nim
#	 --verbose
	time $(NIMB) run
	$(MAKE) format

.PHONY: web
web: $(PY) metaL.py
	$^ $@

.PHONY: test
test: $(PYT) test_metaL.py
	$^
	$(MAKE) format
	$(MIX)  test

.PHONY: format
format: $(PEP)
	$(MIX) format
$(PEP): $(Y)
	$@ --ignore=E26,E302,E401,E402,E701,E702 --in-place $? && touch $@
format: $(N)
	$(NIMP) --indent:2 $<

# \ elixir
.PHONY: iex
iex:
	$(IEX) -S mix phx.server
	$(MAKE) format
	$(MAKE) $@
# / elixir
# / all

# \ nginx
NGINX   = $(CWD)/local/bin/nginx
# / nginx

# \ doc

.PHONY: doxy
doxy: doxy.gen
	doxygen doxy.gen 1>/dev/null

.PHONY: doc
doc: \
	doc/SICP_ru.pdf doc/Dragon_ru.pdf \
	doc/Erlang/LYSE_ru.pdf doc/Erlang/Armstrong_ru.pdf \
	doc/Erlang/ElixirInAction.pdf doc/Erlang/Phoenix.pdf \
	doc/NimInAction.pdf

doc/SICP_ru.pdf:
	$(CURL) $@ https://newstar.rinet.ru/~goga/sicp/sicp.pdf
doc/Dragon_ru.pdf:
	$(CURL) $@ https://linux-doc.ru/programming/assembler/book/compilers.pdf
doc/Erlang/LYSE_ru.pdf:
	$(CURL) $@ https://github.com/mpyrozhok/learnyousomeerlang_ru/raw/master/pdf/learnyousomeerlang_ru.pdf
doc/Erlang/Armstrong_ru.pdf:
	$(CURL) $@ https://github.com/dyp2000/Russian-Armstrong-Erlang/raw/master/pdf/fullbook.pdf
doc/Erlang/ElixirInAction.pdf:
	$(CURL) $@ https://github.com/levunguyen/CGDN-Ebooks/raw/master/Java/Elixir%20in%20Action%2C%202nd%20Edition.pdf
doc/Erlang/Phoenix.pdf:
	$(CURL) $@ http://www.r-5.org/files/books/computers/languages/erlang/phoenix/Chris_McCord_Bruce_Tate_Jose_Valim-Programming_Phoenix-EN.pdf
doc/NimInAction.pdf:
	$(CURL) $@ https://nim.nosdn.127.net/MTY3NjMzODI=/bmltd18wXzE1NzYxNTc0NDQwMTdfMWU4MDhiODUtZDM0Ni00OWFlLWJjYzUtMDg2ODIxMmMzMTIw
# / doc

# \ install
.PHONY: install
install: $(OS)_install js doc
	$(MAKE) $(PIP)
	$(MIX) deps.get
	$(MAKE) update
	$(MIX) archive.install hex phx_new 1.5.8
	$(MIX) ecto.create
.PHONY: update
update: $(OS)_update
	$(PIP) install -U    pip autopep8
	$(PIP) install -U -r requirements.txt
	$(MIX) local.hex local.rebar
	$(MIX) deps.update --all

.PHONY: Linux_install Linux_update
Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt apt.dev`
# \ py
$(PY) $(PIP):
	python3 -m venv .
	$(MAKE) update
$(PYT):
	$(PIP) install -U pytest
# / py
# \ js
.PHONY: js
js: \
	static/js/bootstrap.min.css static/js/bootstrap.dark.css \
	static/js/bootstrap.min.js  static/js/jquery.min.js \
	static/js/html5shiv.min.js  static/js/respond.min.js \
	static/js/socket.io.min.js  static/js/peg.min.js \
	static/js/leaflet/leaflet.js static/js/leaflet/leaflet.css

CDNJS = https://cdnjs.cloudflare.com/ajax/libs

JQUERY_VER = 3.6.0
static/js/jquery.min.js:
	$(CURL) $@ $(CDNJS)/jquery/$(JQUERY_VER)/jquery.min.js

BOOTSTRAP_VER = 4.6.0
BOOTSTRAP_CDN = $(CDNJS)/twitter-bootstrap/$(BOOTSTRAP_VER)
static/js/bootstrap.min.css: static/js/bootstrap.min.css.map
	$(CURL) $@ $(BOOTSTRAP_CDN)/css/bootstrap.min.css
static/js/bootstrap.min.css.map:
	$(CURL) $@ $(BOOTSTRAP_CDN)/css/bootstrap.min.css.map
static/js/bootstrap.dark.css:
	$(CURL) $@ https://bootswatch.com/4/darkly/bootstrap.min.css
static/js/bootstrap.min.js: static/js/bootstrap.min.js.map
	$(CURL) $@ $(BOOTSTRAP_CDN)/js/bootstrap.min.js
static/js/bootstrap.min.js.map:
	$(CURL) $@ $(BOOTSTRAP_CDN)/js/bootstrap.min.js.map

static/js/html5shiv.min.js:
	$(CURL) $@ $(CDNJS)/html5shiv/3.7.3/html5shiv.min.js
static/js/respond.min.js:
	$(CURL) $@ $(CDNJS)/respond.js/1.4.2/respond.min.js

SOCKETIO_VER = 3.1.2
SOCKETIO_CDN = $(CDNJS)/socket.io/$(SOCKETIO_VER)
static/js/socket.io.min.js: static/js/socket.io.min.js.map
	$(CURL) $@ $(SOCKETIO_CDN)/socket.io.min.js
static/js/socket.io.min.js.map:
	$(CURL) $@ $(SOCKETIO_CDN)/socket.io.min.js.map

PEGJS_VER = 0.10.0
static/js/peg.min.js:
	$(CURL) $@ https://github.com/pegjs/pegjs/releases/download/v$(PEGJS_VER)/peg-$(PEGJS_VER).min.js

LEAFLET_VER = 1.7.1
LEAFLET_GZ  = tmp/leaflet.zip
LEAFLET_CDN = http://cdn.leafletjs.com/leaflet/v$(LEAFLET_VER)/leaflet.zip
$(LEAFLET_GZ):
	$(CURL) $@ $(LEAFLET_CDN)
static/js/leaflet/leaflet.css: static/js/leaflet/leaflet.js
	touch $@
static/js/leaflet/leaflet.js: $(LEAFLET_GZ)
	unzip -d static/js/leaflet $< leaflet.css leaflet.js* images/* && touch $@

# / js
# / install

# \ merge
MERGE += README.md Makefile .gitignore apt.txt apt.dev LICENSE doxy.gen $(S)
MERGE += .vscode bin doc tmp src
MERGE += lib test mix.exs .formatter.exs
MERGE += requirements.txt
MERGE += geo

.PHONY: main
main:
	git push -v
	git checkout $@
	git pull -v
	git checkout shadow -- $(MERGE)
.PHONY: shadow
shadow:
	git push -v
	git checkout $@
	git pull -v
.PHONY: release
release:
	git tag $(NOW)-$(REL)
	git push -v && git push -v --tags
	$(MAKE) shadow
.PHONY: zip
zip:
	git archive \
		--format zip \
		--output $(TMP)/$(MODULE)_$(NOW)_$(REL).src.zip \
	HEAD
# / merge
