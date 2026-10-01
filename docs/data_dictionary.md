# Diccionario de datos

| Campo | Tipo sugerido | Descripcion |
|---|---:|---|
| id_anonimo_emp | varchar(32) | Identificador anonimizado de la empresa o unidad economica. |
| anio | smallint | Anio de origen de la informacion. |
| ciiu | char(4) | Codigo CIIU rev.3. |
| descciiu | varchar(200) | Descripcion del Clasificador Internacional Industrial Uniforme. |
| sector | varchar(100) | Sector economico. |
| ubigeo | char(6) | Codigo de ubicacion geografica. |
| departamento | varchar(50) | Departamento donde se ubica la empresa. |
| provincia | varchar(150) | Provincia donde se ubica la empresa. |
| distrito | varchar(150) | Distrito donde se ubica la empresa. |
| tamanio_emp | varchar(20) | Categoria empresarial: micro, pequena, mediana o gran empresa. |
| valor_estimado_minimo_venta | numeric(14,2) | Valor estimado minimo de ventas anuales en soles. |
| valor_estimado_maximo_venta | numeric(14,2) | Valor estimado maximo de ventas anuales en soles. |
| exporta | boolean | Indicador de si la unidad economica exporta. |
| valor_estimado_minimo_fob_dolar | numeric(14,2) | Valor estimado minimo FOB anual en dolares americanos. |
| valor_estimado_maximo_fob_dolar | numeric(14,2) | Valor estimado maximo FOB anual en dolares americanos. |
| fec_creacion | date | Fecha de creacion del dataset. |
