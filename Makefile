.PHONY: help run db-up db-down migrate migrate-down migrate-status migrate-new

ENV ?= .env.local

help: ## Show this help (ENV=.env.production make ...)
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------

run: ## Start development server with --reload
	uv run --env-file $(ENV) uvicorn app.main:app --reload

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

db-up: ## Start local PostgreSQL (docker-compose)
	docker compose --env-file $(ENV) up -d db

db-down: ## Stop local PostgreSQL
	docker compose --env-file $(ENV) down

# ---------------------------------------------------------------------------
# Migration (Alembic)
# ---------------------------------------------------------------------------

migrate: ## Apply all pending migrations (alembic upgrade head)
	uv run --env-file $(ENV) alembic upgrade head

migrate-down: ## Rollback one migration step (alembic downgrade -1)
	uv run --env-file $(ENV) alembic downgrade -1

migrate-status: ## Show current migration status (alembic current)
	uv run --env-file $(ENV) alembic current

migrate-new: ## Create a new migration (usage: make migrate-new m="describe changes")
	uv run --env-file $(ENV) alembic revision --autogenerate -m "$(m)"
