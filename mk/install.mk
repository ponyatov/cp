.PHONY: install update
install: doc ref gz
	$(MAKE) update
update:
	sudo apt update
	sudo apt install -uy `cat apt.$(WS)` $(APT)
ref:
	$(REF)
gz:
	$(GZ)
