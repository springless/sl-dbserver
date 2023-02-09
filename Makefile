VENV_DIR := ./.venv
TEST_SERVER_PORT := 8000

rem-venv:
	-rm -rf $(VENV_DIR)

new-venv: rem-venv
	python3 -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/python -m pip install --upgrade pip
	$(VENV_DIR)/bin/python -m pip install -r requirements.txt
	$(VENV_DIR)/bin/python -m pip install -e ".[dev]"

build-release:
	-rm -rf dist
	$(VENV_DIR)/bin/python -m build .

test-server:
	$(VENV_DIR)/bin/uvicorn sl.dbserver.app:main --reload --port $(TEST_SERVER_PORT)

push-release: build-release
	$(VENV_DIR)/bin/twine upload dist/*

test-db:
	docker-compose up
