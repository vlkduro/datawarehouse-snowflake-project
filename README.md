![status_1](https://img.shields.io/badge/Lot%201-done-brightgreen)
![status_2](https://img.shields.io/badge/Lot%202-In%20Progress-orange)
![status_3](https://img.shields.io/badge/Lot%203--grey)
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
    SNOWFLAKE_WAREHOUSE=warehouse
    ```

**Remarque :** 

> - Le fichier .env est dans le .gitignore afin de ne pas push les secrets de la BDD, faites attention à ne jamais push ce fichier.

> - Les timestamps ont été définie comme `varchar(30)`, car le format des timestamps n'est pas adapté au format Snowflake. Cette adaptation sera bien évidemment faite pour la BDD WRK. 



