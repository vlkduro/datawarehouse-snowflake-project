# 🌐 Projet AI07 - Groupe 4

| Membres du groupe          |
|:--------------------------:|
| **Quentin Valakou** (référent) |
| Rayane Galleze             |
| Lucas Doublet              |
| Julien Pillis              |
| Alexandre Bidaux           |
| Julie Chartier             |
| Quentin Glandier           |

---


## Connexion à Slowflake nécessaire pour tester le projet

Afin de se connecter à distance à l'environnement `Snowflake`, il faut créer à la racine du projet le fichier `.env` suivant : 

```
SNOWFLAKE_USER=user
SNOWFLAKE_PASSWORD=mot_de_passe
SNOWFLAKE_ACCOUNT=compte
SNOWFLAKE_WAREHOUSE=warehouse
```

## 📦 Rendu Lot 2 : Installation du SID et Ingestion des données

### 1. ⚙️ Installation du SID

Les différents scripts suivants sont lancés dans l'ordre:
 - init.sql crée les bases si celles-ci sont non existantes
 - script_creation_stg.sql crée le stage
 - script_creation_soc.sql crée la base SOC
 - script_creation_soc.tch crée la base TCH liée au SOC

Les tables de STG et WRK sont recréées à chaque utilisation en les supprimant avant initialisation dans l'ordre inverse des dépendances.

Les exécutions de code SQL sont tracées dans le dossier log.


Les données DATE ont été convertie en TIMESTAMP.

Concernant les TIMESTAMP:
Lorsque les données sont partiellement manquantes on conserve ce qu'on peut en précision (ex: garder l'information à l'échelle des heures si les minutes sont manquantes)
Quand la donnée est manquante, elle est converti à 0001/01/01/00:00:00, les champs étant NOT NULL et on ne souhaitait pas supprimer la ligne et perdre des informations.

### 2. 🧠  Installation du SID et Ingestion des données

 - Développement des scripts sql d’alimentation des tables de STG
 - Développement du script ‘launch_load_sid.py’ d’exécution du chargement des tables STG

L'ensemble des données sont chargées à l'aide de launch_load_sid.py


### ✅ Bilan

Nous avons pu mettre en pratique nos connaissances de SGBD sur Snowflake et découvrir les librairies Python associées pour automatiser la pipeline de données.

---
