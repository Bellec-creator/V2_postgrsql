from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import models, schemas


# fonctions faisant des requêtes à la base de données


def get_user(db: Session, user_id: int):
    """
    Récupération d'un utilisateur à partir de l'id
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """
    Récupération d'un utilisateur à partir du mail (donnée unique)
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Récupération de tous les utilisateurs
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Création d'un utilisteur
    """
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_partial_user(db:Session, id: int, user: schemas.UserUpdate):
    """
    Modification des données d'un utilisateur 
    (si un champs n'a pas été rempli, il est ignoré lors de la mise à jour)
    """
    dict = user.__dict__
    update = {}
    for param in dict.keys():
        if dict[param] != None:
            update[param] = dict[param]
    user_to_update = db.query(models.User).filter(models.User.id==id).update(update)
    if not(user_to_update):
        raise HTTPException(404, "User not found")
    db.commit()
    return "Field(s) "+str(list(update))+" successfully updated for "+str(user_to_update)+" user(s)"

def update_user(db:Session, id: int, user: schemas.UserUpdate):
    """
    Modification des données d'un utilisateur
    """
    user_to_update = db.query(models.User).filter(models.User.id==id).update(vars(user))
    if not(user_to_update):
        raise HTTPException(404, "User not found")
    db.commit()
    return str(user_to_update)+" user(s) successfully updated"

def delete_user(db:Session, id: int):
    """
    Suppression d'un utilisateur
    """
    # juste besoin de supprimer l'utilisateur de la table et toutes ses relations sont coupées automatiquement
    # voire paramétrage des tables
    nb = db.query(models.User).filter(models.User.id==id).delete()
    db.commit()
    return str(nb)+" user successfully deleted"
    

def create_item(db: Session, item: schemas.ItemCreate):
    """
    Création d'un item
    """
    db_item = models.Item(**item.dict(), owner_id=None)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session, skip: int = 0, limit: int = 100):
    """
    Récupération de tous les items existants
    """
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    """
    Création d'un item pour un utilisateur
    """
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_json(db: Session, id: int):
    """
    Route de récupération des tests json
    """
    return db.query(models.Json).filter(models.Json.id == id).first()

def create_test_json(db: Session, test: schemas.TestJson):
    """
    Création d'un test json
    """
    db_json = models.Json(id=test.id, json=test.test_json)
    db.add(db_json)
    db.commit()
    db.refresh(db_json)
    return db_json


def get_all_friends(db: Session):
    """
    Récupération de toutes les liaisons contenues dans la table d'association
    """
    return db.query(models.Friends).all()

def get_friends(id: int, db: Session):
    """
    Récupération de la liste d'amis d'un utilisateur
    """
    return db.query(models.User).join(models.Friends, models.Friends.left_id==models.User.id).filter(models.Friends.right_id==id).union(
        db.query(models.User).join(models.Friends, models.Friends.right_id==models.User.id).filter(models.Friends.left_id==id)
    ).all()

def create_friendship(id1:int, id2: int, db: Session):
    """
    Création d'une relation entre deux utilisateurs
    """
    # verification qu'ils ne sont pas deja amis
    if db.query(models.Friends) \
        .filter(
            models.Friends.left_id==id2
        ) \
        .filter(
            models.Friends.right_id==id1
        ) \
        .union(
            db.query(models.Friends) \
            .filter(
                models.Friends.left_id==id1
            ) \
            .filter(
                models.Friends.right_id==id2
            )
        ).count() > 0:
        raise HTTPException(500, "This relation already exists.")
    # ajout de la nouvelle relation
    try:
        friend = models.Friends(left_id=id1,right_id=id2)
        db.add(friend)
        db.commit()
    except IntegrityError as err:
        raise HTTPException(500, format(err))
    
    db.refresh(friend)
    return(friend)


def populate_db (db: Session):
    """
    Route remplissant la base avec des données de test:
    
    - 2 utilisateurs
    
    - 1 objet attribué à personne
    
    - 1 relation entre les 2 utilisateurs
    """

    # Users
    create_user(db, 
        schemas.UserCreate(
            email= "mail1",
            password= "pswd"
        )
    )
    create_user(db, 
        schemas.UserCreate(
            email= "mail2",
            password= "pswd2"
        )
    )

    # Items
    create_item(db, 
        schemas.ItemCreate(
            title="THE key",
            description="to open THE door"
        )
    )

    # Friendships
    create_friendship(1,2,db)
