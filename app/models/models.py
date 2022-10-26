from sqlalchemy.sql import expression
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, UniqueConstraint, text
from sqlalchemy.orm import relationship

from app.database.database import Base

# création des differents models (tables de la BDD)

# table d'association entre utilisateurs
class Friends(Base):
    __tablename__ = "friends"

    left_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    right_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    UniqueConstraint('left_id', 'right_id', name='friendship')


# table des utilisateurs
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)
    is_active = Column(Boolean, server_default=expression.true())

    # creation des relations
    items = relationship("Item", back_populates="owner")

    # association:  0..* --> 0..* sur la même table via une table d'association
    friends = relationship(
        "User", 

        secondary=Friends.__table__,
        primaryjoin=Friends.left_id==id,
        secondaryjoin=Friends.right_id==id,
        foreign_keys=id,
        cascade="all, delete", # provoque une suppression automatique des relations avec les autres utilisateurs
        back_populates="friends2"
    )
    # besoin de créer deux relations pour que l'association fonctionne
    # ce n'est pas pratique mais on ne devrait pas utiliser les relations telles quelles
    # pour avoir la liste des amis, on passera plutôt par la table d'association que par les utilisateurs
    friends2 = relationship(
        "User", 

        secondary=Friends.__table__,
        primaryjoin=Friends.right_id==id,
        secondaryjoin=Friends.left_id==id,
        foreign_keys=id,
        cascade="all, delete", # provoque une suppression automatique des relations avec les autres utilisateurs
        back_populates="friends"
    )


# table des items
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    # "SET NULL" permet de conserver un item, après la suppression de son propriétaire, en mettant la clé étrangère à NULL
    
    owner = relationship("User", back_populates="items")


# table des JSON, non utilisée et non modifiée
class Json(Base):
    __tablename__ = "json"

    id = Column(Integer, primary_key=True)
    json = Column(JSON)