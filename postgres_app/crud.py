from sqlalchemy.orm import Session

import models, schemas



# CRUD de usuarios

# get usuario por id
def read_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()


# atualiza usuario por id
def update_usuario(db: Session, usuario_id: int, 
                         nome = None,
                         data_nascimento = None,
                         preferencias = None):
    # atualiza o usuario no dicionario
    usuario_in_db = db.get(models.Usuario, usuario_id)
    if nome:
        usuario_in_db.nome = nome
    if data_nascimento:
        usuario_in_db.data_nascimento = data_nascimento
    if preferencias:
        usuario_in_db.preferencias = preferencias
    db.commit()
    db.refresh(usuario_in_db)
    return usuario_in_db


# cria usuario
def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    # adiciona o usuario ao dicionario
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


# deleta usuario por id
def delete_usuario(db: Session, usuario_id: int):
    usuario_in_db = db.get(models.Usuario, usuario_id)
    db.delete(usuario_in_db)
    db.commit()
    return usuario_in_db



# CRUD de planos

# get plano por id
def read_plano(db: Session, plano_id: int):
    return db.query(models.Plano).filter(models.Plano.id == plano_id).first()


# atualiza plano por id
def update_plano(db: Session, plano_id: int, 
                         nome = None,
                         descricao = None,
                         valor = None):
    # atualiza o plano no dicionario
    plano_in_db = db.get(models.Plano, plano_id)
    if nome:
        plano_in_db.nome = nome
    if descricao:
        plano_in_db.descricao = descricao
    if valor:
        plano_in_db.valor = valor
    db.commit()
    db.refresh(plano_in_db)
    return plano_in_db


# cria plano
def create_plano(db: Session, plano: schemas.PlanoCreate):
    # adiciona o plano ao dicionario
    db_plano = models.Plano(**plano.dict())
    db.add(db_plano)
    db.commit()
    db.refresh(db_plano)
    return db_plano


# deleta plano por id
def delete_plano(db: Session, plano_id: int):
    plano_in_db = db.get(models.Plano, plano_id)
    db.delete(plano_in_db)
    db.commit()
    return plano_in_db


# lista todos os planos
def get_planos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Plano).offset(skip).limit(limit).all()


# lista todos os usuarios
def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

# CRUD de usuario_has_plano

# get usuario_has_plano por id
def read_usuario_has_plano(db: Session, usuario_has_plano_id: int):
    return db.query(models.Usuario_Has_Plano).filter(models.Usuario_Has_Plano.id == usuario_has_plano_id).first()


# atualiza usuario_has_plano por id
def update_usuario_has_plano(db: Session, usuario_has_plano_id: int, 
                         usuario_id = None,
                         plano_id = None,
                         data_inicio = None,
                         data_fim = None):
    # atualiza o usuario_has_plano no dicionario
    usuario_has_plano_in_db = db.query(models.Usuario_Has_Plano).filter(models.Usuario_Has_Plano.id == usuario_has_plano_id).first()
    if usuario_id:
        usuario_has_plano_in_db.usuario_id = usuario_id
    if plano_id:
        usuario_has_plano_in_db.plano_id = plano_id
    if data_inicio:
        usuario_has_plano_in_db.data_inicio = data_inicio
    if data_fim:
        usuario_has_plano_in_db.data_fim = data_fim
    db.commit()
    db.refresh(usuario_has_plano_in_db)
    return usuario_has_plano_in_db


# cria usuario_has_plano
def create_usuario_has_plano(db: Session, usuario_has_plano: schemas.Usuario_Has_PlanoCreate):
    # adiciona o usuario_has_plano ao dicionario
    db_usuario_has_plano = models.Usuario_Has_Plano(**usuario_has_plano.dict())
    db.add(db_usuario_has_plano)
    db.commit()
    db.refresh(db_usuario_has_plano)
    return db_usuario_has_plano


# deleta usuario_has_plano por id
def delete_usuario_has_plano(db: Session, usuario_has_plano_id: int):
    usuario_has_plano_in_db = db.get(models.Usuario_Has_Plano, usuario_has_plano_id)
    db.delete(usuario_has_plano_in_db)
    db.commit()
    return usuario_has_plano_in_db


# lista todos os usuarios_has_planos
def get_usuarios_has_planos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario_Has_Plano).offset(skip).limit(limit).all()

# Lista todos os usuarios de um plano
def get_usuarios_from_plano(db: Session, plano_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario_Has_Plano).filter(models.Usuario_Has_Plano.plano_id == plano_id).offset(skip).limit(limit).all()

# Lista todos os planos de um usuario
def get_planos_from_usuario(db: Session, usuario_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario_Has_Plano).filter(models.Usuario_Has_Plano.usuario_id == usuario_id).offset(skip).limit(limit).all()




