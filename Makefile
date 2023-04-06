flake8:
	flake8 --config=.flake8

black:
	black . --config pyproject.toml

isort:
	isort .

linters: isort black flake8

build:
	docker build -t my-flask-app . && docker run -p 5000:5000 my-flask-app