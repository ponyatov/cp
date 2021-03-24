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
S     += EDS.py
# / src
# \ obj
# / obj
# \ cfg
# / cfg
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
