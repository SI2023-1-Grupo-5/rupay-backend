# rupay-backend

## How to run

- Subir banco de dados mysql (caso não suba com o docker compose é necessário editar a url de conexão no arquivo [database.py](app/database.py) )
- Rodar aplicação fastapi

## start database with docker-compose

got to the rupay-backend directory

``` shellscript
docker-compose up
```
[Download docker linux](https://docs.docker.com/desktop/install/linux-install/)

[Download docker windows](https://docs.docker.com/desktop/install/windows-install/)

## fastapi

```shellscript
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ uvicorn app.main:app --reload
```
