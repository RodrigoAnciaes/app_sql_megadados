from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

from datetime import datetime
from typing import Annotated, Union


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    data_nascimento = Column(String, index=True)
    preferencias = Column(String, index=True)

    # Relacionamento com Plano atraves de Usuario_Has_Plano
    planos = relationship("Usuario_Has_Plano", back_populates="usuario")


class Plano(Base):
    __tablename__ = "planos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String, index=True)
    # valor é o preço em centavos
    valor = Column(Integer, index=True)

    # Relacionamento com Usuario atraves de Usuario_Has_Plano
    usuarios = relationship("Usuario_Has_Plano", back_populates="plano")


class Usuario_Has_Plano(Base):
    __tablename__ = "usuarios_has_planos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    plano_id = Column(Integer, ForeignKey("planos.id"))
    data_inicio = Column(String, index=True)
    data_fim = Column(String, index=True)

    # Relacionamento com Usuario
    usuario = relationship("Usuario", back_populates="planos")
    # Relacionamento com Plano
    plano = relationship("Plano", back_populates="usuarios")

