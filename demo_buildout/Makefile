.PHONY: all
all: bin/py
	bin/py test.py

bin/py: .venv/bin/buildout
	.venv/bin/buildout

.venv/bin/pip:
	python3 -m venv .venv

.venv/bin/buildout: .venv/bin/pip
	.venv/bin/pip install -r https://dist.plone.org/release/6.1-latest/requirements.txt
	.venv/bin/pip install -e ..
