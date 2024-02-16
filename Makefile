# ----------------Commands----------------
#
# # change the 20 value in printf to adjust width
# # Use ' ## some comment' behind a command and it will be added to the help message automatically
help: ## Show this help message
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

format: ## Format the code
	@echo "\n=== Isort ================================="
	poetry run isort .
	@echo "\n=== Black ================================="
	poetry run black .
	@echo ""
## $(git ls-files *py)

check: ## Django run checks
	python manage.py check

test: ## Django run tests
	python manage.py test

test_docker: ## Run Django tests via Docker
	@echo "\n=== Running Tests in Docker Container =================================="
	@docker compose run web python manage.py test
	

install: ## Install poetry packages
	@echo "\n=== Installing packages ================================="
	@poetry install --no-root


up: ## Startup docker containers
	@echo "\n=== Running Docker compose up =================================="
	@docker compose up -d

down: ## Stop docker containers
	@echo "\n=== Running Docker compose Down =================================="
	@docker compose down

logs: ## Show docker logs
	@echo "\n=== Running Docker compose logs =================================="
	@docker compose logs

prod_down: ## Stop docker containers with prod settings
	@echo "\n=== Running Docker compose Down PROD =================================="
	@docker compose -f compose-prod.yml down

prod: ## Run docker containers with prod settings
	@echo "\n=== Running Docker compose Up for Prod =================================="
	@docker compose -f docker-compose.yml -f compose-prod.yml up  --detach --build  --force-recreate

prod_logs: ## Show docker logs with prod settings
	@echo "\n=== Running Docker compose Logs Prod =================================="
	@docker compose -f compose-prod.yml logs -f

# --------------Configuration-------------
#  #
#  .NOTPARALLEL: ; # wait for this target to finish
.EXPORT_ALL_VARIABLES: ; # send all vars to shell

.PHONY: docs all # All targets are accessible for user
	        .DEFAULT: help # Running Make will run the help target

MAKEFLAGS += --no-print-directory # dont add message about entering and leaving the working directory

