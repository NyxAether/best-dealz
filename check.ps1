black best_dealz tests
autoflake -r --in-place best_dealz tests
isort best_dealz tests
mypy best_dealz tests
flake8 best_dealz tests
pylint best_dealz tests