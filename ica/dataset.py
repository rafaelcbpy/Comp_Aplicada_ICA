import re
from pathlib import Path

import pandas as pd
import typer
from loguru import logger
from tqdm import tqdm

from ica.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()


def remove_after_dash(input_string):
    return re.split(r"-", input_string, 1)[0].rstrip()


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
        "Código do Município": "cd_municipio",
        "Município": "nm_municipio",
        "Estado": "estado",
        "Ano de Referência": "ano",
        "Código do Prestador": "cd_prestador",
        "Prestador": "nm_prestador",
        "Sigla do Prestador": "sg_prestador",
        "Abrangência": "abrangencia",
        "Tipo de Serviço": "tipo_servico",
        "Natureza Jurídica": "nat_juridica",
    }

    df = (
        df.query("`Ano de Referência` != '---'")
        .rename(columns=columns_new_names)
        .rename(columns={c: remove_after_dash(c) for c in df.columns})
    )

    df["ano"] = df["ano"].astype(int)

    for c in df.columns[10:]:
        if df[c].dtype == "O":
            df[c] = (
                df[c]
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
                .astype(float)
            )

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
