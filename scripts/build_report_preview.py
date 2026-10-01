from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "agroindustria_nacional_2023_clean.csv"
OUTPUT = ROOT / "powerbi" / "dashboard_preview.html"


def main() -> None:
    df = pd.read_csv(DATA, sep=";", encoding="utf-8")

    total = len(df)
    exportadoras = int((df["exporta"] == "SI").sum())
    pct_exportadoras = exportadoras / total if total else 0
    venta_max = int(df["valor_estimado_maximo_venta"].sum())
    fob_max = int(df["valor_estimado_maximo_fob_dolar"].sum())

    departamentos = df.groupby("departamento").size().sort_values(ascending=False).head(10)
    tamanios = df.groupby("tamanio_emp").size().sort_values(ascending=False)
    exportadoras_departamento = (
        df[df["exporta"] == "SI"].groupby("departamento").size().sort_values(ascending=False).head(10)
    )
    fob_ciiu = (
        df.groupby("descciiu")["valor_estimado_maximo_fob_dolar"].sum().sort_values(ascending=False).head(8)
    )

    detail = df[
        [
            "id_anonimo_emp",
            "departamento",
            "provincia",
            "distrito",
            "descciiu",
            "tamanio_emp",
            "exporta",
            "valor_estimado_maximo_venta",
            "valor_estimado_maximo_fob_dolar",
        ]
    ].head(50)

    def bars(series: pd.Series, color: str) -> str:
        max_value = max(series.max(), 1)
        rows = []
        for label, value in series.items():
            pct = (value / max_value) * 100
            rows.append(
                f"<div class='bar-row'><span>{label}</span><div><i style='width:{pct:.1f}%;background:{color}'></i></div><b>{value:,.0f}</b></div>"
            )
        return "\n".join(rows)

    table_rows = "\n".join(
        "<tr>"
        + "".join(f"<td>{value}</td>" for value in row)
        + "</tr>"
        for row in detail.itertuples(index=False, name=None)
    )

    OUTPUT.write_text(
        f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agroindustria PRODUCE 2023</title>
<style>
body {{ font-family: Segoe UI, Arial, sans-serif; margin: 0; color: #172026; background: #f6f7f9; }}
header {{ background: #143642; color: white; padding: 28px 36px; }}
h1 {{ margin: 0 0 6px; font-size: 30px; }}
h2 {{ margin: 0 0 18px; font-size: 21px; }}
main {{ padding: 24px 36px 42px; }}
section {{ margin-bottom: 32px; }}
.grid {{ display: grid; grid-template-columns: repeat(4, minmax(160px, 1fr)); gap: 14px; margin-bottom: 18px; }}
.card {{ background: white; border: 1px solid #dce2e8; border-radius: 8px; padding: 16px; }}
.metric {{ font-size: 28px; font-weight: 700; color: #143642; }}
.label {{ color: #5a6872; font-size: 13px; }}
.two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
.bar-row {{ display: grid; grid-template-columns: 170px 1fr 70px; gap: 10px; align-items: center; margin: 9px 0; font-size: 13px; }}
.bar-row div {{ height: 11px; background: #e7edf2; border-radius: 2px; overflow: hidden; }}
.bar-row i {{ display: block; height: 100%; }}
table {{ width: 100%; border-collapse: collapse; background: white; font-size: 12px; }}
th, td {{ border: 1px solid #dce2e8; padding: 7px 8px; text-align: left; }}
th {{ background: #eaf0f4; position: sticky; top: 0; }}
.table-wrap {{ max-height: 520px; overflow: auto; border: 1px solid #dce2e8; }}
@media (max-width: 900px) {{ .grid, .two {{ grid-template-columns: 1fr; }} .bar-row {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<header>
  <h1>Empresas Agroindustriales PRODUCE 2023</h1>
  <div>Preview local de los dashboards definidos para Power BI.</div>
</header>
<main>
  <section>
    <h2>Resumen nacional</h2>
    <div class="grid">
      <div class="card"><div class="metric">{total:,.0f}</div><div class="label">Empresas</div></div>
      <div class="card"><div class="metric">{exportadoras:,.0f}</div><div class="label">Exportadoras</div></div>
      <div class="card"><div class="metric">{pct_exportadoras:.1%}</div><div class="label">% exportadoras</div></div>
      <div class="card"><div class="metric">S/ {venta_max:,.0f}</div><div class="label">Venta maxima estimada</div></div>
    </div>
    <div class="two">
      <div class="card"><h2>Empresas por departamento</h2>{bars(departamentos, "#287271")}</div>
      <div class="card"><h2>Empresas por tamano</h2>{bars(tamanios, "#d96c06")}</div>
    </div>
  </section>
  <section>
    <h2>Exportaciones</h2>
    <div class="grid">
      <div class="card"><div class="metric">US$ {fob_max:,.0f}</div><div class="label">FOB maximo estimado</div></div>
      <div class="card"><div class="metric">{exportadoras:,.0f}</div><div class="label">Empresas exportadoras</div></div>
    </div>
    <div class="two">
      <div class="card"><h2>Exportadoras por departamento</h2>{bars(exportadoras_departamento, "#305cde")}</div>
      <div class="card"><h2>FOB maximo por CIIU</h2>{bars(fob_ciiu, "#6f4e7c")}</div>
    </div>
  </section>
  <section>
    <h2>Tabla de detalle</h2>
    <div class="label">En Power BI esta pagina incluye filtro por tamanio_emp.</div>
    <div class="table-wrap">
      <table>
        <thead><tr>{''.join(f'<th>{col}</th>' for col in detail.columns)}</tr></thead>
        <tbody>{table_rows}</tbody>
      </table>
    </div>
  </section>
</main>
</body>
</html>
""",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
