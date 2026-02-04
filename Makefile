.PHONY: dev worker dev-all

dev:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload

worker:
	uv run python -m app.queue.worker

dev-all:
	@echo "API 서버 + 워커 동시 실행"
	@make worker & make dev
