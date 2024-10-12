import pandas as pd
from psycopg2.extras import execute_values
from src.infra.dbconnect import get_db_connection

csv_url = "https://gitlab.fiocruz.br/marcelo.gomes/infogripe/-/raw/3ce17b1fbcec80af39edc0bd9b79b5a33756c2f9/Dados/InfoGripe/casos_semanais_fx_etaria_virus_sem_filtro_sintomas.csv?inline=false"


def handler(event, context):
    print("Loading CSV...")
    df = pd.read_csv(csv_url, sep=";")
    print("CSV loaded successfully.")

    rj_data = df[df["DS_UF_SIGLA"] == "RJ"]
    rj_data = rj_data[rj_data["Ano epidemiológico"] == 2024]

    if rj_data.empty:
        print("No data found for RJ in 2024.")
        return

    records = [
        (
            int(row["SG_UF_NOT"]),
            row["fx_etaria"],
            int(row["SRAG"]),
            int(row["SARS2"]),
            int(row["VSR"]),
            int(row["FLU"]),
            int(row["FLU_A"]),
            int(row["FLU_AH1N1"]),
            int(row["FLU_AH3N2"]),
            int(row["FLU_ANSUBTPD"]),
            int(row["FLU_ANSUBTPV"]),
            int(row["FLU_AINC"]),
            int(row["FLU_AOUT"]),
            int(row["FLU_B"]),
            int(row["FLU_BVIC"]),
            int(row["FLU_BYAM"]),
            int(row["FLU_BNLIN"]),
            int(row["FLU_BINC"]),
            int(row["FLU_BOUT"]),
            int(row["RINO"]),
            int(row["ADNO"]),
            int(row["BOCA"]),
            int(row["METAP"]),
            int(row["PARA1"]),
            int(row["PARA2"]),
            int(row["PARA3"]),
            int(row["PARA4"]),
            int(row["OUTROS"]),
            int(row["positivos"]),
            int(row["negativos"]),
            int(row["aguardando"]),
            row["DS_UF_SIGLA"],
            int(row["epiyear"]),
            int(row["epiweek"]),
            int(row["Semana epidemiológica"]),
            int(row["Ano epidemiológico"]),
        )
        for _, row in rj_data.iterrows()
    ]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("TRUNCATE TABLE fio_cruz_data")

    insert_query = """
        INSERT INTO fio_cruz_data (
            "SG_UF_NOT", "fx_etaria", "SRAG", "SARS2", "VSR", "FLU", "FLU_A", "FLU_AH1N1", 
            "FLU_AH3N2", "FLU_ANSUBTPD", "FLU_ANSUBTPV", "FLU_AINC", "FLU_AOUT", "FLU_B", 
            "FLU_BVIC", "FLU_BYAM", "FLU_BNLIN", "FLU_BINC", "FLU_BOUT", "RINO", "ADNO", "BOCA", 
            "METAP", "PARA1", "PARA2", "PARA3", "PARA4", "OUTROS", "positivos", "negativos", 
            "aguardando", "DS_UF_SIGLA", "epiyear", "epiweek", "semana_epidemiologica", 
            "ano_epidemiologico"
        ) VALUES %s
        """

    execute_values(cur, insert_query, records)

    conn.commit()
    cur.close()
    conn.close()

    print(f"Successfully inserted {len(records)} rows.")

    return "Data loaded successfully."
