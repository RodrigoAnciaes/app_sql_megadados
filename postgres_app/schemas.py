from pydantic import BaseModel
from datetime import datetime, time, timedelta
from typing import Annotated


class UsuarioBase(BaseModel):
    nome: str
    data_nascimento: datetime
    preferencias: str | None = None


class UsuarioCreate(UsuarioBase):
    pass







class PlanoBase(BaseModel):
    nome: str
    descricao: str | None = None
    valor: int


class PlanoCreate(PlanoBase):
    pass


class Plano(PlanoBase):
    id: int

    class Config:
        orm_mode = True

# Movido para ca para não dar err tentando ler Plano antes de ser definido
class Usuario(UsuarioBase):
    id: int

    class Config:
        orm_mode = True


class Usuario_Has_PlanoBase(BaseModel):
    usuario_id: int
    plano_id: int
    data_inicio: datetime
    data_fim: Annotated[datetime | None , None] = None


class Usuario_Has_PlanoCreate(Usuario_Has_PlanoBase):
    pass


class Usuario_Has_Plano(Usuario_Has_PlanoBase):
    id: int

    class Config:
        orm_mode = True
