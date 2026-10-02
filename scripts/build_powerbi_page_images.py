from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "agroindustria_nacional_2023_clean.csv"
OUT = ROOT / "powerbi" / "images"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1600, 900
BG = "#f5f7fa"
INK = "#172026"
MUTED = "#5b6770"
CARD = "#ffffff"
LINE = "#d8e0e7"
TEAL = "#287271"
BLUE = "#305cde"
ORANGE = "#d96c06"
PURPLE = "#6f4e7c"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F_TITLE = font(42, True)
F_H2 = font(27, True)
F_LABEL = font(20)
F_SMALL = font(16)
F_METRIC = font(40, True)
F_TABLE = font(13)


def text(draw, xy, value, fill=INK, fnt=F_LABEL, anchor=None):
    draw.text(xy, str(value), fill=fill, font=fnt, anchor=anchor)


def card(draw, xy, wh, title, value, accent=TEAL):
    x, y = xy
    w, h = wh
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD, outline=LINE)
    draw.rectangle([x, y, x + 8, y + h], fill=accent)
    text(draw, (x + 28, y + 24), value, fill=INK, fnt=F_METRIC)
    text(draw, (x + 30, y + h - 38), title, fill=MUTED, fnt=F_LABEL)


def bar_chart(draw, x, y, w, h, title, series, color):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD, outline=LINE)
    text(draw, (x + 24, y + 18), title, fnt=F_H2)
    max_val = max(float(series.max()), 1.0)
    top = y + 70
    row_h = (h - 95) / max(len(series), 1)
    for i, (label, val) in enumerate(series.items()):
        yy = top + i * row_h
        label = str(label)[:30]
        text(draw, (x + 24, yy + 4), label, fnt=F_SMALL)
        bx = x + 245
        bw = w - 350
        by = yy + 8
        draw.rounded_rectangle([bx, by, bx + bw, by + 16], radius=4, fill="#e8eef3")
        draw.rounded_rectangle([bx, by, bx + bw * float(val) / max_val, by + 16], radius=4, fill=color)
        text(draw, (x + w - 80, yy + 2), f"{int(val):,}", fnt=F_SMALL, fill=MUTED)


def table_page(df):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    text(d, (50, 36), "Detalle de empresas agroindustriales", fnt=F_TITLE)
    text(d, (52, 88), "Filtro aplicado: tamanio_emp = MICRO | Primeros 24 registros", fnt=F_LABEL, fill=MUTED)

    cols = ["id_anonimo_emp", "departamento", "provincia", "distrito", "tamanio_emp", "exporta", "valor_estimado_maximo_venta"]
    sample = df[df["tamanio_emp"] == "MICRO"][cols].head(24).copy()
    sample["id_anonimo_emp"] = sample["id_anonimo_emp"].str.slice(0, 12) + "..."
    sample["valor_estimado_maximo_venta"] = sample["valor_estimado_maximo_venta"].map(lambda v: f"S/ {int(v):,}")

    x0, y0 = 50, 145
    widths = [210, 170, 200, 210, 130, 90, 230]
    row_h = 28
    headers = ["Empresa", "Departamento", "Provincia", "Distrito", "Tamano", "Exporta", "Venta max."]
    d.rounded_rectangle([x0, y0, x0 + sum(widths), y0 + row_h * (len(sample) + 1)], radius=8, fill=CARD, outline=LINE)
    x = x0
    for header, width in zip(headers, widths):
        d.rectangle([x, y0, x + width, y0 + row_h], fill="#eaf0f4", outline=LINE)
        text(d, (x + 8, y0 + 7), header, fnt=F_TABLE)
        x += width
    for r, row in enumerate(sample.itertuples(index=False), start=1):
        x = x0
        y = y0 + r * row_h
        for value, width in zip(row, widths):
            d.rectangle([x, y, x + width, y + row_h], fill=CARD, outline=LINE)
            text(d, (x + 8, y + 7), str(value)[:28], fnt=F_TABLE, fill=INK)
            x += width
    img.save(OUT / "03_tabla_detalle.png")


def main():
    df = pd.read_csv(DATA, sep=";", encoding="utf-8")
    total = len(df)
    exportadoras = int((df["exporta"] == "SI").sum())
    pct = exportadoras / total
    venta = int(df["valor_estimado_maximo_venta"].sum())
    fob = int(df["valor_estimado_maximo_fob_dolar"].sum())

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    text(d, (50, 36), "Empresas Agroindustriales PRODUCE 2023", fnt=F_TITLE)
    text(d, (52, 90), "Resumen nacional", fnt=F_H2, fill=MUTED)
    card(d, (50, 140), (340, 130), "Empresas", f"{total:,}", TEAL)
    card(d, (420, 140), (340, 130), "Exportadoras", f"{exportadoras:,}", BLUE)
    card(d, (790, 140), (340, 130), "% exportadoras", f"{pct:.1%}", ORANGE)
    card(d, (1160, 140), (390, 130), "Venta maxima estimada", f"S/ {venta:,}", PURPLE)
    bar_chart(d, 50, 310, 710, 520, "Empresas por departamento", df.groupby("departamento").size().sort_values(ascending=False).head(10), TEAL)
    bar_chart(d, 800, 310, 750, 520, "Empresas por tamano", df.groupby("tamanio_emp").size().sort_values(ascending=False), ORANGE)
    img.save(OUT / "01_resumen_nacional.png")

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    text(d, (50, 36), "Empresas Agroindustriales PRODUCE 2023", fnt=F_TITLE)
    text(d, (52, 90), "Exportaciones", fnt=F_H2, fill=MUTED)
    card(d, (50, 140), (460, 130), "FOB maximo estimado", f"US$ {fob:,}", BLUE)
    card(d, (540, 140), (420, 130), "Empresas exportadoras", f"{exportadoras:,}", TEAL)
    card(d, (990, 140), (430, 130), "% exportadoras", f"{pct:.1%}", ORANGE)
    exporters = df[df["exporta"] == "SI"].groupby("departamento").size().sort_values(ascending=False).head(10)
    fob_ciiu = df.groupby("descciiu")["valor_estimado_maximo_fob_dolar"].sum().sort_values(ascending=False).head(8)
    bar_chart(d, 50, 310, 710, 520, "Exportadoras por departamento", exporters, BLUE)
    bar_chart(d, 800, 310, 750, 520, "FOB maximo por CIIU", fob_ciiu, PURPLE)
    img.save(OUT / "02_exportaciones.png")

    table_page(df)
    print(f"Wrote images to {OUT}")


if __name__ == "__main__":
    main()
