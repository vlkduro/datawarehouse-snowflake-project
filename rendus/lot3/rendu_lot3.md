# 🌐 Projet AI07 - Groupe 4

|       Membres du groupe        |
| :----------------------------: |
| **Quentin Valakou** (référent) |
|         Rayane Galleze         |
|         Lucas Doublet          |
|         Julien Pillis          |
|        Alexandre Bidaux        |
|         Julie Chartier         |
|        Quentin Glandier        |

---

## Connexion à Slowflake nécessaire pour tester le projet

Afin de se connecter à distance à l'environnement `Snowflake`, il faut créer à la racine du projet le fichier `.env` suivant :

```
SNOWFLAKE_USER=user
SNOWFLAKE_PASSWORD=mot_de_passe
SNOWFLAKE_ACCOUNT=compte
SNOWFLAKE_WAREHOUSE=warehouse
```

## Données à ajouter pour tester le projet

Pour le bon fonctionnement des scrpits Python chargeant les tables Snowflake, il est nécessaire d'ajouter dans Data/ le dossier de données txt du sujet: 'Data Hospital'

## 📦 Rendu Lot 3 : Alimentation d'un datawarehouse

### 1. ⚙️ Alimentation des tables WRK

Le passage des tables de STG à WRK constituent le premier traitement des données pour alimenter le datawarehouse.
Le script Python "stg_to_wrk.py" va alimenter les tables WRK en filtrant les doublons et corrige les dates abberantes.

La durée d'exécution pour la totalité des tables peut varier d'une minute à quelques minutes.

Les exécutions de code SQL sont tracées dans le dossier log.

### 2. 🧠 Alimentation des tables SOCLE

Une fois les tables WRK alimentée, nous allons passer au SOCLE, phase final pour notre datawarehouse.
L'ensemble des tables de SOCLE étant différentes de STG/WRK, nous avons du procéder à un mapping : associer les tables sources aux tables destinations

- En particulier créer les clés (Surrogate Keys).
- Faire attention au typage (TIMESTAMP notamment).

## ✅ Bilan

#### Ce lot 3 nous a permis de pouvoir alimenter l'ensemble de notre datawarehouse avec des données filtrées pour passer ainsi à la création de l'outil décisionnel avec PowerBI.
