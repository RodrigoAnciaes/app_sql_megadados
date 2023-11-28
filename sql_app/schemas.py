from typing import List, Union
from datetime import datetime
from pydantic import BaseModel, Field


class MembroBase(BaseModel):
    """Membro da academia"""
    id_membro: int = Field(..., ge=0, description="Identificador único do plano")
    nome_membro: str = Field(..., description="Nome completo do membro")
    peso: float = Field(..., ge=0, description="Peso do membro, em Kg")
    sexo: str = Field(..., description="Sexo do membro")
    data_inscricao_plano_atual: Union[datetime, None] = Field(None, description="Data de inscrição do membro no plano atual")
    data_inscricao_academia: datetime = Field(..., description="Data de inscrição do membro na academia")
    data_nascimento: datetime = Field(..., description="Data de nascimento do membro")
    rg: str = Field(..., description="RG do membro")

class MembroCreate(MembroBase):
    password: str = Field(..., description="Senha do membro")

class Membro(MembroBase):
    hashed_password: str = Field(..., description="Senha do membro")
    class Config:
        from_attributes = True

class PlanoBase(BaseModel):
    """Plano da academia"""
    id_plano: int = Field(..., ge=0, description="Identificador único do plano")
    nome_plano: str = Field(..., description="Nome descritivo do plano")
    preco: float = Field(..., description="Valor mensal do plano, em Reais")
    multa_valor_fidelidade: int = Field(..., ge=0, description="Valor da multa caso o membro cancele o plano antes do tempo de fidelidade, em Reais. Se não tiver fidelidade, multa = 0")
    tempo_fidelidade: int = Field(..., ge=0, description="Tempo de fidelidade do plano, em meses. Se não tiver fidelidade, tempo = 0")
    tempo_duracao: int = Field(..., ge=0, description="Tempo de duração do plano, em meses")
    beneficios: str = Field(..., description="Benefícios do plano, separados por vírgula e espaço. Ex: 'Mordomo, Chauffer, Treino 24h'")
    ativo: bool = Field(..., description="Se o plano está ativo ou não")

class PlanoCreate(PlanoBase):
    # Define fields specific to creating a new record, if needed
    pass

class Plano(PlanoBase):
    class Config:
        from_attributes = True
