VENV_DIR := ./.venv

rem-venv:
	-rm -rf $(VENV_DIR)

new-venv: rem-venv
	python3 -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/python -m pip install --upgrade pip
	$(VENV_DIR)/bin/python -m pip install -e ".[dev]"
