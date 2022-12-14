# APIpostgreSQL

Le but est de créer une API basique pour tester la techno PostgreSQL est notamment la fonctionnalité d'ingestion
de document JSON.

---

## I) Pour connecter l'API à une base de données :

1.  Ouvrir le dossier "apipostgresql".
2. Ouvrir le dossier "app".
3. Ouvrir le fichier "database.py".
4. En dessous du commentaire `# authentification`, changer les valeurs de :
    - `username`, avec l'identifiant utilisé pour se connecter à la base
    - `pswd`, avec le mot de passe de la base de données
    - `database_name` (pas nécessaire), avec le nom de la base de données à utiliser
5. Sauvegarder les modifications.
6. Il est maintenant possible de lancer l'API !

## II) Pour lancer l'API :

1. Ouvrir le dossier "apipostgresql" sur un invite de commande.
2. Lancer la commande :
    ```commandline
    call venv\Scripts\activate
    ```
3. Puis la commande :
    ```commandline
    python run.py
    ```
4. L'API devrait créer la base de données automatiquement, si elle n'existe pas déjà.
5. Ecrire l'URL suivante dans un navigateur :
    
    [http://localhost:8000](http://localhost:8000)

6. Si il n'y a pas d'erreur, la page devrait afficher: 
    `
    {"detail":"Not Found"}
    `

## III) Pour tester l'API :

1. Lancer l'API (voire la section précédente).
2. Ecrire l'URL suivante dans un navigateur :
    
    [http://localhost:8000/docs](http://localhost:8000/docs)
    
3. La page de documentation de fastAPI devrait apparaître.
4. Cliquer sur une route, par exemple : 
    "**GET /users/**  Read Users"
5. Cliquer sur:
    "Try it out"
6. Remplir les champs des paramètres.
7. Cliquer sur "**Execute**".
8. Descendre légèrement afin de voir le "Response body".
#   V 2 _ p o s t g r s q l  
 