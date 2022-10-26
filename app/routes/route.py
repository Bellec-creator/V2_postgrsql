from typing import List

from fastapi import APIRouter, Depends, APIRouter, HTTPException, Body
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database import crud
from app.models import schemas


router = APIRouter()

# routes

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Création d'un utilisateur

    :param user: données de l'utilisateur à remplir pour sa création

    :param db: à ne pas toucher

    :result: utilisateur détaillé
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=List[schemas.UserNoRelations])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupération de la liste des utilisateurs (forme simplifiée)

    :param skip: sauter les n premiers résultats de la requête

    :param limit: nombre d'utilisateurs à récupérer

    :param db: à ne pas toucher

    :result: liste d'utilisateurs simplifiés
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Récupération d'un utilisateur par id (forme complète)

    :param user_id: id de l'utilisateur à récupérer

    :param db: à ne pas toucher

    :result: utilisateur complet
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.patch("/user/{id}", response_model=str)
def update_partial_user(id: int, user: schemas.UserUpdate=Body(...), db: Session = Depends(get_db)):
    """
    Modification partielle d'un utilisateur

    :param id: id de l'utilisateur à modifier

    :param user: données modifiables

    :param db: à ne pas toucher

    :result: message confirmant la modification
    """
    return crud.update_partial_user(db, id, user)

@router.put("/user/{id}", response_model=str)
def update_user(id: int, user: schemas.UserUpdate=Body(...), db: Session = Depends(get_db)):
    """
    Modification d'un utilisateur (un champs omit est remplacé par null dans la base)

    :param id: id de l'utilisateur à modifier

    :param user: données modifiables

    :param db: à ne pas toucher

    :result: message confirmant la modification
    """
    return crud.update_user(db, id, user)


@router.delete("/user/delete/{id}", response_model=object)
def delete_user(id: int, db: Session = Depends(get_db)):
    """
    Suppression d'un utilisateur

    :param id: id de l'utilisateur à supprimer

    :param db: à ne pas toucher

    :result: message avec le nombre d'utilisateurs supprimés (1 si c'est bon)
    """
    return crud.delete_user(db, id)


@router.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    """
    Création d'un item pour un utilisateur

    :param user_id: id du propriétaire de l'objet

    :param item: informations nécessaires à la création de l'item

    :param db: à ne pas toucher

    :result: schéma de l'item créé 
    """
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@router.post("/items/", response_model=schemas.Item)
def create_item(
    item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    """
    Création d'un item

    :param item: données de l'item

    :param db: à ne pas toucher

    :result: schéma de l'item créé
    """
    return crud.create_item(db=db, item=item)


@router.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupération des items

    param skip: sauter les n premiers résultats de la requête

    :param limit: nombre d'items à récupérer

    :param db: à ne pas toucher

    :result: liste d'items
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@router.post("/test/", response_model= schemas.TestJson)
def create_json(json: schemas.TestJson, db: Session = Depends(get_db)):
    """
    Création d'un json

    :param json: données du json

    :param db: à ne pas toucher

    :result: schéma du json créé
    """
    db_json = crud.get_json(db, id=json.id)
    print(db_json)
    if db_json:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_test_json(db, test=json)


@router.post("/friends/new/", response_model=schemas.Friendships)
def create_friendship(id_1: int, id_2: int, db: Session = Depends(get_db)):
    """
    Création d'un lien entre deux utilisateurs

    :param id_1: id du premier utilisateur

    :param id_2: id du second utilisateur

    :param db: à ne pas toucher

    :result: relation au sein de le table d'association (n'a pas vraiment de sens toute seule)
    """
    return crud.create_friendship(id_1, id_2, db)

@router.get("/friends/", response_model=List[schemas.Friendships])
def show_all_friends(db: Session = Depends(get_db)):
    """
    Récupération de toutes les liaisons entre utilisateurs (dur à lire)

    :param db: à ne pas toucher

    :result: liste des relations entre utilisateurs (forme brute)
    """
    return crud.get_all_friends(db)

@router.get("/friends/{user_id}", response_model=List[schemas.UserNoRelations])
def show_friends(id: int, db: Session = Depends(get_db)):
    """
    Récupération de tous les amis d'un utilisateur

    :param id: id de l'utilisateur dont on veut connaitre les amis

    :param db: à ne pas toucher

    :result: liste d'utilisateurs simplifiés
    """
    return crud.get_friends(id, db)

@router.put("/populate")
def populate(db: Session = Depends(get_db)):
    """
    Remplissage automatique de la base de données

    :param db: à ne pas toucher

    :result: message de confirmation du remplissage de la base
    """
    crud.populate_db(db)
    return "Database filled with test datas"