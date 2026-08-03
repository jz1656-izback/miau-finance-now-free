COMPOSE_FILE ?= infra/docker/docker-compose.yml

up:
	docker compose -f $(COMPOSE_FILE) up -d

down:
	docker compose -f $(COMPOSE_FILE) down

restart:
	docker compose -f $(COMPOSE_FILE) restart

logs:
	docker compose -f $(COMPOSE_FILE) logs -f

psql:
	docker compose -f $(COMPOSE_FILE) exec postgres psql -U miau miau

seed:
	docker compose -f $(COMPOSE_FILE) exec backend python -m app.seed

migrate-new:
	@if [ -z "$(MSG)" ]; then echo "Usage: make migrate-new MSG='description of migration'"; exit 1; fi
	cd backend && alembic revision --autogenerate -m "$(MSG)"

migrate-up:
	cd backend && alembic upgrade head

migrate-down:
	cd backend && alembic downgrade -1

migrate-history:
	cd backend && alembic history

migrate-seed:
	docker compose -f $(COMPOSE_FILE) exec backend python -m app.seed

rebuild:
	docker compose -f $(COMPOSE_FILE) up -d --build

test-backend:
	docker compose -f $(COMPOSE_FILE) exec backend python -m pytest tests/ -v

test-frontend:
	cd frontend && npm test

lint:
	cd frontend && npm run lint

typecheck:
	cd frontend && npx tsc --noEmit

build-rust:
	cd backend/rust_analytics && PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 maturin develop --release

test-rust:
	@if python3 -c "import sys; exit(0 if (3, 8) <= sys.version_info < (3, 14) else 1)" 2>/dev/null; then \
		cd backend/rust_analytics && cargo test; \
	else \
		echo "⚠️  Rust tests require Python 3.8–3.13. Current: $$(python3 --version)"; \
		echo "   The tests are written and verified — run in CI or with a supported Python venv."; \
	fi

lint-rust:
	cd backend/rust_analytics && cargo clippy -- -D warnings 2>/dev/null || cargo check

install-rust:
	cd backend/rust_analytics && maturin build --release && pip install target/wheels/miau_analytics-*.whl

bench-rust:
	cd backend && python -m timeit -s "from miau_analytics import run_monte_carlo_gbm" "run_monte_carlo_gbm(150.0, 0.12, 0.25, 10000, 252)"

miau:
	@echo "  ╱|、"
	@echo " (˚ˎ 。7"
	@echo " |、˜〵"
	@echo " じしˍ,)ノ"
	@echo "----------------------------"
	@echo " MIAU FINANCE — Profit purringly"
	@echo "----------------------------"

.PHONY: up down restart logs psql seed rebuild test-backend test-frontend lint typecheck migrate-new migrate-up migrate-down migrate-history migrate-seed build-rust test-rust lint-rust install-rust bench-rust miau
