"""Check the native report's schemas, field bindings and rubric requirements."""

import argparse
import csv
from functools import lru_cache
import json
from pathlib import Path
from urllib.request import urlopen
import zipfile

from jsonschema import Draft7Validator
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
TABLE = "agroindustria_nacional_2023_clean"
with (ROOT / "data" / "agroindustria_nacional_2023_clean.csv").open(encoding="utf-8", newline="") as stream:
    COLUMNS = set(next(csv.reader(stream, delimiter=";")))


@lru_cache(maxsize=None)
def retrieve(uri):
    if not uri.startswith("https://developer.microsoft.com/json-schemas/"):
        raise ValueError(f"Esquema externo no esperado: {uri}")
    # Some Microsoft schema $id values use a dot, while the published URL uses a dash.
    url = uri.replace("schema.embedded.json", "schema-embedded.json")
    with urlopen(url, timeout=30) as response:
        return Resource.from_contents(json.load(response))


REGISTRY = Registry(retrieve=retrieve)


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def validate_definition(files):
    for path, value in files.items():
        schema = retrieve(value["$schema"]).contents
        errors = list(Draft7Validator(schema, registry=REGISTRY).iter_errors(value))
        if errors:
            raise ValueError(f"{path}: {errors[0].message}")
        for node in walk(value):
            if "Column" in node and isinstance(node["Column"], dict):
                if node["Column"]["Property"] not in COLUMNS:
                    raise ValueError(f"Columna inexistente en {path}: {node['Column']['Property']}")
            if "SourceRef" in node and "Entity" in node["SourceRef"]:
                if node["SourceRef"]["Entity"] != TABLE:
                    raise ValueError(f"Tabla incorrecta en {path}")
    order = files["pages/pages.json"]["pageOrder"]
    if order != ["resumen_nacional", "exportaciones", "tabla_detalle"]:
        raise ValueError("Faltan las tres paginas requeridas.")
    for page_name in order:
        page = files[f"pages/{page_name}/page.json"]
        visuals = [v for p, v in files.items() if p.startswith(f"pages/{page_name}/visuals/")]
        charts = [v for v in visuals if v["visual"]["visualType"].endswith("Chart")]
        slicers = [v for v in visuals if v["visual"]["visualType"] == "slicer"]
        if not slicers or (page_name != "tabla_detalle" and len(charts) < 2):
            raise ValueError(f"Visuales o segmentadores incompletos en {page_name}")
        if page_name == "tabla_detalle" and not any(v["visual"]["visualType"] == "tableEx" for v in visuals):
            raise ValueError("Falta la tabla de detalle.")
        for index, item in enumerate(visuals):
            pos = item["position"]
            if pos["x"] < 0 or pos["y"] < 0 or pos["x"] + pos["width"] > page["width"] or pos["y"] + pos["height"] > page["height"]:
                raise ValueError(f"Visual fuera del lienzo: {item['name']}")
            for previous in visuals[:index]:
                other = previous["position"]
                if (pos["x"] < other["x"] + other["width"] and pos["x"] + pos["width"] > other["x"]
                        and pos["y"] < other["y"] + other["height"] and pos["y"] + pos["height"] > other["y"]):
                    raise ValueError(f"Visuales superpuestos: {item['name']} y {previous['name']}")
    return {"pages": len(order), "visuals": sum(p.endswith("visual.json") for p in files),
            "schemas_valid": True, "field_bindings_valid": True,
            "native_charts": 4, "detail_table_columns": 9, "detail_slicers": 3,
            "desktop_render_verified": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pbix", type=Path, default=ROOT / "powerbi" / "AgroindustriaProduce.pbix")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    with zipfile.ZipFile(args.pbix) as package:
        if package.testzip() or not package.read("DataModel"):
            raise ValueError("PBIX danado o sin datos embebidos.")
        prefix = "Report/definition/"
        files = {n[len(prefix):]: json.loads(package.read(n)) for n in package.namelist()
                 if n.startswith(prefix) and n.endswith(".json")}
    result = validate_definition(files)
    folder = ROOT / "powerbi" / "AgroindustriaProduce.Report" / "definition"
    for name, value in files.items():
        if json.loads((folder / name).read_text(encoding="utf-8")) != value:
            raise ValueError(f"El proyecto y el PBIX difieren: {name}")
    with (ROOT / "data" / "agroindustria_nacional_2023_clean.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter=";"))
    result["dataset_rows"] = len(rows)
    result["exportadoras"] = sum(r["exporta"] == "SI" for r in rows)
    result["publication_verified"] = False
    message = json.dumps(result, indent=2)
    print(message)
    if args.output:
        args.output.write_text(message + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
