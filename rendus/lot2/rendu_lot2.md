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


## Connection à Slowflake nécessaire pour tester le projet

Afin de se connecter à distance à l'environnement `Snowflake`, il faut créer à la racine du projet le fichier `.env` suivant : 

```
SNOWFLAKE_USER=user
SNOWFLAKE_PASSWORD=mot_de_passe
SNOWFLAKE_ACCOUNT=compte
SNOWFLAKE_WAREHOUSE=warehouse
```

## 📦 Rendu Lot 2 : Installation du SID et Ingestion des données

### 1. ⚙️ Installation du SID

Les différents scripts suivatns sont lancés dans l'ordre:
 - init.sql crée les bases si celles-ci sont non existantes
 - script_creation_stg.sql créer le stage
 - script_creation_soc.sql créer la base SOC
 - script_creation_soc.tch créer la base TCH liée au SOC

Les tables de STG et WRK sont recrées à chaque utilisation en les supprimant avant initalisation dans l'ordre inverse des dépendance.

Les exécutions de code SQL sont tracées dans un fichier dans le dossier log

Le client, les partages de documents, et la centralisation des échanges officiels.

### 2. 🧠  Installation du SID et Ingestion des données

 - Développement des scripts sql d’alimentation des tables de STG
 - Développement du script ‘launch_load_sid.py’ d’exécution du chargement des tables STG

L'ensemble des données sont chargées à l'aide de launch_load_sid.py

#### Travaux réalisés :

---

### ✅ Bilan

Nous avons pu mettre en pratique nos connaissances de SGBG sur Snowflake et découvrir les librairies Python associées pour automatiser la pipeline de données.

---
