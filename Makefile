VENV      = .venv
PYTHON    = $(VENV)/bin/python3
MAIN      = src
INSTALLED = $(VENV)/.installed
OUTPUT    = data/output

# Directories that are not our code and must never be linted.
# flake8 takes a comma-separated list of names, mypy takes regexes.
FLAKE8_EXCLUDE = --extend-exclude $(VENV),llm_sdk
MYPY_EXCLUDE   = --exclude '^\.venv/' --exclude '^llm_sdk/'

.PHONY: install run debug lint lint-strict clean fclean

install: $(INSTALLED)

# Real file target, created only once every package is installed: the
# install is redone if it never completed, or if pyproject.toml or
# uv.lock is newer than the last successful install.
$(INSTALLED): pyproject.toml uv.lock
	uv sync
	touch $(INSTALLED)

run: $(INSTALLED)
	$(PYTHON) -m $(MAIN) $(ARGS)

debug: $(INSTALLED)
	$(PYTHON) -m pdb -m $(MAIN) $(ARGS)

clean:
	find . -type d -name __pycache__ -not -path "./$(VENV)/*" \
		-exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -not -path "./$(VENV)/*" -delete

fclean: clean
	rm -rf $(VENV) $(OUTPUT)

lint: $(INSTALLED)
	$(PYTHON) -m flake8 . $(FLAKE8_EXCLUDE)
	$(PYTHON) -m mypy . \
		$(MYPY_EXCLUDE) \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict: $(INSTALLED)
	$(PYTHON) -m flake8 . $(FLAKE8_EXCLUDE)
	$(PYTHON) -m mypy . $(MYPY_EXCLUDE) --strict
