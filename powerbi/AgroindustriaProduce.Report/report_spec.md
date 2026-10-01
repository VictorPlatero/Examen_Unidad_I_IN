# Reporte Power BI: Agroindustria PRODUCE 2023

Este archivo define el reporte que debe abrirse desde `AgroindustriaProduce.pbip` y guardarse como `AgroindustriaProduce.pbix` para publicacion automatizada.

## Modelo

Fuente recomendada: vista `agroindustria.vw_empresas_agroindustriales` en PostgreSQL.

Medidas DAX sugeridas:

```DAX
Empresas = DISTINCTCOUNT(vw_empresas_agroindustriales[id_anonimo_emp])
Exportadoras = CALCULATE([Empresas], vw_empresas_agroindustriales[exporta] = TRUE())
% Exportadoras = DIVIDE([Exportadoras], [Empresas])
Venta maxima estimada = SUM(vw_empresas_agroindustriales[valor_estimado_maximo_venta])
FOB maximo estimado USD = SUM(vw_empresas_agroindustriales[valor_estimado_maximo_fob_dolar])
```

## Pagina 1: Resumen nacional

Visuales:

- Tarjeta: Empresas.
- Tarjeta: Exportadoras.
- Tarjeta: % Exportadoras.
- Grafico de barras: Empresas por departamento.
- Grafico de dona: Empresas por tamanio_emp.
- Segmentador: departamento.

## Pagina 2: Exportaciones

Visuales:

- Tarjeta: FOB maximo estimado USD.
- Grafico de columnas: Empresas exportadoras por departamento.
- Grafico de barras: FOB maximo estimado USD por CIIU.
- Segmentador: exporta.

## Pagina 3: Tabla de detalle

Visuales:

- Tabla: id_anonimo_emp, departamento, provincia, distrito, descripcion_ciiu, tamanio_emp, exporta, valor_estimado_maximo_venta, valor_estimado_maximo_fob_dolar.
- Filtro visual o segmentador obligatorio: tamanio_emp.

## Publicacion

El workflow `.github/workflows/deploy.yml` publica `powerbi/AgroindustriaProduce.pbix` y comparte el workspace con `patcuadrosq@upt.pe`.
Si la cuenta solicitada era `patcuadrosqœupt.pe`, reemplazarla por el correo exacto antes de ejecutar el workflow.
