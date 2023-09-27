.PHONY: all

sources := $(shell ls *.tape)

all:
	@for s in $(sources) ; do \
		make "$${s%.*}"; \
	done

%:
	@echo $@
	vhs < $@.tape
