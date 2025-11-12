FROM python:3.11-slim

# MSSQL ODBC 18
RUN apt-get update && apt-get install -y curl gnupg apt-transport-https && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY api/requirements.in /app/api/requirements.in
RUN python -m pip install --upgrade pip pip-tools && \
    pip-compile /app/api/requirements.in -o /app/api/requirements.txt && \
    pip-sync /app/api/requirements.txt

COPY api /app/api
WORKDIR /app/api
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
