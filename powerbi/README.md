# Power BI

El repositorio incluye un proyecto Power BI (`AgroindustriaProduce.pbip`) con modelo semantico base y una especificacion de reporte.

Para generar el archivo publicable:

1. Abra `AgroindustriaProduce.pbip` con Power BI Desktop.
2. Configure los parametros `Parameter_Server` y `Parameter_Database`.
3. Cree las paginas indicadas en `AgroindustriaProduce.Report/report_spec.md`.
4. Guarde una copia como `powerbi/AgroindustriaProduce.pbix`.
5. Ejecute el workflow `deploy-powerbi`.

Power BI Desktop es el mecanismo soportado por Microsoft para convertir PBIP a PBIX.
