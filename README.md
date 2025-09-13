# University Data Warehouse Project with Snowflake – Decision Support Tool

This repository contains a university project focused on building a **Data Warehouse** using **Snowflake** in order to design a **decision support tool**.

## Overview

- **Objective**: Implement a Data Warehouse architecture and leverage Snowflake to develop a decision support tool.  
- **Technologies**:  
  - Snowflake (cloud-based Data Warehouse)  
  - Python (workflow orchestration & data processing)  
  - Airflow (ETL orchestration)  
- **Deliverable**: A fully functional decision support environment connected to Snowflake.  

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd your-project
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate it:

- On **Windows**:
  ```bash
  venv\Scripts\activate
  ```

- On **Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 3. Configure Snowflake secrets

Create a `.env` file at the root of the project with the following content:

```ini
SNOWFLAKE_USER=user
SNOWFLAKE_PASSWORD=password
SNOWFLAKE_ACCOUNT=account
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
```

⚠️ **Important**:  
- The `.env` file must not be committed (already included in `.gitignore`).  
- Role **SYSADMIN** is required for inserting data into Snowflake tables.  

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the workflow

```bash
python src/main.py
```

---

## Airflow Integration

### Install Airflow

```bash
pip install apache-airflow
```

### Configure Airflow

- **Windows/Linux**:  
  Edit the `airflow.cfg` file in your environment and update:

  ```ini
  dags_folder = /path/to/ai07-groupe4-projet/src
  ```

- **MacOS**:  
  Default path:  
  ```
  /Users/[username]/airflow/airflow.cfg
  ```
  Update `dags_folder` to:  
  ```
  /Users/[username]/<your_path>/ai07-groupe4-projet/src
  ```

### Run Airflow

```bash
airflow standalone
```

Access the UI at **`http://localhost:8080`**.  
The login password will be displayed on the first run, or can be found in:  
```
simple_auth_manager_passwords.json.generated
```

---

## Notes

- Built as part of a university project.  
- Focus: combining **Snowflake** with **ETL orchestration** to deliver a **decision support tool**.  
