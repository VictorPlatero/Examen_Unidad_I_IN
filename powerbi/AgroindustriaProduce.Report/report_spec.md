# Reporte Power BI: Agroindustria PRODUCE 2023

El PBIX y la carpeta `definition/` contienen tres paginas con visuales nativos. Este documento describe su contenido; no es una tarea pendiente de dibujar los graficos.

## Modelo

Tabla utilizada: `agroindustria_nacional_2023_clean`. El PBIX conserva 14,224 registros importados. El PBIP permite CSV local o la vista `agroindustria.vw_empresas_agroindustriales` en PostgreSQL, normalizando sus columnas al mismo contrato.

Los visuales emplean agregaciones nativas: conteo distinto de empresa o departamento y suma de importes. Consultas DAX equivalentes para contrastar los indicadores:

```DAX
Empresas = DISTINCTCOUNT(agroindustria_nacional_2023_clean[id_anonimo_emp])
Exportadoras = CALCULATE([Empresas], agroindustria_nacional_2023_clean[exporta] = "SI")
Venta maxima estimada = SUM(agroindustria_nacional_2023_clean[valor_estimado_maximo_venta])
FOB maximo estimado USD = SUM(agroindustria_nacional_2023_clean[valor_estimado_maximo_fob_dolar])
```

## Pagina 1: Resumen nacional

Visuales:

- Tarjeta: Empresas.
- Tarjeta: Exportadoras.
- Tarjeta: Departamentos.
- Tarjeta: Venta maxima estimada (S/).
- Grafico de barras: Empresas por departamento.
- Grafico de dona: Empresas por tamanio_emp.
- Segmentador: departamento.

## Pagina 2: Exportaciones

Visuales:

- Tarjeta: FOB maximo estimado USD.
- Tarjeta: Empresas exportadoras.
- Tarjeta: Departamentos exportadores.
- Grafico de columnas: Empresas exportadoras por departamento.
- Grafico de barras: FOB maximo estimado USD por CIIU.
- Segmentadores: departamento y tamanio_emp.
- Filtro de pagina bloqueado: exporta = SI.

## Pagina 3: Tabla de detalle

Visuales:

- Tabla: id_anonimo_emp, departamento, provincia, distrito, descciiu, tamanio_emp, exporta, valor_estimado_maximo_venta, valor_estimado_maximo_fob_dolar.
- Segmentadores: departamento, tamanio_emp y exporta.

## Publicacion

El workflow `.github/workflows/deploy.yml` publica `powerbi/AgroindustriaProduce.pbix` y comparte el workspace con `patcuadrosq@upt.pe`.
La cuenta fue confirmada por el titular como `patcuadrosq@upt.pe`. La publicacion y el acceso en el servicio requieren ejecutar el workflow con las credenciales correspondientes.
