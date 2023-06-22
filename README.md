# RUPay Backend

## Como rodar na sua máquina

- Subir banco de dados MySQL (caso não suba com o docker compose é necessário editar a url de conexão no arquivo [database.py](app/database.py) )
- Rodar o servidor:

```shellscript
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Subindo o banco de dados com Docker Compose

No diretório raíz do arquivo:

``` shellscript
docker-compose up
```
### Links úteis:
- [Download docker linux](https://docs.docker.com/desktop/install/linux-install/)
- [Download docker windows](https://docs.docker.com/desktop/install/windows-install/)

