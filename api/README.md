# HSB API

## Dev (local)
cd api
pip install --upgrade pip pip-tools
pip-compile requirements.in -o requirements.txt
pip-sync requirements.txt
uvicorn app.main:app --reload

## Docker
cd docker
docker compose up --build

## Migraciones (MSSQL)
cd api
alembic revision --autogenerate -m "init schema"
alembic upgrade head
