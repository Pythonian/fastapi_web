# Makefile for setting up the project

.DEFAULT_GOAL=help

# Define commands to be explicitly invoked
.PHONY: all venv install check clean help run migrate hello

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

hello: ## Hello, World!
	@echo "Hello, World!"

# Setup the development environment
all: venv install check

venv: ## Create a virtual environment
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created."

install: ## Install development packages
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PRE_COMMIT) install
	cp .env.example .env
	@echo "Development packages has been setup."

check: ## Run all checks using tox and pre-commit
	$(TOX)
	$(PRE_COMMIT) run --all-files
	@echo "All checks passed"

clean: ## Clean up the project of unneeded files
	@echo "Cleaning up the project of unneeded files..."
	@rm -rf $(VENV_DIR)
	@rm -rf .cache
	@rm -rf htmlcov coverage.xml .coverage
	@rm -rf .tox
	@rm -rf .mypy_cache
	@rm -rf .ruff_cache
	@rm -rf *.egg-info
	@rm -rf dist
	@find . -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@echo "Clean up successfully completed."

help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

run: ## Run the development server
	$(UVICORN) main:app --reload

migrate: ## Run the database migration
	$(ALEMBIC) revision --autogenerate
	$(ALEMBIC) upgrade head
