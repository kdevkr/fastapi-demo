# FastAPI Demo

## How to run using FastAPI
```shell
fastapi dev main.py
```

## How to run with intellij

1. Install python3.9+
2. Add python sdk with pipenv
![](images/setup-01.png)
3. Set up run configuration with FastAPI
![](images/setup-02.png)

## requirements.txt
- https://github.com/pypa/pipenv/issues/3493#issuecomment-511690036
- https://github.com/pypa/pipenv/issues/3493#issuecomment-511708312

```sh
pipenv run pip freeze > requirements.txt
```