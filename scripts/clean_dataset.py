from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "Agroindustria_Nacional_2023.csv"
OUTPUT = ROOT / "data" / "agroindustria_nacional_2023_clean.csv"

COLUMNS = [
    "id_anonimo_emp",
    "anio",
    "ciiu",
    "descciiu",
    "sector",
    "ubigeo",
    "departamento",
    "provincia",
    "distrito",
    "tamanio_emp",
    "valor_estimado_minimo_venta",
    "valor_estimado_maximo_venta",
    "exporta",
    "valor_estimado_minimo_fob_dolar",
    "valor_estimado_maximo_fob_dolar",
    "fec_creacion",
]


def main() -> None:
    df = pd.read_csv(SOURCE, sep=";", encoding="latin1").dropna(axis=1, how="all")
    if len(df.columns) != len(COLUMNS):
        raise ValueError(f"Expected {len(COLUMNS)} columns, found {len(df.columns)}")

    df.columns = COLUMNS
    df["ciiu"] = df["ciiu"].astype(str).str.zfill(4)
    df["ubigeo"] = df["ubigeo"].astype(str).str.zfill(6)
    df.to_csv(OUTPUT, sep=";", index=False, encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(df):,} rows")


if __name__ == "__main__":
    main()
