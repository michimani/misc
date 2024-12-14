init:
	uv sync
	cp .env.example .env

run:
	@set -a \
	&& source .env \
	&& set +a \
	&& uv run main.py $(ARGS)

fmt:
	uv run ruff format

lint:
	uv run ruff check