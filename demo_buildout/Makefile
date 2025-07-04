.PHONY: all
all: bin/instance
	bin/instance run test.py

bin/instance: .venv/bin/buildout
	.venv/bin/buildout -D

.venv/bin/pip:
	uv venv --seed .venv

.venv/bin/buildout: .venv/bin/pip
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install -e ..

.PHONY: clean
clean:
	rm -rf .installed.cfg .venv bin develop-eggs eggs parts var
