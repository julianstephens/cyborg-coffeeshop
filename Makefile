
.PHONY: down db seed api aws clean help

help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

down:             ## Remove Docker resources
	@docker compose down
	@docker volume rm cyborg-coffeeshop_app-db-data

db:               ## Start DB
	@docker compose up -d db

seed:             ## Seed DB and S3
	@docker compose up -d prestart
	@aws s3 sync ./backend/data s3://cyborg-coffeeshop-data

api:              ## Start API
	@cd ./backend && fastapi dev --host=0.0.0.0 --reload

aws:              ## Create AWS resources
	@tf init -upgrade
	@tf plan
	@tf apply -auto-approve

clean:            ## Remove AWS resources
	@aws s3 rm s3://cyborg-coffeeshop-data --recursive
	@terraform destroy -auto-approve
