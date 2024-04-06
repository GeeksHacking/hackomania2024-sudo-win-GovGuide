# How to run

1. Install pipenv
```bash
pip install --user pipenv
```

2. Install dependencies in pipenv
```bash
pipenv install
```

3. Run application
```bash
pipenv run uvicorn app:app --reload
```

# Docker
```bash
docker build -t backend .
```

```bash
docker login govguide.azurecr.io
```

```bash
docker tag backend govguide.azurecr.io/backend
docker push govguide.azurecr.io/backend
```

```bash
docker pull govguide.azurecr.io/backend
```
