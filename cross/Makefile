APP = clock
HW  = qemu386

include   hw/$(HW).mk
include  cpu/$(CPU).mk
include arch/$(ARCH).mk

.PHONY: cross
cross:
	$(MAKE) Linux_install
	$(MAKE) gz

include ../Makefile

FW  = $(CWD)/firmware
SRC = $(TMP)/src


BUILDROOT_VER = 2021.02
BUILDROOT     = buildroot-$(BUILDROOT_VER)
BUILDROOT_GZ  = $(BUILDROOT).tar.gz

.PHONY: br
br: $(BUILDROOT)/README
	cd $(BUILDROOT) ;\
	rm .config ; make allnoconfig ;\
	cat ../all.kernel													\
		../arch/$(ARCH).kernel ../cpu/$(CPU).kernel ../hw/$(HW).kernel	\
		../app/$(APP).bkernel 											>> .config.kernel ;\
	cat ../all.br											\
		../arch/$(ARCH).br ../cpu/$(CPU).br ../hw/$(HW).br	\
		../app/$(APP).br 									>> .config ;\
	echo "BR2_TARGET_GENERIC_HOSTNAME=\"$(APP)\"" 			>> .config ;\
	make menuconfig ;\
	make linux-menuconfig ;\
	make

$(BUILDROOT)/README: $(GZ)/$(BUILDROOT_GZ)
	tar zx < $< && touch $@

.PHONY: gz
gz: \
	$(GZ)/$(BUILDROOT_GZ)

$(GZ)/$(BUILDROOT_GZ):
	$(CURL) $@ https://github.com/buildroot/buildroot/archive/refs/tags/$(BUILDROOT_VER).tar.gz
