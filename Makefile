# \ var
MODULE = $(notdir $(CURDIR))
OS     = $(shell uname -s)
NOW    = $(shell date +%d%m%y)
REL    = $(shell git rev-parse --short=4 HEAD)
CORES  = $(shell grep processor /proc/cpuinfo| wc -l)
# / var

# \ dir
CWD    = $(CURDIR)
BIN    = $(CWD)/bin
DOC    = $(CWD)/doc
TMP    = $(CWD)/tmp
# / dir

# \ tool
CURL   = curl -L -o
PY     = bin/python3
PIP    = bin/pip3
PEP    = bin/autopep8
PYT    = bin/pytest
ERL    = erl
ERLC   = erlc
MIX    = mix
IEX    = iex
# / tool

# \ src
P     += config.py
S     += $(MODULE).py test_$(MODULE).py
S     += metaL.py test_metaL.py
S     += EDS.py
# / src

# \ obj
# / obj
# \ cfg
# / cfg

# \ all
.PHONY: all
all: $(PY) metaL.py
	$^ $@
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
$(PEP): $(S)
	$@ --ignore=E26,E302,E401,E402,E701,E702 --in-place $? && touch $@

# \ elixir
.PHONY: iex
iex:
	$(IEX) -S $(MIX)
# / elixir
# / all

# \ doc
.PHONY: doc
doc: \
	doc/SICP_ru.pdf doc/Armstrong_ru.pdf
doc/SICP_ru.pdf:
	$(CURL) $@ https://newstar.rinet.ru/~goga/sicp/sicp.pdf
doc/Armstrong_ru.pdf:
	$(CURL) $@ https://github.com/dyp2000/Russian-Armstrong-Erlang/raw/master/pdf/fullbook.pdf
# / doc

# \ install
.PHONY: install
install: $(OS)_install js doc
	$(MAKE) $(PIP)
	$(MAKE) update
.PHONY: update
update: $(OS)_update
	$(PIP) install -U    pip autopep8
	$(PIP) install -U -r requirements.txt
	$(MIX) deps.get
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
	static/js/socket.io.min.js  static/js/peg.min.js

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
# / js
# / install


