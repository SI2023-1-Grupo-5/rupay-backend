from fastapi import FastAPI

app = FastAPI()

# TODO: criar CRUD pra usuários e comentários

@app.get()
def list_all_users():
  return "Lista de todos os usuários...."