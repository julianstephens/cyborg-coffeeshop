
.PHONY: down db seed backend

down:
	@docker compose down
	@docker volume rm cyborg-coffeeshop_app-db-data

db:
	@docker compose up -d db

seed:
	@docker compse up -d prestart

backend:
	@docker compose up -d db prestart
	@cd ./backend && fastapi dev --host=0.0.0.0 --reload
