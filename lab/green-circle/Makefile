python_src=app

.PHONY: help
help:  # from https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: check-lint
check-lint:   ## Lint Python code
	mypy ${python_src}
	flake8 ${python_src}

.PHONY: check-format
check-format:  ## Check formatting of Python files
	isort --check --diff ${python_src}
	black --check --diff ${python_src}

.PHONY: check-test
check-test:  ## Run Python tests
	pytest --numprocesses auto

.PHONY: check
check: check-lint check-format check-test  ## Run all checks

.PHONY: format
format:  ## Format Python files
	isort ${python_src}
	black ${python_src}
