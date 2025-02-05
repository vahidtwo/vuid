.PHONY: install
install: ## Install the environment using uv and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using uv"
	@uv venv
	@uv pip install -r requirements.txt
	@uv pip install pre-commit
	@pre-commit install
	@echo "🚀 Virtual environment ready. Activate it using 'source .venv/bin/activate'"

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Linting code: Running pre-commit"
	@pre-commit run -a

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@uv run pytest --cov --cov-config=pyproject.toml --cov-report=xml

.PHONY: build
build: clean-build ## Build wheel file using uv
	@echo "🚀 Creating wheel file"
	@uv build

.PHONY: clean-build
clean-build: ## Clean build artifacts
	@rm -rf dist

.PHONY: publish
publish: ## Publish a release to PyPI.
	@echo "🚀 Publishing: Dry run."
	@uv publish --token $PIPY_TOKEN

.PHONY: build-and-publish
build-and-publish: build publish ## Build and publish.

.PHONY: docs-test
docs-test: ## Test if documentation can be built without warnings or errors
	@uv run mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation
	@uv run mkdocs serve -a localhost:9090

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
