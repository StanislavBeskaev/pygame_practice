
## Format all
fmt: format
format: isort black


## Check code quality
chk: check
lint: check
check: flake black_check isort_check


## Sort imports
isort:
	isort learning projects

isort_check:
	isort --check-only learning projects


## Format code
black:
	black --config pyproject.toml learning projects

black_check:
	black --config pyproject.toml --diff --check learning projects


# Check pep8
flake:
	flake8 --config .flake8 learning projects

