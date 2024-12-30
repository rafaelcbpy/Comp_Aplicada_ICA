from pathlib import Path

import typer
from loguru import logger
from tqdm import tqdm
import pandas as pd
from ica.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()


def preprocess_regression_dataset(df: pd.DataFrame, inplace: bool = False) -> pd.DataFrame:
    """Function that applies the preprocessing phase of the Water Consumption Dataset for the Regression Model.

    Args:
        df (pd.DataFrame): Dataset of Consumption of water
        inplace (bool, optional): Flag that indicates if the transformations are aapplied inplace. Defaults to False.

    Returns:
        pd.DataFrame: Transformed dataset
    """
    if inplace is False:
        df = df.copy()

    columns_new_names = {
        "Município": "nm_municipio",
        "Ano de Referência": "ano",
        # 'Sigla do Prestador': 'sg_prestador',
        "Abrangência": "abrangencia",
        "Tipo de Serviço": "tipo_servico",
        "Natureza Jurídica": "nat_juridica",
        "IN001 - Densidade de economias de água por ligação": "IN001",
        "IN009 - Índice de hidrometração": "IN009",
        "IN020 - Extensão da rede de água por ligação": "IN020",
        "IN022 - Consumo médio percapita de água": "IN022",
        "IN023 - Índice de atendimento urbano de água": "IN023",
        "IN037 - Participação da despesa com energia elétrica nas despesas de exploração": "IN037",
        "IN038 - Participação da despesa com produtos químicos nas despesas de exploração (DEX)": "IN038",
        "IN055 - Índice de atendimento total de água": "IN055",
        "IN057 - Índice de fluoretação de água": "IN057",
    }

    selected_cols = columns_new_names.keys()
    numerical_columns = ["IN001", "IN009", "IN020", "IN023", "IN037", "IN038", "IN055", "IN057"]
    categorical_columns = ["tipo_servico"]
    target_col = "IN022"

    columns_transformations = {"ano": int}
    columns_transformations.update(
        {
            c: lambda x: x.str.replace(",", ".").astype(float)
            for c in numerical_columns + [target_col]
        }
    )

    df = df[selected_cols].query("`Ano de Referência` != '---'").rename(columns=columns_new_names)

    df["tipo_servico"] = df["tipo_servico"].str.rstrip()
    df[list(columns_transformations.keys())] = df.agg(columns_transformations)

    df = df[df["IN022"].notna()]

    return df


@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    # ----------------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Processing dataset...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Processing dataset complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
