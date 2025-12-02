.PHONY: help install dev build start stop clean test

help:
	@echo "AI Reels Generator - Available Commands:"
	@echo "  make install    - Install all dependencies"
	@echo "  make dev        - Start development environment"
	@echo "  make build      - Build all services"
	@echo "  make start      - Start production environment"
	@echo "  make stop       - Stop all services"
	@echo "  make clean      - Clean up containers and volumes"
	@echo "  make test       - Run all tests"
	@echo "  make logs       - Show logs from all services"

install:
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt

dev:
	@echo "Starting development environment..."
	docker-compose up --build

build:
	@echo "Building all services..."
	docker-compose build

start:
	@echo "Starting production environment..."
	docker-compose up -d

stop:
	@echo "Stopping all services..."
	docker-compose down

clean:
	@echo "Cleaning up..."
	docker-compose down -v
	rm -rf frontend/node_modules
	rm -rf frontend/.next
	rm -rf backend/__pycache__
	find backend -type d -name "__pycache__" -exec rm -rf {} +

test:
	@echo "Running frontend tests..."
	cd frontend && npm run test
	@echo "Running backend tests..."
	cd backend && pytest

logs:
	docker-compose logs -f

frontend-dev:
	cd frontend && npm run dev

backend-dev:
	cd backend && uvicorn src.main:app --reload

db-migrate:
	cd backend && alembic upgrade head

db-reset:
	docker-compose down -v postgres
	docker-compose up -d postgres
	sleep 5
	cd backend && alembic upgrade head
