## Partventory

A small backend application to store Parts. 

### Notes:

Tech Stack:
- FastAPI
- SQLAlchemy with async support
- SQLite with aiosqlite
- Alembic
- Pytest



### Setup & Run

```bash
git clone https://github.com/coluck/partventory.git
cd partventory
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
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


### Test

```bash
pytest
```


### Run with podman

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



### TODO's

- Run rollback in each test case.
- Create modules if the app gets bigger.
  - for models.py, routers.py, service.py, schemas.py

