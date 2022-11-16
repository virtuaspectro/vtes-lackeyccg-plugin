.PHONY: static update cards list test

SERVER_SSH ?= krcg.org:projects/lackey.krcg.org/dist
SERVER_HTTP ?= https://lackey.krcg.org
DATE := $(shell date -u +"%F")

static:
	rsync -rlptq --delete-after -e ssh plugin/ ${SERVER_SSH}

update:
	pip install -U pip
	pip install -r cardgen/requirements.txt

cards: update
	python -m cardgen

list: cards
	echo 'version = "${DATE}"' > updatelist/version.py
	LACKEY_SERVER_ROOT=${SERVER_HTTP} python -m updatelist

test:
	cp -r plugin/* /Applications/LackeyCCG/plugins/vtes-test
