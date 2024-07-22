.DEFAULT_GOAL := help
ROOT_DIR := ./

hello:
	@echo "Hello, World!"

help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

clean: ## Clean up the project of unneeded files
	@echo "Cleaning up the project of unneeded files..."
	@rm -rf .tox .mypy_cache .ruff_cache *.egg-info dist .cache htmlcov coverage.xml .coverage
	@find . -name '*.pyc' -delete
	@find . -name 'db.sqlite3' -delete
	@find . -type d -name '__pycache__' -exec rm -r {} \+
	@echo "Clean up successfully completed."

run: ## Run the development server
	@uvicorn main:app --reload