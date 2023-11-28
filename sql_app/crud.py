import bcrypt
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException


# ==== GET ====

def get_membro(db: Session, membro_id: int, modo_criar = False):
    # First, check if the member exists
    existing_membro = db.query(models.MembrosSQL).filter(models.MembrosSQL.id_membro == membro_id).first()

    # Raise an HTTPException with a 400 status code if the member doesn't exist
    if not existing_membro and not modo_criar:
        raise HTTPException(status_code=400, detail="Error - membro não existe")

    # Return the member
    return existing_membro

def get_all_membros(db: Session):
    return db.query(models.MembrosSQL).all()

def get_plano(db: Session, plano_id: int, modo_criar = False):
    # First, check if the plan exists
    existing_plano = db.query(models.PlanosSQL).filter(models.PlanosSQL.id_plano == plano_id).first()

    # Raise an HTTPException with a 400 status code if the plan doesn't exist
    if not existing_plano and not modo_criar:
        raise HTTPException(status_code=400, detail="Error - plano não existe")
    
    # Return the plan
    return existing_plano

def get_all_planos(db: Session):
    return db.query(models.PlanosSQL).all()

def get_membros_ativos(db: Session):
    # First, get all the membros in the database
    all_membros = db.query(models.MembrosSQL).all()

    # Iterate through each membro and get all his planos
    for membro in all_membros:
        is_membro_active = False
        ids_planos = [plano.id_plano for plano in membro.planos]
        
        # If the membro has at least one plano that is active, then he is active
        for id_plano in ids_planos:
            if get_plano(db, id_plano).ativo:
                is_membro_active = True
                break
        
        # If the membro is not active, remove him from the list
        if not is_membro_active:
            all_membros.remove(membro)

    # Raise an HTTPException with a 400 status code if there are no active membros
    if not all_membros:
        raise HTTPException(status_code=400, detail="Error - nenhum membro com plano ativo")

    # Return the list of active membros
    return all_membros

def get_membros_plano(db: Session, plano_id: int):
    # First, check if the plan exists
    existing_plano = get_plano(db, plano_id)

    # Raise an HTTPException with a 400 status code if the plan doesn't exist
    if not existing_plano:
        raise HTTPException(status_code=400, detail="Error - plano não existe")
    
    # Get all the membros in the database
    all_membros = db.query(models.MembrosSQL).all()

    # Iterate through each membro and get all his planos
    for membro in all_membros:
        ids_planos = [plano.id_plano for plano in membro.planos]
        
        # If the membro has the plano, add him to the list
        if plano_id in ids_planos:
            continue
        else:
            all_membros.remove(membro)

    # Raise an HTTPException with a 400 status code if there are no membros with the plan
    if not all_membros:
        raise HTTPException(status_code=400, detail="Error - nenhum membro com esse plano")

    # Return the list of membros with the plan
    return all_membros
        

def get_planos_membro(db: Session, membro_id: int):
    # First, check if the member exists
    existing_membro = db.query(models.MembrosSQL).filter(models.MembrosSQL.id_membro == membro_id).first()

    # Raise an HTTPException with a 400 status code if the member doesn't exist
    if not existing_membro:
        raise HTTPException(status_code=400, detail="Error - membro não existe")

    # Return the member's planos
    return existing_membro.planos

# ==== POST ====

def create_membro(db: Session, membro: schemas.MembroCreate):
    # First, check if the member already exists
    existing_membro = get_membro(db, membro.id_membro, modo_criar=True)
    
    # Raise an HTTPException with a 400 status code if the member already exists
    if existing_membro:
        raise HTTPException(status_code=400, detail="Error - membro já existe")    
    
    # Create a SQLAlchemy model instance of the member
    db_membro = models.MembrosSQL(
        nome_membro=membro.nome_membro,
        peso=membro.peso,
        sexo=membro.sexo,
        data_inscricao_plano_atual=membro.data_inscricao_plano_atual,
        data_inscricao_academia=membro.data_inscricao_academia,
        data_nascimento=membro.data_nascimento,
        rg=membro.rg,
        hashed_password=bcrypt.hashpw(f'{membro.password}'.encode('utf8'), bcrypt.gensalt(rounds=10)) # hash the password with bcrypt
    )
    
    # Add the member to the database
    db.add(db_membro)
    db.commit()
    db.refresh(db_membro)
    return db_membro

def create_plano(db: Session, plano: schemas.PlanoCreate):
    # First, check if the plan already exists
    existing_plano = get_plano(db, plano.id_plano, modo_criar=True)

    # Raise an HTTPException with a 400 status code if the plan already exists
    if existing_plano:
        raise HTTPException(status_code=400, detail="Error - plano já existe")
    
    # Create a SQLAlchemy model instance of the plan
    db_plano = models.PlanosSQL(
        nome_plano=plano.nome_plano,
        preco=plano.preco,
        multa_valor_fidelidade=plano.multa_valor_fidelidade,
        tempo_fidelidade=plano.tempo_fidelidade,
        tempo_duracao=plano.tempo_duracao,
        beneficios=plano.beneficios,
        ativo=plano.ativo,
    )

    # Add the plan to the database
    db.add(db_plano)
    db.commit()
    db.refresh(db_plano)
    return db_plano

