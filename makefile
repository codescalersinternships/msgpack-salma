format:
	black .
	isort .
lint:
	flake8 .
test:
	python tests/msgpack_test.py