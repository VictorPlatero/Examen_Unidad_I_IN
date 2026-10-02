INSERT INTO agroindustria.dim_ciiu (ciiu, descripcion, sector)
SELECT DISTINCT ciiu, descciiu, sector
FROM agroindustria.stg_empresas_agroindustriales
ON CONFLICT (ciiu) DO UPDATE
SET descripcion = EXCLUDED.descripcion,
    sector = EXCLUDED.sector;

INSERT INTO agroindustria.dim_ubigeo (ubigeo, departamento, provincia, distrito)
SELECT DISTINCT ubigeo, departamento, provincia, distrito
FROM agroindustria.stg_empresas_agroindustriales
ON CONFLICT (ubigeo) DO UPDATE
SET departamento = EXCLUDED.departamento,
    provincia = EXCLUDED.provincia,
    distrito = EXCLUDED.distrito;

INSERT INTO agroindustria.dim_tamanio_empresa (tamanio_emp)
SELECT DISTINCT tamanio_emp
FROM agroindustria.stg_empresas_agroindustriales
ON CONFLICT (tamanio_emp) DO NOTHING;

INSERT INTO agroindustria.fact_empresa_agroindustrial (
    id_anonimo_emp,
    anio,
    ciiu,
    ubigeo,
    tamanio_emp_id,
    valor_estimado_minimo_venta,
    valor_estimado_maximo_venta,
    exporta,
    valor_estimado_minimo_fob_dolar,
    valor_estimado_maximo_fob_dolar,
    fec_creacion
)
SELECT
    s.id_anonimo_emp,
    s.anio,
    s.ciiu,
    s.ubigeo,
    t.tamanio_emp_id,
    s.valor_estimado_minimo_venta,
    s.valor_estimado_maximo_venta,
    CASE WHEN upper(s.exporta) = 'SI' THEN true ELSE false END,
    s.valor_estimado_minimo_fob_dolar,
    s.valor_estimado_maximo_fob_dolar,
    to_date(s.fec_creacion_raw, 'YYYYMMDD')
FROM agroindustria.stg_empresas_agroindustriales s
JOIN agroindustria.dim_tamanio_empresa t ON t.tamanio_emp = s.tamanio_emp
ON CONFLICT (id_anonimo_emp, anio) DO UPDATE
SET ciiu = EXCLUDED.ciiu,
    ubigeo = EXCLUDED.ubigeo,
    tamanio_emp_id = EXCLUDED.tamanio_emp_id,
    valor_estimado_minimo_venta = EXCLUDED.valor_estimado_minimo_venta,
    valor_estimado_maximo_venta = EXCLUDED.valor_estimado_maximo_venta,
    exporta = EXCLUDED.exporta,
    valor_estimado_minimo_fob_dolar = EXCLUDED.valor_estimado_minimo_fob_dolar,
    valor_estimado_maximo_fob_dolar = EXCLUDED.valor_estimado_maximo_fob_dolar,
    fec_creacion = EXCLUDED.fec_creacion;