# ==== UPDATE ====

def update_membro(db: Session, membro: schemas.MembroCreate, membro_id: int):
    # First, check if the member with the specified ID exists
    existing_membro = get_membro(db, membro_id)

    if existing_membro:
        # Update the member attributes with the new values
        existing_membro.nome_membro = membro.nome_membro
        existing_membro.peso = membro.peso
        existing_membro.sexo = membro.sexo
        existing_membro.data_inscricao_plano_atual = membro.data_inscricao_plano_atual
        existing_membro.data_inscricao_academia = membro.data_inscricao_academia
        existing_membro.data_nascimento = membro.data_nascimento
        existing_membro.rg = membro.rg
        existing_membro.hashed_password = bcrypt.hashpw(f'{membro.hashed_password}'.encode('utf8'), bcrypt.gensalt(rounds=10))

        # Commit the changes to the database
        db.commit()

        # Refresh the instance to get the updated state from the database
        db.refresh(existing_membro)

        return existing_membro

    # Raise an HTTPException with a 400 status code if the member doesn't exist
    raise HTTPException(status_code=400, detail=f'Error - membro não existe')

def update_plano(db: Session, plano: schemas.PlanoCreate, plano_id: int):
    # First, check if the plano with the specified ID exists
    existing_plano = get_plano(db, plano_id)
    
    if existing_plano:
        # Update the member attributes with the new values
        existing_plano.nome_plano = plano.nome_plano
        existing_plano.preco = plano.preco
        existing_plano.multa_valor_fidelidade = plano.multa_valor_fidelidade
        existing_plano.tempo_fidelidade = plano.tempo_fidelidade
        existing_plano.tempo_duracao = plano.tempo_duracao
        existing_plano.beneficios = plano.beneficios
        existing_plano.ativo = plano.ativo

        # Commit the changes to the database
        db.commit()

        # Refresh the instance to get the updated state from the database
        db.refresh(existing_plano)

        return existing_plano

    # Raise an HTTPException with a 400 status code if the plano doesn't exist
    raise HTTPException(status_code=400, detail=f'Error - plano não existe')

def update_membro_plano(db: Session, membro_id: int, plano_id: int):
    # Check if both the member and the plan exist
    existing_membro = get_membro(db, membro_id)
    existing_plano = get_plano(db, plano_id)

    # Check if the membro already has the plan
    for plano in existing_membro.planos:
        if plano.id_plano == existing_plano.id_plano:
            raise HTTPException(status_code=400, detail=f'Error - membro já tem esse plano')

    # Add the plan to the membro table
    existing_membro.planos.append(existing_plano)

    # Create a list with all the plano IDs
    ids_planos = [plano.id_plano for plano in existing_membro.planos]

    # Commit the changes to the database
    db.commit()
    db.refresh(existing_membro)
    return {"id_membro": [existing_membro.id_membro], "ids_plano": ids_planos}

# ==== DELETE ====

def delete_membro(db: Session, membro_id: int):
    # First, check if the member with the specified ID exists
    existing_membro = get_membro(db, membro_id)
    
    # Raise an HTTPException with a 400 status code if the member doesn't exist
    if not existing_membro:
        raise HTTPException(status_code=400, detail=f'Error - membro não existe')

    # Delete the relationships between the membro and the planos
    existing_membro.planos.clear()
    
    # Delete the member from the database
    db.delete(existing_membro)
    db.commit()
    return {"id_membro": existing_membro.id_membro}

def delete_plano(db: Session, plano_id: int):
    # First, check if the plan with the specified ID exists
    existing_plano = get_plano(db, plano_id)

    # Raise an HTTPException with a 400 status code if the plan doesn't exist
    if not existing_plano:
        raise HTTPException(status_code=400, detail=f'Error - plano não existe')
    
    # Delete the relationships between the membro and the planos
    existing_plano.membros.clear()

    # Delete the plan from the database
    db.delete(existing_plano)
    db.commit()
    return {"id_plano": existing_plano.id_plano}

def delete_membro_plano(db: Session, membro_id: int, plano_id: int):
    # Check if both the member and the plan exist
    existing_membro = get_membro(db, membro_id)
    existing_plano = get_plano(db, plano_id)
    
    # Check if the member has the plan
    has_plano = False
    for plano in existing_membro.planos:
        if plano.id_plano == existing_plano.id_plano:
            has_plano = True
            break

    # Raise an HTTPException with a 400 status code if the member doesn't have the plan
    if not has_plano:
        raise HTTPException(status_code=400, detail=f'Error - membro não tem esse plano')
    
    # Remove the plan from the membro_plano table
    existing_membro.planos.remove(existing_plano)

    # Create a list with all the plano IDs
    ids_planos = [plano.id_plano for plano in existing_membro.planos]

    # Commit the changes to the database
    db.commit()
    db.refresh(existing_membro)
    return {"id_membro": [existing_membro.id_membro], "ids_plano": ids_planos}
