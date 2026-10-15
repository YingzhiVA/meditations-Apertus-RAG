.PHONY: run test eval stop

# Build the image and start the web UI at http://localhost:7860.
# Needs LLM_NAME, LLM_BASE_URL and LLM_API_KEY (shell or .env); without
# them the page still runs, in reduced mode (keyword routing, plain search).
run:
	docker compose up --build

# The test suite, inside the same image.
test:
	docker compose build
	docker compose run --rm --no-deps meditations python -m pytest -q src/tests

# Reproduce the headline rows from the shipped completion cache
# (data/cache/llm): no API key needed, no LLM calls made.
eval:
	docker compose build
	docker compose run --rm --no-deps meditations python src/eval/run_eval.py \
		--strategy raw raw+hyde --llm apertus-v15-70b --out /tmp/eval.md

stop:
	docker compose down
