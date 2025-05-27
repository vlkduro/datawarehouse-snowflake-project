-- Postgres n'accepte pas la syntaxe CREATE DATABASE IF NOT EXISTS
-- On utilise un bloc DO pour vérifier l'existence de la base de données avant de la créer

-- Creation de STG si la base n'existe pas
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'STG') THEN
        CREATE DATABASE STG;
    END IF;
END
$$;

-- Creation de WRK si la base n'existe pas
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'WRK') THEN
        CREATE DATABASE WRK;
    END IF;
END
$$;

-- Creation de SOC si la base n'existe pas
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'SOC') THEN
        CREATE DATABASE SOC;
    END IF;
END
$$;

-- Creation de TCH si la base n'existe pas
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'TCH') THEN
        CREATE DATABASE TCH;
    END IF;
END
$$;