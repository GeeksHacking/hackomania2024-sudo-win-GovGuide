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
docker build backend .
```
