PACKAGE_VERSION = master

LINT_SOURCES = .

PYTHON = python

all:	wg-srle

clean:
	find . -name '*.tmp' -delete
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -f wg_srle/buildinfo_override.py
	rm -fr build *.egg-info

sdist:		all
	$(NULL) \
		PACKAGE_VERSION="$(PACKAGE_VERSION)" \
		$(PYTHON) ./setup.py \
			sdist \
			$(NULL)

check:	all
	$(PYTHON) ./setup.py test

wg-srle:
	$(PYTHON) -m pyflakes $(LINT_SOURCES)
	if $(PYTHON) -m pycodestyle --version > /dev/null; then \
		$(PYTHON) -m pycodestyle $(LINT_SOURCES); \
	else \
		$(PYTHON) -m pep8 $(LINT_SOURCES); \
	fi

	$(NULL) \
		PACKAGE_VERSION="$(PACKAGE_VERSION)" \
		$(PYTHON) ./setup.py \
			check \
			build \
			$(NULL)
