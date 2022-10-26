from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# connexion et création de la base de données


# authentification
username = "postgres"
pswd = " "
database_name = "test_fastapi"

SQLALCHEMY_DATABASE_URL = "postgresql://"+username+":"+pswd+"@localhost/"+database_name

with create_engine(
    "postgresql://"+username+":"+pswd+"@localhost/",
    isolation_level='AUTOCOMMIT'
).connect() as connection:
    try:
        # création de la base de données si elle n'existe pas
        connection.execute('CREATE DATABASE '+database_name)
    except:
        print("Database "+database_name+" already exists. \nEverything's good !")

# lancement de la base de données
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency, session de connexion à la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()