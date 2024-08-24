format:
	black .
	isort .
lint:
	flake8 .
test:
	poetry run python tests/msgpack_test.py