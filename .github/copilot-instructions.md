# DataForge-Py — Copilot / AI assistant instructions

These notes help an AI agent be immediately productive in this repository. They are intentionally short and concrete — follow file pointers to learn details.

## Big picture (what to read first)
- `README.md` — project overview and CLI examples (top-level quickstart).
- `CLAUDE.md` — richer developer, testing, and architecture notes; much of this file should be used as source material.
- `pyproject.toml` — entry points for generators, required dependencies, and lint/test configuration (mypy/black/ruff settings).

## Core components and data flow
- `dataforge/core/` — base classes and runtime services (Generator base, factory/registry, relations manager, cache, preloader).
- `dataforge/generators/` — generators grouped by category (basic, identifier, advanced). New generators live here and register via decorator or entry points.
- `dataforge/cli/` and `dataforge/api/` — CLI (script `dataforge`) and FastAPI server entrypoints. CLI uses `dataforge.cli.main:cli` (see `pyproject.toml`).
- `data/` — static reference data (surnames, regions, phone prefixes). Use `data/loader.py` and `core/preloader.py` when adding data.

Typical data flow: config/CLI -> `ConfigParser` -> `default_factory.create_generator` -> generator(s) -> `OutputFormatter` -> write JSON/CSV/XML/SQL.

## Project-specific conventions (do this exactly)
- Registration: prefer `@register_generator(name, aliases)` in generator module; production packaging also defines entry points in `pyproject.toml` under `dataforge.generators`.
- Generator contract: implement `_setup()`, `generate_single()`, `validate()`, `generator_type` and `supported_parameters`. See `CLAUDE.md` for a code sketch.
- Tests: tests live under `tests/` with pytest markers: `unit`, `integration`, `performance`, `security`.
- Formatting/type/lint: `black` (88 chars), `isort` (black profile), `ruff`, `mypy` (strict). Follow `pyproject.toml` settings.
- Packaging: the console entry script is `dataforge` (maps to `dataforge.cli.main:cli`).

## Dev workflows & useful commands (copyable)
- Install dev environment: `pip install -e ".[dev]"`
- Run CLI locally: `python -m dataforge.cli.main generate idcard --count 5`
- Start API server: `uvicorn dataforge.api.main:app --reload`
- Run tests: `pytest tests/ -m unit` (or `pytest tests/` to run all)
- Format / lint: `black dataforge/ && isort dataforge/ && ruff check dataforge/`

## Integration points & risks to watch for
- Generators may preload large data files from `data/` via `core/preloader.py` — prefer streaming/batch implementations for bulk generation.
- SQL output uses `dataforge/output/sql.py` — be careful to use parameterized templates to avoid injection when adapting logic.
- API uses FastAPI async endpoints; prefer `async def` handlers and avoid blocking I/O in endpoint code paths.

## Quick pointers for common edits
- To add a generator: create module under `dataforge/generators/<category>/`, implement the generator contract, add unit tests under `tests/generators/`, and either decorate with `@register_generator` or add an entry-point in `pyproject.toml` for distribution.
- To add static reference data: put JSON under `data/` and add a loader in `data/loader.py`; consider updating `core/preloader.py` to preload.

## Where to look for more context
- `CLAUDE.md` — developer rules and detailed examples (use liberally).
- `pyproject.toml` — test and CI configuration, entry points, and dev extras.
- `dataforge/core/relations.py` and `dataforge/output/formatter.py` — relation handling and output formatting examples.

If anything above is unclear or you want more detail on a particular area (generator lifecycle, relation manager, or test setup), tell me which area and I will expand or merge additional examples.
