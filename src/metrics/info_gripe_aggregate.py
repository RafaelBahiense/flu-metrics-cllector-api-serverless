import json
import pandas as pd
from src.infra.dbconnect import get_db_connection

def handler(event, context):
    try:
        limit = int(event.get("limit", 10))
        page = int(event.get("page", 1))
        offset = (page - 1) * limit

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM fio_cruz_data LIMIT %s OFFSET %s", (limit, offset))
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()

        df = pd.DataFrame(rows, columns=columns)

        if df.empty:
            return create_response(404, "No data available.")

        half_monthly_cases = reduce_table(df)

        return create_response(200, half_monthly_cases.to_json(orient="records", force_ascii=False))

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return create_response(500, f"An error occurred: {str(e)}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def create_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": body,
    }


def assign_half_month_portuguese(epiweek):
    half_month_map = {
        range(1, 3): "Primeira metade de Janeiro",
        range(3, 5): "Segunda metade de Janeiro",
        range(5, 7): "Primeira metade de Fevereiro",
        range(7, 9): "Segunda metade de Fevereiro",
        range(9, 11): "Primeira metade de Março",
        range(11, 13): "Segunda metade de Março",
        range(13, 15): "Primeira metade de Abril",
        range(15, 17): "Segunda metade de Abril",
        range(17, 19): "Primeira metade de Maio",
        range(19, 21): "Segunda metade de Maio",
        range(21, 23): "Primeira metade de Junho",
        range(23, 25): "Segunda metade de Junho",
        range(25, 27): "Primeira metade de Julho",
        range(27, 29): "Segunda metade de Julho",
        range(29, 31): "Primeira metade de Agosto",
        range(31, 33): "Segunda metade de Agosto",
        range(33, 35): "Primeira metade de Setembro",
        range(35, 37): "Segunda metade de Setembro",
        range(37, 39): "Primeira metade de Outubro",
        range(39, 41): "Segunda metade de Outubro",
        range(41, 43): "Primeira metade de Novembro",
        range(43, 45): "Segunda metade de Novembro",
        range(45, 47): "Primeira metade de Dezembro",
        range(47, 49): "Segunda metade de Dezembro",
        range(49, 53): "Fim do Ano",
    }

    for epi_range, period in half_month_map.items():
        if epiweek in epi_range:
            return period
    return "Semana inválida"


def reduce_table(df):
    reduced_df = df[["DS_UF_SIGLA", "ano_epidemiologico", "SRAG", "semana_epidemiologica"]]

    reduced_df["Período do Mês"] = reduced_df["semana_epidemiologica"].apply(assign_half_month_portuguese)

    half_monthly_cases = reduced_df.groupby(["DS_UF_SIGLA", "ano_epidemiologico", "Período do Mês"]).agg(
        {"SRAG": "sum"}
    ).reset_index()

    half_monthly_cases.rename(
        columns={
            "DS_UF_SIGLA": "Estado",
            "ano_epidemiologico": "Ano Epidemiológico",
            "SRAG": "Casos de SRAG",
        },
        inplace=True,
    )

    return half_monthly_cases
