from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# CRUD de usuarios

# get usuario por id
@app.get("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = crud.read_usuario(db, usuario_id=usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return usuario


# atualiza usuario por id
@app.put("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def update_usuario(usuario_id: int, 
                         nome = None,
                         data_nascimento = None,
                         preferencias = None,
                         db: Session = Depends(get_db)):
    # atualiza o usuario no dicionario
    usuario = crud.update_usuario(db, usuario_id=usuario_id, 
                         nome = nome,
                         data_nascimento = data_nascimento,
                         preferencias = preferencias)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return usuario


# cria usuario
@app.post("/usuarios/", response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario = crud.create_usuario(db=db, usuario=usuario)
    return usuario


# CRUD de planos

# get plano por id
@app.get("/planos/{plano_id}", response_model=schemas.Plano)
def read_plano(plano_id: int, db: Session = Depends(get_db)):
    plano = crud.read_plano(db, plano_id=plano_id)
    if plano is None:
        raise HTTPException(status_code=404, detail="Plano nao encontrado")
    return plano


# atualiza plano por id
@app.put("/planos/{plano_id}", response_model=schemas.Plano)
def update_plano(plano_id: int, 
                         nome = None,
                         descricao = None,
                         valor = None,
                         db: Session = Depends(get_db)):
    # atualiza o plano no dicionario
    plano = crud.update_plano(db, plano_id=plano_id, 
                         nome = nome,
                         descricao = descricao,
                         valor = valor)
    if plano is None:
        raise HTTPException(status_code=404, detail="Plano nao encontrado")
    return plano


# cria plano
@app.post("/planos/", response_model=schemas.Plano)
def create_plano(plano: schemas.PlanoCreate, db: Session = Depends(get_db)):
    plano = crud.create_plano(db=db, plano=plano)
    return plano


# CRUD de usuario_has_plano

# get usuario_has_plano por id
@app.get("/usuario_has_planos/{usuario_has_plano_id}", response_model=schemas.Usuario_Has_Plano)
def read_usuario_has_plano(usuario_has_plano_id: int, db: Session = Depends(get_db)):
    usuario_has_plano = crud.read_usuario_has_plano(db, usuario_has_plano_id=usuario_has_plano_id)
    if usuario_has_plano is None:
        raise HTTPException(status_code=404, detail="Usuario_has_plano nao encontrado")
    return usuario_has_plano


# atualiza usuario_has_plano por id

# cria usuario_has_plano
@app.post("/usuario_has_planos/", response_model=schemas.Usuario_Has_Plano)
def create_usuario_has_plano(usuario_has_plano: schemas.Usuario_Has_PlanoCreate, db: Session = Depends(get_db)):
    #verifica se usuário e plano existem
    usuario = crud.read_usuario(db, usuario_id=usuario_has_plano.usuario_id)
    plano = crud.read_plano(db, plano_id=usuario_has_plano.plano_id)
    if usuario is None and plano is None:
        raise HTTPException(status_code=404, detail="Usuario e plano nao encontrados")
    elif usuario is None:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    elif plano is None:
        raise HTTPException(status_code=404, detail="Plano nao encontrado")
    else:
        usuario_has_plano = crud.create_usuario_has_plano(db=db, usuario_has_plano=usuario_has_plano)
        return usuario_has_plano

# lista todos os usuarios
@app.get("/usuarios")
def read_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    usuarios = crud.get_usuarios(db, skip=skip, limit=limit)
    return usuarios


# lista todos os planos
@app.get("/planos")
def read_planos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    planos = crud.get_planos(db, skip=skip, limit=limit)
    return planos

# lista todos os usuarios_has_planos
@app.get("/usuarios_has_planos")
def read_usuarios_has_planos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    usuarios_has_planos = crud.get_usuarios_has_planos(db, skip=skip, limit=limit)
    return usuarios_has_planos


# Lista todos os usuarios de um plano
@app.get("/planos/{plano_id}/usuarios")
def read_usuarios_from_plano(plano_id: int, db: Session = Depends(get_db)):
    usuarios_has_plano_com_plano = crud.get_usuarios_from_plano(db, plano_id=plano_id)
    usuarios = []
    for usuario_has_plano in usuarios_has_plano_com_plano:
        usuarios.append(usuario_has_plano.usuario)
    # remove duplicatas
    usuarios = list(dict.fromkeys(usuarios))
    return usuarios

# Lista todos os planos de um usuario
@app.get("/usuarios/{usuario_id}/planos")
def read_planos_from_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario_has_plano_com_usuario = crud.get_planos_from_usuario(db, usuario_id=usuario_id)
    planos = []
    for usuario_has_plano in usuario_has_plano_com_usuario:
        planos.append(usuario_has_plano.plano)
    # remove duplicatas
    planos = list(dict.fromkeys(planos))
    return planos

# Deleta usuario por id
@app.delete("/usuarios/{usuario_id}")
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = crud.delete_usuario(db, usuario_id=usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return usuario

# Deleta plano por id
@app.delete("/planos/{plano_id}")
def delete_plano(plano_id: int, db: Session = Depends(get_db)):
    plano = crud.delete_plano(db, plano_id=plano_id)
    if plano is None:
        raise HTTPException(status_code=404, detail="Plano nao encontrado")
    return plano

# Deleta usuario_has_plano por id
@app.delete("/usuario_has_planos/{usuario_has_plano_id}")
def delete_usuario_has_plano(usuario_has_plano_id: int, db: Session = Depends(get_db)):
    usuario_has_plano = crud.delete_usuario_has_plano(db, usuario_has_plano_id=usuario_has_plano_id)
    if usuario_has_plano is None:
        raise HTTPException(status_code=404, detail="Usuario_has_plano nao encontrado")
    return usuario_has_plano