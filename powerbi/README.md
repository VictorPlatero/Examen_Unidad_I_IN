# Power BI

Titular: Victor Joseph Platero Maron.

Archivo para abrir o publicar: **`AgroindustriaProduce.pbix`**. Contiene el modelo importado y tres paginas con visuales nativos de Power BI:

1. **Resumen nacional:** cuatro indicadores, barras por departamento, dona por tamano y filtro de departamento.
2. **Exportaciones:** tres indicadores, columnas por departamento, barras de FOB por actividad y filtros de departamento y tamano. La pagina considera solo `exporta = SI`.
3. **Tabla de detalle:** nueve columnas y segmentadores de departamento, tamano y condicion exportadora. Incluye todos los registros; no se limita a las primeras 50 filas del HTML de muestra.

Los filtros y graficos estan vinculados al modelo, no son imagenes pegadas. Los importes representan limites maximos estimados, no ventas o exportaciones observadas.

## Verificacion paso por paso

1. Abrir `AgroindustriaProduce.pbix` en Power BI Desktop. Si ya estaba abierto, abrir otra vez la copia del repositorio para cargar los cambios del archivo.
2. Confirmar las tres pestanas: `01 Resumen nacional`, `02 Exportaciones`, `03 Tabla de detalle`.
3. Sin filtros, contrastar **14,224 empresas** y **665 exportadoras** con el CSV.
4. En Resumen nacional, seleccionar un departamento y comprobar que cambian indicadores y graficos.
5. En Exportaciones, comprobar que solo se consideran empresas exportadoras.
6. En Tabla de detalle, seleccionar `MICRO` en Tamano de empresa y comprobar que la tabla cambia. Limpiar el filtro para volver a todos los registros.
7. Guardar desde Desktop y publicar el PBIX con el mismo nombre. El workflow `deploy-powerbi` usa este archivo.

## Proyecto editable

`AgroindustriaProduce.pbip` contiene la misma definicion visual PBIR y el modelo TMDL. Su fuente inicial es el CSV local. Al clonar en otra carpeta, cambiar `Parameter_Csv` en Transformar datos > Administrar parametros. Para usar Azure, cambiar `Parameter_Source` a `PostgreSQL`, configurar `Parameter_Server` y `Parameter_Database`, introducir las credenciales y actualizar. Guardar como PBIX para publicar esa conexion; el PBIX entregado conserva la importacion local existente.

## Comprobaciones automatizadas

Desde la raiz del repositorio:

```bash
python -m pip install jsonschema
python scripts/build_powerbi_report.py --update-pbix
python scripts/validate_powerbi_report.py --output powerbi/validation.json
```

El generador guarda una copia `.pbix.bak` antes del primer reemplazo y conserva el `DataModel` binario. La validacion comprueba esquemas oficiales de Microsoft, columnas, tres paginas, graficos, filtros, integridad del paquete, concordancia PBIR/PBIX y posiciones sin superposicion.

`validation.json` registra el resultado. La validacion estructural no confirma la renderizacion en Desktop ni la publicacion en el servicio: esos estados figuran por separado. La revision visual en Desktop sigue pendiente porque el control de escritorio no estuvo disponible en la sesion de construccion.

`dashboard_preview.html` y `images/` son vistas previas auxiliares, no el reporte publicable.

Microsoft documenta la edicion de PBIR en [Power BI Desktop project report folder](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report). Para guardar una version final PBIX desde el proyecto, utilizar Power BI Desktop.
