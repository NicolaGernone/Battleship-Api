build:
	docker compose build

down:
	docker compose down

up: build migrate
	docker compose up -d

migrate:
	docker compose run --rm api python manage.py migrate

show:
	docker compose run --rm api python manage.py showmigrations

makemigrations:
	docker compose run --rm api python manage.py makemigrations api

user:
	docker compose run --rm api python manage.py createsuperuser

shell:
	docker compose run --rm api python manage.py shell

deps:
	docker compose run --rm api poetry install

bash:
	docker compose run --rm api /bin/sh

test: build migrate
	docker compose run --rm api pytest

coverage: build migrate
	docker compose run --rm api coverage run --source='api' --omit='api/tests/*' -m pytest
	docker compose run --rm api coverage report
	docker compose run --rm api coverage xml

run: build migrate db_country_list
	docker compose up -d

reboot: down run
