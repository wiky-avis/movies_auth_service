flake8:
	flake8 --config=.flake8

black:
	black . --config pyproject.toml

isort:
	isort .

linters: isort black flake8

up:
	cp .env.example .env
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml up -d

build:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml up -d --build

down:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml down -v
