CREATE SCHEMA IF NOT EXISTS agroindustria;

CREATE TABLE IF NOT EXISTS agroindustria.stg_empresas_agroindustriales (
    id_anonimo_emp VARCHAR(32) NOT NULL,
    anio SMALLINT NOT NULL,
    ciiu CHAR(4) NOT NULL,
    descciiu VARCHAR(200) NOT NULL,
    sector VARCHAR(100) NOT NULL,
    ubigeo CHAR(6) NOT NULL,
    departamento VARCHAR(50) NOT NULL,
    provincia VARCHAR(150) NOT NULL,
    distrito VARCHAR(150) NOT NULL,
    tamanio_emp VARCHAR(20) NOT NULL,
    valor_estimado_minimo_venta NUMERIC(14, 2) NOT NULL,
    valor_estimado_maximo_venta NUMERIC(14, 2) NOT NULL,
    exporta VARCHAR(2) NOT NULL,
    valor_estimado_minimo_fob_dolar NUMERIC(14, 2) NOT NULL,
    valor_estimado_maximo_fob_dolar NUMERIC(14, 2) NOT NULL,
    fec_creacion_raw CHAR(8) NOT NULL
);

CREATE TABLE IF NOT EXISTS agroindustria.dim_ciiu (
    ciiu CHAR(4) PRIMARY KEY,
    descripcion VARCHAR(200) NOT NULL,
    sector VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS agroindustria.dim_ubigeo (
    ubigeo CHAR(6) PRIMARY KEY,
    departamento VARCHAR(50) NOT NULL,
    provincia VARCHAR(150) NOT NULL,
    distrito VARCHAR(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS agroindustria.dim_tamanio_empresa (
    tamanio_emp_id SMALLSERIAL PRIMARY KEY,
    tamanio_emp VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS agroindustria.fact_empresa_agroindustrial (
    id_anonimo_emp VARCHAR(32) NOT NULL,
    anio SMALLINT NOT NULL,
    ciiu CHAR(4) NOT NULL REFERENCES agroindustria.dim_ciiu (ciiu),
    ubigeo CHAR(6) NOT NULL REFERENCES agroindustria.dim_ubigeo (ubigeo),
    tamanio_emp_id SMALLINT NOT NULL REFERENCES agroindustria.dim_tamanio_empresa (tamanio_emp_id),
    valor_estimado_minimo_venta NUMERIC(14, 2) NOT NULL,
    valor_estimado_maximo_venta NUMERIC(14, 2) NOT NULL,
    exporta BOOLEAN NOT NULL,
    valor_estimado_minimo_fob_dolar NUMERIC(14, 2) NOT NULL,
    valor_estimado_maximo_fob_dolar NUMERIC(14, 2) NOT NULL,
    fec_creacion DATE NOT NULL,
    CONSTRAINT fact_empresa_agroindustrial_pk PRIMARY KEY (id_anonimo_emp, anio)
);

CREATE INDEX IF NOT EXISTS ix_fact_empresa_departamento
    ON agroindustria.fact_empresa_agroindustrial (ubigeo);

CREATE INDEX IF NOT EXISTS ix_fact_empresa_ciiu
    ON agroindustria.fact_empresa_agroindustrial (ciiu);

CREATE INDEX IF NOT EXISTS ix_fact_empresa_tamanio
    ON agroindustria.fact_empresa_agroindustrial (tamanio_emp_id);

CREATE OR REPLACE VIEW agroindustria.vw_empresas_agroindustriales AS
SELECT
    f.id_anonimo_emp,
    f.anio,
    c.ciiu,
    c.descripcion AS descripcion_ciiu,
    c.sector,
    u.ubigeo,
    u.departamento,
    u.provincia,
    u.distrito,
    t.tamanio_emp,
    f.valor_estimado_minimo_venta,
    f.valor_estimado_maximo_venta,
    f.exporta,
    f.valor_estimado_minimo_fob_dolar,
    f.valor_estimado_maximo_fob_dolar,
    f.fec_creacion
FROM agroindustria.fact_empresa_agroindustrial f
JOIN agroindustria.dim_ciiu c ON c.ciiu = f.ciiu
JOIN agroindustria.dim_ubigeo u ON u.ubigeo = f.ubigeo
JOIN agroindustria.dim_tamanio_empresa t ON t.tamanio_emp_id = f.tamanio_emp_id;
