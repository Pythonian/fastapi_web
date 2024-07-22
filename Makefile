# Makefile for setting up the project

.DEFAULT_GOAL=help

# Define commands to be explicitly invoked
.PHONY: help hello venv install migrate check run clean

# Define the name of the virtual environment directory
VENV_DIR = .venv

# Define the python command for creating virtual environments
PYTHON = python3

# Define the pip executable within the virtual environment
PIP = $(VENV_DIR)/bin/pip

# Define the tox executable within the virtual environment
TOX = $(VENV_DIR)/bin/tox

# Define the pre-commit executable within the virtual environment
PRE_COMMIT = $(VENV_DIR)/bin/pre-commit

# Define the uvicorn executable within the virtual environment
UVICORN = $(VENV_DIR)/bin/uvicorn

# Define the alembic executable within the virtual environment
ALEMBIC = $(VENV_DIR)/bin/alembic

help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

hello: ## Hello, World!
	@echo "Hello, World!"

venv: ## Create a virtual environment
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created."

install: ## Install development dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	cp .env.example .env
	@echo "Development dependencies has been setup."

migrate: ## Run the database migration
	$(ALEMBIC) upgrade head

check: ## Run all checks using tox and pre-commit
	$(PIP) install tox==4.16.0 pre-commit==3.7.1
	$(TOX)
	$(PRE_COMMIT) install
	$(PRE_COMMIT) run --all-files
	@echo "All checks passed"

run: ## Run the development server
	$(UVICORN) main:app --reload

clean: ## Clean up the project
	@echo "Cleaning up the project of temporary files and directories..."
	@rm -rf $(VENV_DIR)
	@rm -rf .cache
	@rm -rf build
	@rm -rf htmlcov coverage.xml .coverage
	@rm -rf .tox
	@rm -rf *.log
	@rm -rf .mypy_cache
	@rm -rf .ruff_cache
	@rm -rf *.egg-info
	@rm -rf dist
	@find . -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@echo "Clean up successfully completed."
