.PHONY: backend-dev frontend-dev

backend-dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --app-dir backend

frontend-dev:
	cd frontend && npm install && npm run dev
