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
	cp .env.example .env
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml up -d --build

down:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml down -v

up_local_compose:
	cp .env.example .env
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml up -d

down_local_compose:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml down -v

build_local_compose:
	cp .env.example .env
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml up -d --build
