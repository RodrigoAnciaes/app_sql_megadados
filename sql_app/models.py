# Importanto Tipos de Dados
from sqlalchemy import Boolean, Column, Integer, Float, DateTime
from sqlalchemy.dialects.mysql import VARCHAR
# Importando Relacionamentos e outros
from sqlalchemy import ForeignKey, Table, CheckConstraint
from sqlalchemy.orm import relationship
from .database import Base


# Defining N:N relationship between MembrosSQL and PlanosSQL
membro_plano_association = Table('membro_plano_association', Base.metadata,
    Column('membro_id', Integer, ForeignKey('membros.id_membro')),
    Column('plano_id', Integer, ForeignKey('planos.id_plano'))
)


class MembrosSQL(Base):
    __tablename__ = "membros" # Nome da tabela no banco de dados

    # Definindo colunas
    id_membro = Column(Integer, primary_key=True, index=True)
    nome_membro = Column(VARCHAR(100), index=True)
    peso = Column(Float, index=True)
    sexo = Column(VARCHAR(1), index=True)
    data_inscricao_plano_atual = Column(DateTime, index=True, nullable=True)
    data_inscricao_academia = Column(DateTime, index=True)
    data_nascimento = Column(DateTime, index=True)
    rg = Column(VARCHAR(20), index=True)
    hashed_password = Column(VARCHAR(200), index=True)

    __table_args__ = (
        CheckConstraint('peso > 0', name='peso_positivo'),
        CheckConstraint('data_inscricao_academia > data_nascimento', name='data_inscricao_academia_valida'),
    )

    planos = relationship("PlanosSQL", secondary=membro_plano_association, back_populates="membros", cascade="all, delete")


class PlanosSQL(Base):
    __tablename__ = "planos" # Nome da tabela no banco de dados

    # Definindo colunas
    id_plano = Column(Integer, primary_key=True, index=True)
    nome_plano = Column(VARCHAR(100), index=True)
    preco = Column(Float, index=True)
    multa_valor_fidelidade = Column(Integer, index=True)
    tempo_fidelidade = Column(Integer, index=True)
    tempo_duracao = Column(Integer, index=True)
    beneficios = Column(VARCHAR(500), index=True)
    ativo = Column(Boolean, index=True)

    __table_args__ = (
        CheckConstraint('preco > 0', name='preco_positivo'),
        CheckConstraint('multa_valor_fidelidade > 0', name='multa_valor_fidelidade_positivo'),
        CheckConstraint('tempo_fidelidade > 0', name='tempo_fidelidade_positivo'),
        CheckConstraint('tempo_duracao > 0', name='tempo_duracao_positivo'),
        CheckConstraint('tempo_fidelidade <= tempo_duracao', name='tempo_fidelidade_menor_igual_tempo_duracao'),
        CheckConstraint('tempo_fidelidade = 0 or multa_valor_fidelidade > 0', name='multa_valor_fidelidade_valido'),
    )

    membros = relationship("MembrosSQL", secondary=membro_plano_association, back_populates="planos")
