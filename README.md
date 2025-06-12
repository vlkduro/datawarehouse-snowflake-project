![status_1](https://img.shields.io/badge/Lot%201-done-brightgreen)
![status_2](https://img.shields.io/badge/Lot%201-done-brightgreen)
![status_3](https://img.shields.io/badge/Lot%202-In%20Progress-orange)
![status_4](https://img.shields.io/badge/Lot%204--grey)

# ai07-groupe4-projet

## Secrets et structure

1. Clonez ce dépôt ou téléchargez les fichiers nécessaires.

2. Créez un environnement virtuel (optionnel mais recommandé) :

   ```bash
   python -m venv venv
   ```

3. Activez l'environnement virtuel :

   - Sur Windows :

     ```bash
     venv\Scripts\activate
     ```

   - Sur Mac/Linux :

     ```bash
     source venv/bin/activate
     ```

4. Afin de se connecter à distance à l'environnement `Snowflake`, il faut créer à la racine du projet le fichier `.env` suivant :

   ```
   SNOWFLAKE_USER=user
   SNOWFLAKE_PASSWORD=mot_de_passe
   SNOWFLAKE_ACCOUNT=compte
   SNOWFLAKE_WAREHOUSE=COMPUTE_WH
   ```

**Remarque :**

> - Le fichier .env est dans le .gitignore afin de ne pas push les secrets de la BDD, faites attention à ne jamais push ce fichier.

> - Les timestamps ont été définie comme `varchar(30)`, car le format des timestamps n'est pas adapté au format Snowflake. Cette adaptation sera bien évidemment faite pour la BDD WRK.

> - Le rôle "SYSADMIN" est nécessaire pour l'insertion des données dans les tables sur Snowflake.

## Airflow 🤡

1. Installer airflow :

```bash
pip install apache-airflow
```

2. Configurer Airflow :

Trouver le fichier `airflow.cfg` dans le dossier `airflow` de votre environnement virtuel et modifier les paramètres suivants :

```ini
...
dags_folder = /chemin/vers/le/dossier/des/dags
```

Pour nous ce fichier est le fichier `<votre chemin>/ai07-groupe4-projet/src`

3. Lancer airflow :

```bash
airflow standalone
```

Au début de l'execution de cette commade, vous aurez le mot de passe pour vous connecter à l'interface web d'airflow.
Si vous le loupez, vous pouvez aller chercher le mot de passe dans le fichier `simple_auth_manager_passwords.json.generated` qui se trouve dans le dossier `airflow` de votre environnement.

4. Naviguez dans airflow

Allez dans DAGs et activez les DAGs que vous souhaitez exécuter.