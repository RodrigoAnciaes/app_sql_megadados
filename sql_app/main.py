from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import bcrypt
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==== GET ====

@app.get("/membros", response_model=list[schemas.Membro])
def read_membros(db: Session = Depends(get_db)):
    """Retorna uma lista com todos os membros cadastrados na academia."""
    return crud.get_all_membros(db)

@app.get("/planos", response_model=list[schemas.Plano])
def read_planos(db: Session = Depends(get_db)):
    """Retorna uma lista com todos os planos cadastrados na academia."""
    return crud.get_all_planos(db)

@app.get("/membro/{id_membro}", response_model=schemas.Membro, responses={400: {"description": "Error - membro não existe"}})
def read_membro_id(id_membro: int, db: Session = Depends(get_db)):
    """Retorna o membro cadastrado que possui um determinado id."""
    return crud.get_membro(db, id_membro)

@app.get("/plano/{id_plano}", response_model=schemas.Plano, responses={400: {"description": "Error - plano não existe"}})
def read_plano_id(id_plano: int, db: Session = Depends(get_db)):
    """Retorna o plano cadastrado que possui um determinado id."""
    return crud.get_plano(db, id_plano)

@app.get("/membros/ativos", response_model=list[schemas.Membro], responses={200: {"description": "Success - membros ativos retornados"},
                                                                            400: {"description": "Error - nenhum membro com plano ativo"}})
def read_membros_ativos(db: Session = Depends(get_db)):
    """Retorna uma lista com todos os membros ativos cadastrados na academia."""
    return crud.get_membros_ativos(db)

@app.get("/membros/{id_plano}", response_model=list[schemas.Membro], responses={400: {"description": "Error - plano não existe"},
                                                                                400: {"description": "Error - nenhum membro com esse plano"},
                                                                                200: {"description": "Success - membros com esse plano retornados"}})
def read_membros_plano(id_plano: int, db: Session = Depends(get_db)):
    """Retorna uma lista com todos os membros cadastrados em um determinado plano da academia."""
    return crud.get_membros_plano(db, id_plano)

@app.get("/planos/{id_membro}", response_model=list[schemas.Plano])
def read_planos_membro(id_membro: int, db: Session = Depends(get_db)):
    """Retorna uma lista com todos os planos cadastrados de um determinado membro da academia."""
    return crud.get_planos_membro(db, id_membro)

# ==== POST ====

@app.post("/membro", response_model=schemas.Membro, responses={400: {"description": "Error - membro já existe"},
                                                                200: {"description": "Success - membro criado", "content": {"application/json": {"example": {"id_membro": 1}}}}})
def create_membro(membro: schemas.MembroCreate, db: Session = Depends(get_db)):
    """Cria um novo membro na academia."""
    return crud.create_membro(db, membro)

@app.post("/plano", response_model=schemas.Plano, responses={400: {"description": "Error - plano já existe"},
                                                              200: {"description": "Success - plano criado", "content": {"application/json": {"example": {"id_plano": 1}}}}})
def create_plano(plano: schemas.PlanoCreate, db: Session = Depends(get_db)):
    """Cria um novo plano na academia."""
    return crud.create_plano(db, plano)

# ==== PATCH ====

@app.patch("/membro", response_model=schemas.Membro, responses={400: {"description": "Error - membro não existe"},
                                                                 200: {"description": "Success - membro atualizado", "content": {"application/json": {"example": {"id_membro": 1}}}}})
def update_membro(membro: schemas.Membro, db: Session = Depends(get_db)):
    """Atualiza as informações de um membro."""
    return crud.update_membro(db, membro, membro.id_membro)

@app.patch("/plano", response_model=schemas.Plano, responses={400: {"description": "Error - plano não existe"},
                                                               200: {"description": "Success - plano atualizado", "content": {"application/json": {"example": {"id_plano": 1}}}}})
def update_plano(plano: schemas.Plano, db: Session = Depends(get_db)):
    """Atualiza as informações de um plano."""
    return crud.update_plano(db, plano, plano.id_plano)

# ==== PUT ====

@app.put("/membro/{id_membro}/plano/{id_plano}", response_model=dict[str, list[int]], responses={400: {"description": "Error - membro já tem esse plano"},
                                                                                                   400: {"description": "Error - membro não existe"},
                                                                                                   400: {"description": "Error - plano não existe"},
                                                                                                   200: {"description": "Success - plano adicionado ao membro", "content": {"application/json": {"example": {"id_membro": 1, "ids_planos": [1,2]}}}}})
def update_membro_plano(id_membro: int, id_plano: int, db: Session = Depends(get_db)):
    """Adiciona um plano a um membro."""
    return crud.update_membro_plano(db, id_membro, id_plano)

# ==== DELETE ====

@app.delete("/membro/{id_membro}", response_model=dict[str, int], responses={400: {"description": "Error - membro não existe"},
                                                                              200: {"description": "Success - membro removido", "content": {"application/json": {"example": {"id_membro": 1}}}}})
def delete_membro(id_membro: int, db: Session = Depends(get_db)):
    """Remove um membro da academia."""
    return crud.delete_membro(db, id_membro)

@app.delete("/plano/{id_plano}", response_model=dict[str, int], responses={400: {"description": "Error - plano não existe"},
                                                                            200: {"description": "Success - plano removido", "content": {"application/json": {"example": {"id_plano": 1}}}}})
def delete_plano(id_plano: int, db: Session = Depends(get_db)):
    """Remove um plano da academia."""
    return crud.delete_plano(db, id_plano)

@app.delete("/membro/{id_membro}/plano/{id_plano}", response_model=dict[str, list[int]], responses={400: {"description": "Error - membro não existe"},
                                                                                                    400: {"description": "Error - plano não existe"},
                                                                                                    400: {"description": "Error - membro não tem esse plano"},
                                                                                                    200: {"description": "Success - plano removido do membro", "content": {"application/json": {"example": {"id_membro": 1, "ids_planos": [1]}}}}})
def delete_membro_plano(id_membro: int, id_plano: int, db: Session = Depends(get_db)):
    """Remove um plano de um membro."""
    return crud.delete_membro_plano(db, id_membro, id_plano)


# / path
@app.get("/")
def read_root():
    return {"Hello": "World"}
    

    s
