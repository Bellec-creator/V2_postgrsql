from typing import List, Optional

from pydantic import BaseModel


# schémas des classes utilisés pour l'affichage et la modification des données


# schémas des items

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: Optional[int]

    class Config:
        orm_mode = True


# schémas des utilisateurs et des amitiés

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    # ce champs sert uniquement à initialiser le mot de passe de l'utilisateur
    # dans tous ces schémas, aucun ne permet de voir le mot de passe d'un utilisateur


class Friend(UserBase):
    id: int

    class Config:
        orm_mode = True


class Friendships(BaseModel):
    left_id: int
    right_id: int

    class Config:
        orm_mode = True

# schéma le plus simple à comprendre d'un utilisateur
class UserNoRelations(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

#schéma complet avec les relations sous forme de listes
class User(UserNoRelations):
    items: List[Item] = []
    friends: List[Friend] = []
    friends2: List[Friend] = []

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    email: Optional[str]
    is_active: Optional[bool]
    hashed_password: Optional[str]

    class Config:
        orm_mode = True


# schéma du test json

class TestJson(BaseModel):
    id: int
    test_json: dict

