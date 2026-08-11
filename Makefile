.DEFAULT_GOAL := help

.PHONY: help install install-dev test test-cov lint format typecheck clean render

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install project dependencies
	uv sync --no-dev

install-dev: ## Install project + dev dependencies
	uv sync

test: ## Run tests
	uv run pytest

test-cov: ## Run tests with coverage report
	uv run pytest --cov=docker_render --cov-report=term-missing

lint: ## Lint source with ruff
	uv run ruff check .

format: ## Format source with ruff
	uv run ruff format .

typecheck: ## Run static type checks with mypy
	uv run mypy docker_render

clean: ## Remove build artefacts and caches
	rm -rf .venv dist build *.egg-info .pytest_cache .coverage .mypy_cache .ruff_cache __pycache__ docker_render/__pycache__ tests/__pycache__

render: ## Run the render CLI (pass ARGS="..." to forward arguments)
	uv run render $(ARGS)
