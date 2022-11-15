.PHONY: cards static update

STATIC_SERVER ?= krcg.org:projects/lackey.krcg.org/dist

static:
	rsync -rlptq --delete-after -e ssh plugin/ ${STATIC_SERVER}

update:
	pip install -U pip
	pip install -r cardgen/requirements.txt

cards:
	python -m cardgen
