# ai07-groupe4-projet

## Notes première session TD

Surrogate key : table SK intermédiaire stockant les plusieurs colonnes qui forment la primary key. recup uniquement id dans Soc plus rapide pour l'exploitation mais pas le chargement.

## Secrets et structure

Afin de se connecter à distance à l'environnement `Snowflake`, il faut créer à la racine du projet le fichier `.env` suivant : 

```
SNOWFLAKE_USER=user
SNOWFLAKE_PASSWORD=mot_de_passe
SNOWFLAKE_ACCOUNT=compte
SNOWFLAKE_WAREHOUSE=warehouse
```

> **ATTENTION :** Ce fichier est dans le .gitignore afin de ne pas push les secrets de la BDD, faites attention à ne jamais push ce fichier.