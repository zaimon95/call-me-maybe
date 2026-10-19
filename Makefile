# Makefile — A-Maze-ing
# RESPONSABLE: Otto (configurer les chemins et dépendances)

PYTHON = python3
MAIN   = call_me_maybe.py
CONFIG = config.txt

.PHONY: install run debug lint lint-strict clean

## Installe les dépendances du projet
install:
	pip install -r requirements.txt

## Lance le programme principal avec config.txt
run:
	$(PYTHON) $(MAIN) $(CONFIG)

## Lance en mode debug (pdb)
debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

## Nettoyage des fichiers temporaires
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	rm -rf dist/ build/ *.egg-info/

## Linting: flake8 + mypy (flags obligatoires du sujet)
lint:
	flake8 .flake8
	mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

## Linting strict (optionnel mais recommandé)
lint-strict:
	flake8 .
	mypy . --strict:warn-unused-ignores
