dev-run:
	flask --app mostpopular run --debug

dev-test:
	pytest -sv

dev-mypy:
	mypy ./mostpopular

web-up:
	docker compose up

web-stop:
	docker compose stop

web-sh:
	docker compose exec web sh

web-test:
	docker compose run --build --rm web pytest -v

