.PHONY: static update cards list test

STATIC_SERVER ?= krcg.org:projects/lackey.krcg.org/dist
DATE := $(shell date -u +"%F")

static:
	rsync -rlptq --delete-after -e ssh plugin/ ${STATIC_SERVER}

update:
	pip install -U pip
	pip install -r cardgen/requirements.txt

cards: update
	python -m cardgen

list: cards
	echo 'version = "${DATE}"' > updatelist/version.py
	python -m updatelist

test:
	cp -r plugin/* /Applications/LackeyCCG/plugins/vtes-test 