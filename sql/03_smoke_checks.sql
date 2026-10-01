SELECT 'staging_rows' AS metric, count(*)::text AS value
FROM agroindustria.stg_empresas_agroindustriales
UNION ALL
SELECT 'fact_rows', count(*)::text
FROM agroindustria.fact_empresa_agroindustrial
UNION ALL
SELECT 'departamentos', count(*)::text
FROM agroindustria.dim_ubigeo
UNION ALL
SELECT 'ciiu', count(*)::text
FROM agroindustria.dim_ciiu
UNION ALL
SELECT 'empresas_exportadoras', count(*)::text
FROM agroindustria.fact_empresa_agroindustrial
WHERE exporta = true;
