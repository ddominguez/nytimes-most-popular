dev-run:
	flask run --debug

web-up:
	docker compose up

web-stop:
	docker compose stop

web-sh:
	docker compose exec web sh

