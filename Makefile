.PHONY: static

STATIC_SERVER ?= krcg.org:projects/lackey.krcg.org/dist

static:
	rsync -rlptq --delete-after -e ssh plugin/ ${STATIC_SERVER}
