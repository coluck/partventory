## Partventory

[![Tests](https://img.shields.io/github/actions/workflow/status/coluck/partventory/test.yaml?label=tests)](https://github.com/coluck/partventory/actions)

A small backend application to store Parts. 

### Notes:

Tech Stack:
- FastAPI
- SQLAlchemy with async support
- SQLite with aiosqlite
- Alembic
- Pytest
- Docker & GitHub Actions for CI


### Setup & Run

```bash
git clone https://github.com/coluck/partventory.git
cd partventory
# 0. Setup virtualenv
python3 -m venv venv
source venv/bin/activate

# 1. Install dependencies
pip install -r requirements.txt
# 2. Set up database
alembic upgrade head
# 3. Run the app
uvicorn src.main:app --reload
```


### How to run:

```bash
uvicorn src.main:app --reload
# or
fastapi dev src/main.py
# or in prod:
gunicorn src.main:app -k uvicorn.workers.UvicornWorker --workers 4 --bind 0.0.0.0:8000
```

### Example API Usage

```bash
# 1. Create a Part
curl -X POST http://localhost:8000/parts \
  -H "Content-Type: application/json" \
  -d '{
    "part_number": "PN-1001",
    "name": "Brake Assembly",
    "price": 1999.99,
    "quantity": 10
  }'

# 2. Get a Part
curl http://localhost:8000/parts/1
```


### Test

```bash
pytest
```


### Run with podman (or docker)

Tested with podman but it should also work with docker. Replace podman with docker 

```bash
podman build -t partventory .
podman exec -it partventory alembic upgrade head
podman run -d -p 8000:8000 --name partventory partventory
```


### To Upsert Models

```bash
# Update model

alembic revision --autogenerate -m "Changelog"
alembic upgrade head
```


### Files
- main.py: Initializes FastAPI app and mounts routers.
- routers.py: Defines HTTP routes.
- service.py: Business logic and DB operations.
- models.py: SQLAlchemy ORM models.
- schemas.py: Pydantic models for validation and serialization.
- exceptions.py: Custom exceptions.
- database.py: Async DB session + engine setup.
- tests/: Tests the app with pytest


### TODO's

- Run rollback in each test case.
- Create modules if the app gets bigger.
  - for models.py, routers.py, service.py, schemas.py

