"""Build native Power BI visuals in PBIR and preserve the imported PBIX model."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

from validate_powerbi_report import validate_definition


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "powerbi" / "AgroindustriaProduce.Report"
PBIX = ROOT / "powerbi" / "AgroindustriaProduce.pbix"
TABLE = "agroindustria_nacional_2023_clean"
SCHEMAS = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition"


def literal(value):
    if isinstance(value, bool):
        value = str(value).lower()
    elif isinstance(value, str):
        value = "'" + value.replace("'", "''") + "'"
    else:
        value = str(value)
    return {"expr": {"Literal": {"Value": value}}}


def column(name, source=None):
    reference = {"Source": source} if source else {"Entity": TABLE}
    return {"Column": {"Expression": {"SourceRef": reference}, "Property": name}}


def projection(name, label, aggregate=None):
    field = column(name)
    query_ref = f"{TABLE}.{name}"
    if aggregate is not None:
        field = {"Aggregation": {"Expression": field, "Function": aggregate}}
        query_ref = f"{'Sum' if aggregate == 0 else 'CountDistinct'}({query_ref})"
    return {"field": field, "queryRef": query_ref, "nativeQueryRef": label,
            "displayName": label}


def export_filter(name):
    return {"filters": [{
        "name": name, "field": column("exporta"), "type": "Categorical",
        "howCreated": "User", "isLockedInViewMode": True,
        "filter": {"Version": 2, "From": [{"Name": "e", "Entity": TABLE, "Type": 0}],
                   "Where": [{"Condition": {"In": {
                       "Expressions": [column("exporta", "e")],
                       "Values": [[{"Literal": {"Value": "'SI'"}}]]}}}]}}]}


def visual(name, kind, title, x, y, width, height, roles=None, objects=None):
    result = {
        "$schema": f"{SCHEMAS}/visualContainer/2.8.0/schema.json", "name": name,
        "position": {"x": x, "y": y, "width": width, "height": height,
                     "z": 0, "tabOrder": y * 10 + x},
        "visual": {"visualType": kind, "drillFilterOtherVisuals": True,
                   "visualContainerObjects": {
                       "title": [{"properties": {"show": literal(bool(title)),
                                  "text": literal(title), "fontSize": literal(14),
                                  "fontColor": {"solid": {"color": literal("#202B28")}}}}],
                       "background": [{"properties": {"show": literal(True),
                                       "color": {"solid": {"color": literal("#FFFFFF")}},
                                       "transparency": literal(0)}}]}}
    }
    if roles:
        result["visual"]["query"] = {"queryState": {
            role: {"projections": fields} for role, fields in roles.items()}}
    if objects:
        result["visual"]["objects"] = objects
    return result


def textbox(name, text, x, y, width, size=24, height=48):
    return visual(name, "textbox", "", x, y, width, height, objects={
        "general": [{"properties": {"paragraphs": [{"textRuns": [
            {"value": text, "textStyle": {"fontFamily": "Segoe UI", "fontSize": f"{size}pt",
                                         "color": "#202B28"}}]}]}}]})


def card(name, title, field, x, width, aggregate=2, exporters=False):
    item = projection(field, title, aggregate)
    item["format"] = "#,0"
    result = visual(name, "card", title, x, 140, width, 120, {"Values": [item]}, {
        "labels": [{"properties": {"fontSize": literal(28),
                   "color": {"solid": {"color": literal("#167D68")}},
                   "labelDisplayUnits": literal(1000000 if aggregate == 0 else 0),
                   "labelPrecision": literal(2 if aggregate == 0 else 0)}}],
        "categoryLabels": [{"properties": {"show": literal(False)}}]})
    if exporters:
        result["filterConfig"] = export_filter(name + "_solo_exportadoras")
    return result


def slicer(name, field, title, x, y, width):
    return visual(name, "slicer", title, x, y, width, 90,
                  {"Values": [projection(field, title)]}, {
                      "data": [{"properties": {"mode": literal("Dropdown")}}],
                      "selection": [{"properties": {"singleSelect": literal(False),
                                     "selectAllCheckboxEnabled": literal(True)}}]})


def chart(name, kind, title, category, value, label, x, width, aggregate=2):
    item = projection(value, label, aggregate)
    item["format"] = "#,0"
    result = visual(name, kind, title, x, 284, width, 556,
                    {"Category": [projection(category, category)], "Y": [item]}, {
                        "labels": [{"properties": {"show": literal(True),
                                   "fontSize": literal(10)}}]})
    result["visual"]["query"]["sortDefinition"] = {
        "sort": [{"field": item["field"], "direction": "Descending"}], "isDefaultSort": False}
    return result


def build_definition():
    with zipfile.ZipFile(PBIX) as source:
        report_settings = json.loads(source.read("Report/definition/report.json"))
    pages = [
        ("resumen_nacional", "01 Resumen nacional", "Resumen nacional"),
        ("exportaciones", "02 Exportaciones", "Exportaciones"),
        ("tabla_detalle", "03 Tabla de detalle", "Detalle de empresas"),
    ]
    files = {"version.json": {
        "$schema": f"{SCHEMAS}/versionMetadata/1.0.0/schema.json", "version": "2.0.0"},
        "report.json": report_settings,
        "pages/pages.json": {"$schema": f"{SCHEMAS}/pagesMetadata/1.1.0/schema.json",
                             "pageOrder": [p[0] for p in pages],
                             "activePageName": pages[0][0]}}
    for name, display, title in pages:
        page = {"$schema": f"{SCHEMAS}/page/2.1.0/schema.json", "name": name,
                "displayName": display, "displayOption": "FitToPage", "width": 1600, "height": 900}
        visuals = [textbox(name + "_titulo", title, 24, 16, 840),
                   textbox(name + "_autor", "PRODUCE 2023 | Victor Joseph Platero Maron",
                           24, 66, 850, 11, 34),
                   textbox(name + "_nota", "Fuente: Ministerio de la Produccion. Importes maximos estimados; no ventas observadas.",
                           24, 855, 1540, 10, 30)]
        if name == "resumen_nacional":
            visuals += [slicer("resumen_departamento", "departamento", "Departamento", 1000, 24, 576),
                        card("resumen_empresas", "Empresas", "id_anonimo_emp", 24, 370),
                        card("resumen_exportadoras", "Exportadoras", "id_anonimo_emp", 418, 370, exporters=True),
                        card("resumen_departamentos", "Departamentos", "departamento", 812, 370),
                        card("resumen_venta", "Venta maxima estimada (S/)", "valor_estimado_maximo_venta", 1206, 370, 0),
                        chart("resumen_por_departamento", "clusteredBarChart", "Empresas por departamento",
                              "departamento", "id_anonimo_emp", "Empresas", 24, 890),
                        chart("resumen_por_tamanio", "donutChart", "Empresas por tamano",
                              "tamanio_emp", "id_anonimo_emp", "Empresas", 938, 638)]
        elif name == "exportaciones":
            page["filterConfig"] = export_filter("pagina_exportaciones_solo_si")
            visuals += [slicer("export_departamento", "departamento", "Departamento", 970, 24, 290),
                        slicer("export_tamanio", "tamanio_emp", "Tamano", 1284, 24, 292),
                        card("export_empresas", "Empresas exportadoras", "id_anonimo_emp", 24, 500),
                        card("export_fob", "FOB maximo estimado (USD)", "valor_estimado_maximo_fob_dolar", 548, 504, 0),
                        card("export_departamentos", "Departamentos exportadores", "departamento", 1076, 500),
                        chart("export_por_departamento", "clusteredColumnChart", "Exportadoras por departamento",
                              "departamento", "id_anonimo_emp", "Exportadoras", 24, 762),
                        chart("export_por_actividad", "clusteredBarChart", "FOB maximo estimado por CIIU (USD)",
                              "descciiu", "valor_estimado_maximo_fob_dolar", "FOB maximo estimado USD", 810, 766, 0)]
        else:
            fields = [("id_anonimo_emp", "Empresa"), ("departamento", "Departamento"),
                      ("provincia", "Provincia"), ("distrito", "Distrito"),
                      ("descciiu", "Actividad CIIU"), ("tamanio_emp", "Tamano"),
                      ("exporta", "Exporta"), ("valor_estimado_maximo_venta", "Venta max. (S/)"),
                      ("valor_estimado_maximo_fob_dolar", "FOB max. (USD)")]
            visuals += [slicer("detalle_departamento", "departamento", "Departamento", 24, 115, 500),
                        slicer("detalle_tamanio", "tamanio_emp", "Tamano de empresa", 548, 115, 504),
                        slicer("detalle_exporta", "exporta", "Exporta", 1076, 115, 500),
                        visual("detalle_tabla", "tableEx", "Detalle empresarial", 24, 230, 1552, 610,
                               {"Values": [projection(f, label) for f, label in fields]}, {
                                   "grid": [{"properties": {"textSize": literal(10)}}]})]
        files[f"pages/{name}/page.json"] = page
        for item in visuals:
            files[f"pages/{name}/visuals/{item['name']}/visual.json"] = item
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--update-pbix", action="store_true", help="Update the existing PBIX, keeping a .bak copy.")
    args = parser.parse_args()
    files = build_definition()
    validate_definition(files)
    for name, value in files.items():
        target = REPORT / "definition" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    with zipfile.ZipFile(PBIX) as source:
        for name in source.namelist():
            if name.startswith("Report/StaticResources/"):
                target = REPORT / name.removeprefix("Report/")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read(name))
    if args.update_pbix:
        with zipfile.ZipFile(PBIX) as source:
            if not any(n.startswith("Report/definition/") for n in source.namelist()):
                raise ValueError("Se requiere un PBIX con formato PBIR y modelo importado.")
            original_hash = hashlib.sha256(source.read("DataModel")).hexdigest()
            with tempfile.TemporaryDirectory() as temp:
                candidate = Path(temp) / PBIX.name
                with zipfile.ZipFile(candidate, "w", compression=zipfile.ZIP_DEFLATED) as output:
                    for info in source.infolist():
                        if not info.filename.startswith("Report/definition/"):
                            output.writestr(info, source.read(info.filename))
                    for name, value in files.items():
                        output.writestr("Report/definition/" + name, json.dumps(value).encode("utf-8"))
                with zipfile.ZipFile(candidate) as output:
                    if output.testzip() or hashlib.sha256(output.read("DataModel")).hexdigest() != original_hash:
                        raise ValueError("La comprobacion de integridad del PBIX fallo.")
                backup = PBIX.with_suffix(".pbix.bak")
                if not backup.exists():
                    shutil.copy2(PBIX, backup)
                source.close()
                shutil.copy2(candidate, PBIX)
        print("PBIX actualizado; DataModel y otras partes conservadas. Copia anterior: .pbix.bak")
    print(f"Definicion creada: {len(files)} archivos, 3 paginas con visuales nativos.")


if __name__ == "__main__":
    main()
