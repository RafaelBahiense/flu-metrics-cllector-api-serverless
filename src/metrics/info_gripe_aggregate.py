from src.infra.dbconnect import get_db_connection
import pandas as pd


def handler(event, context):
    conn = get_db_connection()
    cur = conn.cursor()

    if "limit" not in event:
        event["limit"] = 10
    if "page" not in event:
        event["page"] = 1

    event["offset"] = (event["page"] - 1) * event["limit"]

    cur.execute(
        "SELECT * FROM fio_cruz_data",
    )
    columns = cur.description
    result = [
        {columns[index][0]: column for index, column in enumerate(value)}
        for value in cur.fetchall()
    ]

    df = pd.json_normalize(result)

    half_monthly_cases = reduce_table(df)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": half_monthly_cases.to_json(
            orient="records", force_ascii=False
        ),  # Ensure Portuguese characters are preserved
    }


def assign_half_month_portuguese(epiweek):
    """Assign half-months in Portuguese based on epidemiological week."""
    if epiweek in range(1, 3):
        return "Primeira metade de Janeiro"
    elif epiweek in range(3, 5):
        return "Segunda metade de Janeiro"
    elif epiweek in range(5, 7):
        return "Primeira metade de Fevereiro"
    elif epiweek in range(7, 9):
        return "Segunda metade de Fevereiro"
    elif epiweek in range(9, 11):
        return "Primeira metade de Março"
    elif epiweek in range(11, 13):
        return "Segunda metade de Março"
    elif epiweek in range(13, 15):
        return "Primeira metade de Abril"
    elif epiweek in range(15, 17):
        return "Segunda metade de Abril"
    elif epiweek in range(17, 19):
        return "Primeira metade de Maio"
    elif epiweek in range(19, 21):
        return "Segunda metade de Maio"
    elif epiweek in range(21, 23):
        return "Primeira metade de Junho"
    elif epiweek in range(23, 25):
        return "Segunda metade de Junho"
    elif epiweek in range(25, 27):
        return "Primeira metade de Julho"
    elif epiweek in range(27, 29):
        return "Segunda metade de Julho"
    elif epiweek in range(29, 31):
        return "Primeira metade de Agosto"
    elif epiweek in range(31, 33):
        return "Segunda metade de Agosto"
    elif epiweek in range(33, 35):
        return "Primeira metade de Setembro"
    elif epiweek in range(35, 37):
        return "Segunda metade de Setembro"
    elif epiweek in range(37, 39):
        return "Primeira metade de Outubro"
    elif epiweek in range(39, 41):
        return "Segunda metade de Outubro"
    elif epiweek in range(41, 43):
        return "Primeira metade de Novembro"
    elif epiweek in range(43, 45):
        return "Segunda metade de Novembro"
    elif epiweek in range(45, 47):
        return "Primeira metade de Dezembro"
    elif epiweek in range(47, 49):
        return "Segunda metade de Dezembro"
    elif epiweek in range(49, 53):
        return "Fim do Ano"
    else:
        return "Semana inválida"


def reduce_table(df):
    # Select relevant columns including 'DS_UF_SIGLA', 'semana_epidemiologica', 'ano_epidemiologico', and 'SRAG'
    reduced_df = df[
        ["DS_UF_SIGLA", "ano_epidemiologico", "SRAG", "semana_epidemiologica"]
    ]

    # Apply the half-month assignment function (in Portuguese)
    reduced_df["Meia-Mes"] = reduced_df["semana_epidemiologica"].apply(
        assign_half_month_portuguese
    )

    # Group by state, half-month, and year
    half_monthly_cases = (
        reduced_df.groupby(["DS_UF_SIGLA", "ano_epidemiologico", "Meia-Mes"])
        .sum()
        .reset_index()
    )

    # Sort the results by year and epidemiological week
    half_monthly_cases = half_monthly_cases.sort_values(
        by=["ano_epidemiologico", "semana_epidemiologica"]
    )

    # Rename the columns to Portuguese
    half_monthly_cases.rename(
        columns={
            "DS_UF_SIGLA": "Estado",
            "ano_epidemiologico": "Ano Epidemiológico",
            "SRAG": "Casos de SRAG",
            "Meia-Mes": "Período do Mês",
        },
        inplace=True,
    )

    # Drop 'semana_epidemiologica' from final output since it's already mapped to 'Meia-Mes'
    half_monthly_cases = half_monthly_cases.drop(columns=["semana_epidemiologica"])

    return half_monthly_cases
