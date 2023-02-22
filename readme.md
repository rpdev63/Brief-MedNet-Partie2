# Brief-MedNet

## Procédure d'installation 

1 ) Cloner le repo git :    

https://github.com/rpdev63/Brief-MLOps.git  

2 ) Créer un environnement virtuel 
```
cd Brief-MLOps/
python -m venv env
```
  
3 ) Activer l'environnement virtuel
```
source env/Scripts/activate
```
  
4 ) Lire le fichier requirements.txt pour installer les librairies python
```
pip install -r requirements.txt
```

## Travaux sur notebooks :

5 ) Dans le dossier travaux-notebooks créer un répertoire "resized" et importer les images disponibles ici :  
https://drive.google.com/drive/folders/15-0OM8c6_LPgRIbjyyBJlW5QkENrRpwz

6 ) Lancer le notebook depuis la racine du projet
```
python -m notebook .
```

## Lancer l'application :

7 ) Configurer les variables d'environnements dans le fichier .env pour accéder à votre base de donnée ( mySQL ) : entrer votre nom d'admistrateur et mot de passe

8 ) Lancer l'application depuis la racine du projet
```
python run.py
```
