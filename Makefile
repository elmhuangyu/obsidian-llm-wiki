help:
	@echo "Available commands:"
	@echo "  update-skills - Update skills"
	@echo "  install-skills - Install skills"
	@echo "  pyfmt - Format Python code"
	@echo "  pylint - Lint Python code"
	@echo "  pylint-fix - Fix Python linting issues"
	@echo "  pytest - Run Python tests"

ingest:
	uv run Scripts/ingest.py

absorb:
	uv run Scripts/absorb.py

.ONESHELL:
update-skills:
	npx skills update

# Will install skills to .agents/skills.
# You can link .agents/skills to .claude/skills if you want to use Claude.
.ONESHELL:
install-skills:
	npx skills add git@github.com:kepano/obsidian-skills.git \
		--skill json-canvas \
		--skill obsidian-bases \
		--skill obsidian-markdown \
		--skill obsidian-cli \
		-y -a gemini-cli

install: install-skills
	uv sync

pyfmt:
	uvx ruff check --select I --fix
	uvx ruff format

pylint:
	uvx ruff check && uvx ruff format --check

pylint-fix:
	uvx ruff check --fix

pytest:
	uv run pytest
