from datetime import datetime
from logger_setup import setup_logger
import utils
import pandas as pd

logger = setup_logger("wrk_to_socle.py")

EXEC_ID_TABLES = {"CHAMBRE","TRAITEMENT","STAFF","PATIENT_INDV","PATIENT_TELP","PATIENT_ADDR","CONSULTATION","HOSPITALISATION","MEDICAMENT"}

TABLE_CONSTANTS = {
    "PATIENT":      {"SRC_TYP": "Patient"},
    "PATIENT_INDV": {"INDV_STTS_CD": "Actif"},
}

column_mapping_party = {
    # "PART_ID" ajouté dynamiquement (surrogate key) #todo part_id
    "ID_PERSONNEL": "SRC_ID",
    "FONCTION_PERSONNEL" : "SRC_TYP",
}


column_mapping_chambre = {
    "NO_CHAMBRE": "ROOM_NUM",
    "NOM_CHAMBRE": "ROOM_NAME",
    "NO_ETAGE": "FLOOR_NUM",
    "NOM_BATIMENT": "BULD_NAME",
    "TYPE_CHAMBRE": "ROOM_TYP",
    "PRIX_JOUR": "ROOM_DAY_RATE",
    "DT_CREATION": "CRTN_DT",
}

column_mapping_traitement = {
    "ID_TRAITEMENT": "TRET_ID",
    # "MEDC_ID" obtenu par lookup sur R_MEDC (CD_MEDICAMENT, CATG_MEDICAMENT, MARQUE_FABRI) TODO
    "QTE_MEDICAMENT": "MEDC_QTY",
    "DSC_POSOLOGIE": "DOSG_DSC",
    "ID_CONSULT": "CONS_ID",
    "TS_CREATION_TRAITEMENT": "TRET_CRTN_DTTM",
}


column_mapping_individual = {
    # "PART_ID" obtenu par lookup sur R_PART (ID_PERSONNEL, FONCTION_PERSONNEL)
    "NOM_PERSONNEL": "INDV_NAME",
    "PRENOM_PERSONNEL": "INDV_FIRS_NAME",
    "CD_STATUT_PERSONNEL": "INDV_STTS_CD",
    "TS_CREATION_PERSONNEL": "CRTN_DTTM",
    "TS_MAJ_PERSONNEL": "UPDT_DTTM",
}

column_mapping_staff = {
    # "PART_ID" obtenu par lookup sur R_PART (ID_PERSONNEL, FONCTION_PERSONNEL)
    "TS_DEBUT_ACTIVITE": "WORK_STRT_DTTM",
    "TS_FIN_ACTIVITE": "WORK_END_DTTM",
    "RAISON_FIN_ACTIVITE": "WORK_END_RESN",
}

column_mapping_medicament = {
    # "MEDC_ID" ajouté dynamiquement
    "CD_MEDICAMENT": "MEDC_CD",
    "NOM_MEDICAMENT": "MEDC_NAME",
    "CONDIT_MEDICAMENT": "MEDC_COND",
    "CATG_MEDICAMENT": "MEDC_CATG",
    "MARQUE_FABRI": "MANF_BRND",
}


column_mapping_patient_individual = {
    # "PART_ID" obtenu par lookup sur R_PART (ID_PATIENT, 'Patient')
    "NOM_PATIENT":        "INDV_NAME",
    "PRENOM_PATIENT":     "INDV_FIRS_NAME",
    # "INDV_STTS_CD" valeur fixe : 'Actif' TODO
    "TS_CREATION_PATIENT": "CRTN_DTTM",
    "TS_MAJ_PATIENT":      "UPDT_DTTM",
    "DT_NAISS":           "BIRT_DT",
    "VILLE_NAISS":        "BIRT_CITY",
    "PAYS_NAISS":         "BIRT_CNTR",
    "NUM_SECU":           "SOCL_NUM",
}

column_mapping_patient_telephone = {
    # "PART_ID" obtenu par lookup sur R_PART (ID_PATIENT, 'Patient')
    "IND_PAYS_NUM_TELP":  "CNTR_IND",
    "NUM_TELEPHONE":      "TELP_NUM",
    "TS_CREATION_PATIENT": "STRT_VALD_DTTM",
    "TS_MAJ_PATIENT":      "END_VALD_DTTM",
}

column_mapping_patient_address = {
    # "PART_ID" obtenu par lookup sur R_PART (ID_PATIENT, 'Patient')
    "NUM_VOIE":           "STRT_NUM",
    "DSC_VOIE":           "STRT_DSC",
    "CMPL_VOIE":          "COMP_STRT",
    "CD_POSTAL":          "POST_CD",
    "VILLE":              "CITY_NAME",
    "PAYS":               "CNTR_NAME",
    "TS_CREATION_PATIENT": "STRT_VALD_DTTM",
    "TS_MAJ_PATIENT":      "END_VALD_DTTM",
}
column_mapping_consultation = {
    "ID_CONSULT":        "CONS_ID",
    # "STFF_ID" lookup sur R_PART (ID_PERSONNEL, SRC_TYP!= 'Patient')
    # "PATN_ID" lookup sur R_PART (ID_PATIENT, 'Patient')
    "TS_DEBUT_CONSULT":  "CONS_STRT_DTTM",
    "TS_FIN_CONSULT":    "CONS_END_DTTM",
    "POIDS_PATIENT":     "PATN_WEGH",
    "TEMP_PATIENT":      "PATN_TEMP",
    "UNIT_TEMP":         "TEMP_UNIT",
    "TENSION_PATIENT":   "BLD_PRSS",
    "DSC_PATHO":         "PATH_DSC",
    "INDIC_DIABETE":     "DIBT_IND",
    "ID_TRAITEMENT":     "TRET_ID",
    "INDIC_HOSPI":       "HOSP_IND",
}

column_mapping_hospitalisation = {
    "ID_HOSPI":          "HOSP_ID",
    "ID_CONSULT":        "CONS_ID",
    "NO_CHAMBRE":        "ROOM_NUM",
    "TS_DEBUT_HOSPI":    "HOSP_STRT_DTTM",
    "TS_FIN_HOSPI":      "HOSP_END_DTTM",
    "COUT_HOSPI":        "HOSP_FINL_RATE",
    # "STFF_ID" obtenu par lookup sur R_PART (ID_PERSONNEL_RESP, SRC_TYP ≠ 'Patient')
}   

columns_mapping = {
    "CHAMBRE": column_mapping_chambre,
    "TRAITEMENT": column_mapping_traitement,
    "PERSONNEL":  column_mapping_party,
    "MEDICAMENT": column_mapping_medicament,
    "INDIVIDUAL": column_mapping_individual,
    "STAFF":      column_mapping_staff,
    "PATIENT_INDV": column_mapping_patient_individual,
    "PATIENT_TELP": column_mapping_patient_telephone,
    "PATIENT_ADDR": column_mapping_patient_address,
    "CONSULTATION": column_mapping_consultation,
    "HOSPITALISATION": column_mapping_hospitalisation
}

SOC_TARGET = {
    "CHAMBRE":         "R_ROOM",
    "TRAITEMENT":      "O_TRET",
    "PERSONNEL":       "R_PART",
    "MEDICAMENT":      "R_MEDC",
    "INDIVIDUAL":      "O_INDV",
    "STAFF":           "O_STFF",
    "PATIENT_INDV":    "O_INDV",
    "PATIENT_TELP":    "O_TELP",
    "PATIENT_ADDR":    "O_ADDR",
    "CONSULTATION":    "O_CONS",
    "HOSPITALISATION": "O_HOSP",
}

def _fix_timestamps(df: pd.DataFrame) -> pd.DataFrame:
    ts_cols = df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns
    if ts_cols.empty:
        return df.where(pd.notnull(df), None)

    # supprime les zones UTC et convertit en objets datetime
    df[ts_cols] = (
        df[ts_cols]
        .apply(lambda s: s.dt.tz_localize(None).dt.to_pydatetime())
    )
    return df.where(pd.notnull(df), None)

def retrieve_table_wrk(conn, table_name: str) -> pd.DataFrame:
    sql = f"SELECT * FROM WRK.PUBLIC.{table_name}"
    return conn.cursor().execute(sql).fetch_pandas_all()  # évite le warning


def map_and_prepare_data(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    mapping = columns_mapping[table_name]
    df = df.rename(columns=mapping)[list(mapping.values())]

    # Ajout dynamique de colonnes
    if table_name in EXEC_ID_TABLES:
        exec_id = int(datetime.now().timestamp() * 1000)  # Convertir en millisecondes
        df["EXEC_ID"] = exec_id

    _fix_timestamps(df)
    return df.where(pd.notnull(df), None)  # Snowflake -> NULL

def insert_data_in_socle(cs, table, table_name):
    cols = table.columns.tolist()
    col_names = ", ".join(cols)
    insert_query = (
        f"USE DATABASE SOC; "
        f"USE SCHEMA PUBLIC; "
        f"INSERT INTO {SOC_TARGET[table_name]} ({col_names}) VALUES "
    )
    values = []
    for _, row in table.iterrows():
        row_values = []
        for value in row.tolist():
            if value is None:
                row_values.append("NULL")
            else:
                safe_value = str(value).replace("'", "''")
                row_values.append(f"'{safe_value}'")
        values.append(f"({', '.join(row_values)})")

    insert_query += ",\n".join(values) + ";"
    utils.execute_sql(cs, insert_query, logger)


def populate_socle_from_wrk() -> None:
    with utils.connect_snowflake() as conn:  
        cs = conn.cursor()
        for stg_table in columns_mapping:
            logger.info("=== WRK -> SOCLE : %s ===", stg_table)
            df_stg = retrieve_table_wrk(conn, stg_table)
            df_soc = map_and_prepare_data(df_stg, stg_table)
            
            if SOC_TARGET[stg_table] =="R_PART":
                insert_data_in_socle_rpart(cs, df_soc, stg_table)
            else:
                insert_data_in_socle(cs, df_soc, stg_table)
            
def insert_data_in_socle_rpart(cs, table, table_name):
    part_id_dict = {}
    part_id_count=1


    cols = table.columns.tolist()
    col_names = ", ".join(cols)
    insert_query = (
        f"USE DATABASE SOC; "
        f"USE SCHEMA PUBLIC; "
        f"INSERT INTO R_PART (PART_ID,{col_names}) VALUES "
    )
    values = []
    for _, row in table.iterrows():
        row_values = []
        logger.info("row.tolist(): %s ", row.tolist())
        logger.info("LEN: %s ", len(row.tolist()))
        
        if (row.tolist()[0] is not None and row.tolist()[1] is not None):
            part_id_value = str(str(row.tolist()[0])+row.tolist()[1])
            if part_id_value not in part_id_dict.keys():
                part_id_dict[part_id_value]=part_id_count
                part_id_count+=1
                
            safe_part_id_value = str(part_id_dict[part_id_value]).replace("'", "''")
            row_values.append(f"'{safe_part_id_value}'")

        for value in row.tolist():
            if value is None:
                row_values.append("NULL")
            else:
                safe_value = str(value).replace("'", "''")
                row_values.append(f"'{safe_value}'")
                logger.info("safe_value: %s ", safe_value)
        values.append(f"({', '.join(row_values)})")

    insert_query += ",\n".join(values) + ";"
    utils.execute_sql(cs, insert_query, logger)