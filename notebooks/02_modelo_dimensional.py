# Databricks notebook source
# MAGIC %sql
# MAGIC DESCRIBE TABLE workspace.raw.anac_dados_estatisticos;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT NATUREZA, COUNT(*) AS n
# MAGIC FROM workspace.raw.anac_dados_estatisticos
# MAGIC GROUP BY NATUREZA
# MAGIC ORDER BY n DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT GRUPO_DE_VOO, COUNT(*) AS n
# MAGIC FROM workspace.raw.anac_dados_estatisticos
# MAGIC GROUP BY GRUPO_DE_VOO
# MAGIC ORDER BY n DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.staging.stg_anac_voos AS
# MAGIC SELECT
# MAGIC   TRIM(EMPRESA_SIGLA)                          AS empresa_sigla,
# MAGIC   TRIM(EMPRESA_NOME)                           AS empresa_nome,
# MAGIC   UPPER(TRIM(EMPRESA_NACIONALIDADE))           AS empresa_nacionalidade,
# MAGIC
# MAGIC   TRY_CAST(NULLIF(TRIM(ANO), '') AS INT)       AS ano,
# MAGIC   TRY_CAST(NULLIF(TRIM(MES), '') AS INT)       AS mes,
# MAGIC   TRY_CAST(NULLIF(TRIM(ANO), '') AS INT) * 100
# MAGIC     + TRY_CAST(NULLIF(TRIM(MES), '') AS INT)   AS ano_mes,
# MAGIC
# MAGIC   TRIM(AEROPORTO_DE_ORIGEM_SIGLA)              AS aero_origem_sigla,
# MAGIC   TRIM(AEROPORTO_DE_ORIGEM_NOME)               AS aero_origem_nome,
# MAGIC   UPPER(TRIM(AEROPORTO_DE_ORIGEM_UF))          AS aero_origem_uf,
# MAGIC   UPPER(TRIM(AEROPORTO_DE_ORIGEM_REGIAO))      AS aero_origem_regiao,
# MAGIC   UPPER(TRIM(AEROPORTO_DE_ORIGEM_PAIS))        AS aero_origem_pais,
# MAGIC   UPPER(TRIM(AEROPORTO_DE_ORIGEM_CONTINENTE))  AS aero_origem_continente,
# MAGIC
# MAGIC   TRIM(AEROPORTO_DE_DESTINO_SIGLA)             AS aero_destino_sigla,
# MAGIC   TRIM(AEROPORTO_DE_DESTINO_NOME)              AS aero_destino_nome,
# MAGIC   UPPER(TRIM(AEROPORTO_DE_DESTINO_UF))         AS aero_destino_uf,
# MAGIC   UPPER(TRIM(AEROPORTO_DE_DESTINO_REGIAO))     AS aero_destino_regiao,
# MAGIC   UPPER(TRIM(AEROPORTO_DE_DESTINO_PAIS))       AS aero_destino_pais,
# MAGIC   UPPER(TRIM(AEROPORTO_DE_DESTINO_CONTINENTE)) AS aero_destino_continente,
# MAGIC
# MAGIC   TRIM(NATUREZA)                               AS natureza,
# MAGIC   TRIM(GRUPO_DE_VOO)                           AS grupo_voo,
# MAGIC
# MAGIC   -- domínio estável para o filtro da 4.3 (sem acento, maiúsculo)
# MAGIC   TRANSLATE(
# MAGIC     UPPER(TRIM(NATUREZA)),
# MAGIC     'ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇ',
# MAGIC     'AAAAAEEEEIIIIOOOOOUUUUC'
# MAGIC   )                                            AS natureza_norm,
# MAGIC   TRANSLATE(
# MAGIC     UPPER(TRIM(GRUPO_DE_VOO)),
# MAGIC     'ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇ',
# MAGIC     'AAAAAEEEEIIIIOOOOOUUUUC'
# MAGIC   )                                            AS grupo_voo_norm,
# MAGIC
# MAGIC   TRY_CAST(NULLIF(TRIM(PASSAGEIROS_PAGOS), '') AS BIGINT)   AS passageiros_pagos,
# MAGIC   TRY_CAST(NULLIF(TRIM(PASSAGEIROS_GRATIS), '') AS BIGINT)  AS passageiros_gratis,
# MAGIC   TRY_CAST(NULLIF(TRIM(ASSENTOS), '') AS BIGINT)            AS assentos,
# MAGIC   TRY_CAST(NULLIF(TRIM(ASK), '') AS DOUBLE)                 AS ask,
# MAGIC   TRY_CAST(NULLIF(TRIM(RPK), '') AS DOUBLE)                 AS rpk,
# MAGIC   TRY_CAST(NULLIF(TRIM(COMBUSTIVEL_LITROS), '') AS DOUBLE)  AS combustivel_litros,
# MAGIC   TRY_CAST(NULLIF(TRIM(DISTANCIA_VOADA_KM), '') AS DOUBLE)  AS distancia_km,
# MAGIC   TRY_CAST(NULLIF(TRIM(DECOLAGENS), '') AS BIGINT)          AS decolagens,
# MAGIC
# MAGIC   -- passam adiante; não entram no KPI do MVP
# MAGIC   TRY_CAST(NULLIF(TRIM(CARGA_PAGA_KG), '') AS DOUBLE)       AS carga_paga_kg,
# MAGIC   TRY_CAST(NULLIF(TRIM(CARGA_GRATIS_KG), '') AS DOUBLE)     AS carga_gratis_kg,
# MAGIC   TRY_CAST(NULLIF(TRIM(CORREIO_KG), '') AS DOUBLE)          AS correio_kg,
# MAGIC   TRY_CAST(NULLIF(TRIM(ATK), '') AS DOUBLE)                 AS atk,
# MAGIC   TRY_CAST(NULLIF(TRIM(RTK), '') AS DOUBLE)                 AS rtk,
# MAGIC   TRY_CAST(NULLIF(TRIM(CARGA_PAGA_KM), '') AS DOUBLE)       AS carga_paga_km,
# MAGIC   TRY_CAST(NULLIF(TRIM(CARGA_GRATIS_KM), '') AS DOUBLE)     AS carga_gratis_km,
# MAGIC   TRY_CAST(NULLIF(TRIM(CORREIO_KM), '') AS DOUBLE)          AS correio_km,
# MAGIC   TRY_CAST(NULLIF(TRIM(PAYLOAD), '') AS DOUBLE)             AS payload,
# MAGIC   TRY_CAST(NULLIF(TRIM(HORAS_VOADAS), '') AS DOUBLE)        AS horas_voadas,
# MAGIC   TRY_CAST(NULLIF(TRIM(BAGAGEM_KG), '') AS DOUBLE)          AS bagagem_kg
# MAGIC FROM workspace.raw.anac_dados_estatisticos;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   (SELECT COUNT(*) FROM workspace.raw.anac_dados_estatisticos) AS n_raw,
# MAGIC   (SELECT COUNT(*) FROM workspace.staging.stg_anac_voos)       AS n_stg;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT natureza, natureza_norm, COUNT(*) AS n
# MAGIC FROM workspace.staging.stg_anac_voos
# MAGIC GROUP BY ALL
# MAGIC ORDER BY n DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT grupo_voo, grupo_voo_norm, COUNT(*) AS n
# MAGIC FROM workspace.staging.stg_anac_voos
# MAGIC GROUP BY ALL
# MAGIC ORDER BY n DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.intermediate.int_voos_mensais AS
# MAGIC WITH base AS (
# MAGIC   SELECT
# MAGIC     empresa_sigla,
# MAGIC     empresa_nome,
# MAGIC     empresa_nacionalidade,
# MAGIC     CASE
# MAGIC       WHEN TRANSLATE(empresa_nacionalidade, 'ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇ', 'AAAAAEEEEIIIIOOOOOUUUUC')
# MAGIC            LIKE '%BRASIL%'
# MAGIC       THEN TRUE ELSE FALSE
# MAGIC     END AS eh_empresa_br,
# MAGIC     ano,
# MAGIC     mes,
# MAGIC     ano_mes,
# MAGIC     aero_origem_sigla,
# MAGIC     aero_origem_nome,
# MAGIC     aero_origem_uf,
# MAGIC     aero_origem_regiao,
# MAGIC     aero_origem_pais,
# MAGIC     aero_origem_continente,
# MAGIC     aero_destino_sigla,
# MAGIC     aero_destino_nome,
# MAGIC     aero_destino_uf,
# MAGIC     aero_destino_regiao,
# MAGIC     aero_destino_pais,
# MAGIC     aero_destino_continente,
# MAGIC     natureza,
# MAGIC     natureza_norm,
# MAGIC     grupo_voo,
# MAGIC     grupo_voo_norm,
# MAGIC     passageiros_pagos,
# MAGIC     passageiros_gratis,
# MAGIC     COALESCE(passageiros_pagos, 0) + COALESCE(passageiros_gratis, 0) AS passageiros_totais,
# MAGIC     assentos,
# MAGIC     ask,
# MAGIC     rpk,
# MAGIC     combustivel_litros,
# MAGIC     distancia_km,
# MAGIC     decolagens,
# MAGIC     GREATEST(
# MAGIC       assentos - (COALESCE(passageiros_pagos, 0) + COALESCE(passageiros_gratis, 0)),
# MAGIC       0
# MAGIC     ) AS assentos_fantasma,
# MAGIC     GREATEST(
# MAGIC       assentos - (COALESCE(passageiros_pagos, 0) + COALESCE(passageiros_gratis, 0)),
# MAGIC       0
# MAGIC     ) / NULLIF(assentos, 0) AS taxa_ociosidade,
# MAGIC     LEAST(rpk / NULLIF(ask, 0), 1.05) AS load_factor,
# MAGIC     GREATEST(ask - rpk, 0) AS ask_ocioso,
# MAGIC     combustivel_litros / NULLIF(
# MAGIC       COALESCE(passageiros_pagos, 0) + COALESCE(passageiros_gratis, 0),
# MAGIC       0
# MAGIC     ) AS litros_por_pax,
# MAGIC     combustivel_litros / NULLIF(rpk, 0) AS eficiencia_combustivel
# MAGIC   FROM workspace.staging.stg_anac_voos
# MAGIC   WHERE natureza_norm = 'DOMESTICA'
# MAGIC     AND grupo_voo_norm = 'REGULAR'
# MAGIC     AND assentos > 0
# MAGIC     AND ano BETWEEN 2020 AND 2025
# MAGIC )
# MAGIC SELECT
# MAGIC   *,
# MAGIC   CASE
# MAGIC     WHEN assentos < 5000 THEN 'FORA_ESCOPO'
# MAGIC     WHEN load_factor >= 0.92 THEN 'SUBOFERTA'
# MAGIC     WHEN taxa_ociosidade >= 0.40 AND assentos >= 10000 THEN 'ASSENTOS_FANTASMA'
# MAGIC     WHEN taxa_ociosidade >= 0.28 THEN 'DESPERDICIO_MODERADO'
# MAGIC     ELSE 'EFICIENTE'
# MAGIC   END AS status_rota
# MAGIC FROM base;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   COUNT(*) AS n_int,
# MAGIC   MIN(ano) AS ano_min,
# MAGIC   MAX(ano) AS ano_max,
# MAGIC   SUM(assentos_fantasma) AS assentos_fantasma_total
# MAGIC FROM workspace.intermediate.int_voos_mensais;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT status_rota, COUNT(*) AS n
# MAGIC FROM workspace.intermediate.int_voos_mensais
# MAGIC GROUP BY status_rota
# MAGIC ORDER BY n DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS workspace.marts;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.marts.dim_tempo AS
# MAGIC SELECT DISTINCT
# MAGIC   ano,
# MAGIC   mes,
# MAGIC   ano_mes,
# MAGIC   CASE
# MAGIC     WHEN mes IN (1, 2, 3) THEN 1
# MAGIC     WHEN mes IN (4, 5, 6) THEN 2
# MAGIC     WHEN mes IN (7, 8, 9) THEN 3
# MAGIC     ELSE 4
# MAGIC   END AS trimestre,
# MAGIC   CASE WHEN mes <= 6 THEN 1 ELSE 2 END AS semestre,
# MAGIC   (ano IN (2020, 2021)) AS eh_pandemia
# MAGIC FROM workspace.intermediate.int_voos_mensais;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.marts.dim_empresa AS
# MAGIC SELECT
# MAGIC   empresa_sigla,
# MAGIC   MAX(empresa_nome) AS empresa_nome,
# MAGIC   MAX(empresa_nacionalidade) AS empresa_nacionalidade,
# MAGIC   MAX(eh_empresa_br) AS eh_empresa_br
# MAGIC FROM workspace.intermediate.int_voos_mensais
# MAGIC GROUP BY empresa_sigla;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.marts.dim_aeroporto AS
# MAGIC SELECT
# MAGIC   aero_sigla,
# MAGIC   MAX(aero_nome) AS aero_nome,
# MAGIC   MAX(aero_uf) AS aero_uf,
# MAGIC   MAX(aero_regiao) AS aero_regiao,
# MAGIC   MAX(aero_pais) AS aero_pais,
# MAGIC   MAX(aero_continente) AS aero_continente
# MAGIC FROM (
# MAGIC   SELECT
# MAGIC     aero_origem_sigla AS aero_sigla,
# MAGIC     aero_origem_nome AS aero_nome,
# MAGIC     aero_origem_uf AS aero_uf,
# MAGIC     aero_origem_regiao AS aero_regiao,
# MAGIC     aero_origem_pais AS aero_pais,
# MAGIC     aero_origem_continente AS aero_continente
# MAGIC   FROM workspace.intermediate.int_voos_mensais
# MAGIC   UNION ALL
# MAGIC   SELECT
# MAGIC     aero_destino_sigla,
# MAGIC     aero_destino_nome,
# MAGIC     aero_destino_uf,
# MAGIC     aero_destino_regiao,
# MAGIC     aero_destino_pais,
# MAGIC     aero_destino_continente
# MAGIC   FROM workspace.intermediate.int_voos_mensais
# MAGIC )
# MAGIC GROUP BY aero_sigla;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.marts.dim_rota AS
# MAGIC SELECT
# MAGIC   CONCAT(aero_origem_sigla, '-', aero_destino_sigla) AS rota_id,
# MAGIC   aero_origem_sigla,
# MAGIC   MAX(aero_origem_nome) AS aero_origem_nome,
# MAGIC   MAX(aero_origem_uf) AS aero_origem_uf,
# MAGIC   MAX(aero_origem_regiao) AS aero_origem_regiao,
# MAGIC   aero_destino_sigla,
# MAGIC   MAX(aero_destino_nome) AS aero_destino_nome,
# MAGIC   MAX(aero_destino_uf) AS aero_destino_uf,
# MAGIC   MAX(aero_destino_regiao) AS aero_destino_regiao,
# MAGIC   TRUE AS eh_domestica
# MAGIC FROM workspace.intermediate.int_voos_mensais
# MAGIC GROUP BY aero_origem_sigla, aero_destino_sigla;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.marts.dim_natureza AS
# MAGIC SELECT DISTINCT natureza, natureza_norm
# MAGIC FROM workspace.intermediate.int_voos_mensais;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.marts.dim_grupo_voo AS
# MAGIC SELECT DISTINCT grupo_voo, grupo_voo_norm
# MAGIC FROM workspace.intermediate.int_voos_mensais;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'dim_tempo' AS dim, COUNT(*) AS n FROM workspace.marts.dim_tempo
# MAGIC UNION ALL
# MAGIC SELECT 'dim_empresa', COUNT(*) FROM workspace.marts.dim_empresa
# MAGIC UNION ALL
# MAGIC SELECT 'dim_aeroporto', COUNT(*) FROM workspace.marts.dim_aeroporto
# MAGIC UNION ALL
# MAGIC SELECT 'dim_rota', COUNT(*) FROM workspace.marts.dim_rota
# MAGIC UNION ALL
# MAGIC SELECT 'dim_natureza', COUNT(*) FROM workspace.marts.dim_natureza
# MAGIC UNION ALL
# MAGIC SELECT 'dim_grupo_voo', COUNT(*) FROM workspace.marts.dim_grupo_voo;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.marts.fct_voos_mensais AS
# MAGIC SELECT
# MAGIC   empresa_sigla,
# MAGIC   empresa_nome,
# MAGIC   empresa_nacionalidade,
# MAGIC   eh_empresa_br,
# MAGIC   ano,
# MAGIC   mes,
# MAGIC   ano_mes,
# MAGIC   aero_origem_sigla,
# MAGIC   aero_origem_nome,
# MAGIC   aero_origem_uf,
# MAGIC   aero_origem_regiao,
# MAGIC   aero_destino_sigla,
# MAGIC   aero_destino_nome,
# MAGIC   aero_destino_uf,
# MAGIC   aero_destino_regiao,
# MAGIC   CONCAT(aero_origem_sigla, '-', aero_destino_sigla) AS rota_id,
# MAGIC   natureza,
# MAGIC   natureza_norm,
# MAGIC   grupo_voo,
# MAGIC   grupo_voo_norm,
# MAGIC   passageiros_pagos,
# MAGIC   passageiros_gratis,
# MAGIC   passageiros_totais,
# MAGIC   assentos,
# MAGIC   assentos_fantasma,
# MAGIC   taxa_ociosidade,
# MAGIC   ask,
# MAGIC   rpk,
# MAGIC   load_factor,
# MAGIC   ask_ocioso,
# MAGIC   combustivel_litros,
# MAGIC   litros_por_pax,
# MAGIC   eficiencia_combustivel,
# MAGIC   distancia_km,
# MAGIC   decolagens,
# MAGIC   status_rota
# MAGIC FROM workspace.intermediate.int_voos_mensais;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS n_fct
# MAGIC FROM workspace.marts.fct_voos_mensais;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS duplicatas
# MAGIC FROM (
# MAGIC   SELECT empresa_sigla, ano, mes, aero_origem_sigla, aero_destino_sigla, natureza, grupo_voo
# MAGIC   FROM workspace.marts.fct_voos_mensais
# MAGIC   GROUP BY ALL
# MAGIC   HAVING COUNT(*) > 1
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS workspace.analytics;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.marts.mart_kpi_rota_mensal AS
# MAGIC WITH agg AS (
# MAGIC   SELECT
# MAGIC     rota_id,
# MAGIC     MAX(aero_origem_sigla) AS aero_origem_sigla,
# MAGIC     MAX(aero_origem_nome) AS aero_origem_nome,
# MAGIC     MAX(aero_origem_uf) AS aero_origem_uf,
# MAGIC     MAX(aero_origem_regiao) AS aero_origem_regiao,
# MAGIC     MAX(aero_destino_sigla) AS aero_destino_sigla,
# MAGIC     MAX(aero_destino_nome) AS aero_destino_nome,
# MAGIC     MAX(aero_destino_uf) AS aero_destino_uf,
# MAGIC     MAX(aero_destino_regiao) AS aero_destino_regiao,
# MAGIC     ano,
# MAGIC     mes,
# MAGIC     ano_mes,
# MAGIC     SUM(passageiros_totais) AS passageiros_totais,
# MAGIC     SUM(assentos) AS assentos,
# MAGIC     SUM(assentos_fantasma) AS assentos_fantasma,
# MAGIC     SUM(ask) AS ask,
# MAGIC     SUM(rpk) AS rpk,
# MAGIC     SUM(ask_ocioso) AS ask_ocioso,
# MAGIC     SUM(decolagens) AS decolagens,
# MAGIC     SUM(combustivel_litros) AS combustivel_litros
# MAGIC   FROM workspace.marts.fct_voos_mensais
# MAGIC   GROUP BY rota_id, ano, mes, ano_mes
# MAGIC )
# MAGIC SELECT
# MAGIC   *,
# MAGIC   assentos_fantasma / NULLIF(assentos, 0) AS taxa_ociosidade,
# MAGIC   LEAST(rpk / NULLIF(ask, 0), 1.05) AS load_factor,
# MAGIC   CASE
# MAGIC     WHEN assentos < 5000 THEN 'FORA_ESCOPO'
# MAGIC     WHEN LEAST(rpk / NULLIF(ask, 0), 1.05) >= 0.92 THEN 'SUBOFERTA'
# MAGIC     WHEN assentos_fantasma / NULLIF(assentos, 0) >= 0.40 AND assentos >= 10000 THEN 'ASSENTOS_FANTASMA'
# MAGIC     WHEN assentos_fantasma / NULLIF(assentos, 0) >= 0.28 THEN 'DESPERDICIO_MODERADO'
# MAGIC     ELSE 'EFICIENTE'
# MAGIC   END AS status_rota
# MAGIC FROM agg;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.marts.mart_ociosidade_empresa_mensal AS
# MAGIC SELECT
# MAGIC   empresa_sigla,
# MAGIC   MAX(empresa_nome) AS empresa_nome,
# MAGIC   MAX(eh_empresa_br) AS eh_empresa_br,
# MAGIC   ano,
# MAGIC   mes,
# MAGIC   ano_mes,
# MAGIC   SUM(passageiros_totais) AS passageiros_totais,
# MAGIC   SUM(assentos) AS assentos,
# MAGIC   SUM(assentos_fantasma) AS assentos_fantasma,
# MAGIC   SUM(assentos_fantasma) / NULLIF(SUM(assentos), 0) AS taxa_ociosidade,
# MAGIC   SUM(ask) AS ask,
# MAGIC   SUM(rpk) AS rpk,
# MAGIC   LEAST(SUM(rpk) / NULLIF(SUM(ask), 0), 1.05) AS load_factor,
# MAGIC   SUM(ask_ocioso) AS ask_ocioso,
# MAGIC   SUM(combustivel_litros) AS combustivel_litros,
# MAGIC   SUM(combustivel_litros) / NULLIF(SUM(passageiros_totais), 0) AS litros_por_pax
# MAGIC FROM workspace.marts.fct_voos_mensais
# MAGIC GROUP BY empresa_sigla, ano, mes, ano_mes;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.marts.mart_ociosidade_aeroporto_mensal AS
# MAGIC SELECT
# MAGIC   aero_origem_sigla AS aero_sigla,
# MAGIC   MAX(aero_origem_nome) AS aero_nome,
# MAGIC   MAX(aero_origem_uf) AS aero_uf,
# MAGIC   MAX(aero_origem_regiao) AS aero_regiao,
# MAGIC   ano,
# MAGIC   mes,
# MAGIC   ano_mes,
# MAGIC   SUM(passageiros_totais) AS passageiros_totais,
# MAGIC   SUM(assentos) AS assentos,
# MAGIC   SUM(assentos_fantasma) AS assentos_fantasma,
# MAGIC   SUM(assentos_fantasma) / NULLIF(SUM(assentos), 0) AS taxa_ociosidade,
# MAGIC   SUM(ask) AS ask,
# MAGIC   SUM(rpk) AS rpk,
# MAGIC   SUM(decolagens) AS decolagens
# MAGIC FROM workspace.marts.fct_voos_mensais
# MAGIC GROUP BY aero_origem_sigla, ano, mes, ano_mes;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.marts.mart_ranking_assentos_fantasma AS
# MAGIC WITH agg AS (
# MAGIC   SELECT
# MAGIC     rota_id,
# MAGIC     MAX(aero_origem_sigla) AS aero_origem_sigla,
# MAGIC     MAX(aero_origem_nome) AS aero_origem_nome,
# MAGIC     MAX(aero_origem_uf) AS aero_origem_uf,
# MAGIC     MAX(aero_destino_sigla) AS aero_destino_sigla,
# MAGIC     MAX(aero_destino_nome) AS aero_destino_nome,
# MAGIC     MAX(aero_destino_uf) AS aero_destino_uf,
# MAGIC     SUM(assentos) AS assentos,
# MAGIC     SUM(assentos_fantasma) AS assentos_fantasma,
# MAGIC     SUM(passageiros_totais) AS passageiros_totais,
# MAGIC     SUM(ask) AS ask,
# MAGIC     SUM(rpk) AS rpk,
# MAGIC     SUM(ask_ocioso) AS ask_ocioso
# MAGIC   FROM workspace.marts.fct_voos_mensais
# MAGIC   WHERE ano BETWEEN 2022 AND 2025
# MAGIC   GROUP BY rota_id
# MAGIC )
# MAGIC SELECT
# MAGIC   *,
# MAGIC   assentos_fantasma / NULLIF(assentos, 0) AS taxa_ociosidade,
# MAGIC   LEAST(rpk / NULLIF(ask, 0), 1.05) AS load_factor,
# MAGIC   RANK() OVER (ORDER BY assentos_fantasma DESC) AS rank_volume,
# MAGIC   RANK() OVER (ORDER BY assentos_fantasma / NULLIF(assentos, 0) DESC) AS rank_taxa
# MAGIC FROM agg
# MAGIC WHERE assentos >= 10000;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.analytics.mart_status_rota AS
# MAGIC SELECT
# MAGIC   rota_id,
# MAGIC   aero_origem_sigla,
# MAGIC   aero_origem_uf,
# MAGIC   aero_destino_sigla,
# MAGIC   aero_destino_uf,
# MAGIC   ano,
# MAGIC   mes,
# MAGIC   ano_mes,
# MAGIC   assentos,
# MAGIC   assentos_fantasma,
# MAGIC   taxa_ociosidade,
# MAGIC   load_factor,
# MAGIC   status_rota
# MAGIC FROM workspace.marts.mart_kpi_rota_mensal;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW workspace.analytics.vw_pbi_executivo_ociosidade AS
# MAGIC SELECT
# MAGIC   e.ano,
# MAGIC   e.mes,
# MAGIC   e.ano_mes,
# MAGIC   t.eh_pandemia,
# MAGIC   e.empresa_sigla,
# MAGIC   e.empresa_nome,
# MAGIC   e.eh_empresa_br,
# MAGIC   e.passageiros_totais,
# MAGIC   e.assentos,
# MAGIC   e.assentos_fantasma,
# MAGIC   e.taxa_ociosidade,
# MAGIC   e.load_factor,
# MAGIC   e.ask,
# MAGIC   e.rpk,
# MAGIC   e.ask_ocioso,
# MAGIC   e.combustivel_litros,
# MAGIC   e.litros_por_pax
# MAGIC FROM workspace.marts.mart_ociosidade_empresa_mensal e
# MAGIC LEFT JOIN workspace.marts.dim_tempo t
# MAGIC   ON e.ano_mes = t.ano_mes;
# MAGIC
# MAGIC CREATE OR REPLACE VIEW workspace.analytics.vw_pbi_ranking_fantasma AS
# MAGIC SELECT *
# MAGIC FROM workspace.marts.mart_ranking_assentos_fantasma;
# MAGIC
# MAGIC CREATE OR REPLACE VIEW workspace.analytics.vw_pbi_sazonalidade_desperdicio AS
# MAGIC SELECT
# MAGIC   k.ano,
# MAGIC   k.mes,
# MAGIC   k.ano_mes,
# MAGIC   t.eh_pandemia,
# MAGIC   k.aero_origem_uf,
# MAGIC   k.aero_origem_regiao,
# MAGIC   SUM(k.assentos) AS assentos,
# MAGIC   SUM(k.assentos_fantasma) AS assentos_fantasma,
# MAGIC   SUM(k.ask) AS ask,
# MAGIC   SUM(k.ask_ocioso) AS ask_ocioso
# MAGIC FROM workspace.marts.mart_kpi_rota_mensal k
# MAGIC LEFT JOIN workspace.marts.dim_tempo t
# MAGIC   ON k.ano_mes = t.ano_mes
# MAGIC GROUP BY k.ano, k.mes, k.ano_mes, t.eh_pandemia, k.aero_origem_uf, k.aero_origem_regiao;
# MAGIC
# MAGIC CREATE OR REPLACE VIEW workspace.analytics.vw_pbi_empresa_eficiencia AS
# MAGIC SELECT *
# MAGIC FROM workspace.marts.mart_ociosidade_empresa_mensal;
# MAGIC
# MAGIC CREATE OR REPLACE VIEW workspace.analytics.vw_pbi_contraste_suboferta AS
# MAGIC SELECT
# MAGIC   ano,
# MAGIC   mes,
# MAGIC   ano_mes,
# MAGIC   status_rota,
# MAGIC   COUNT(*) AS n_rotas,
# MAGIC   SUM(assentos) AS assentos,
# MAGIC   SUM(assentos_fantasma) AS assentos_fantasma
# MAGIC FROM workspace.marts.mart_kpi_rota_mensal
# MAGIC WHERE status_rota <> 'FORA_ESCOPO'
# MAGIC GROUP BY ano, mes, ano_mes, status_rota;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'kpi_rota' AS obj, COUNT(*) AS n FROM workspace.marts.mart_kpi_rota_mensal
# MAGIC UNION ALL
# MAGIC SELECT 'empresa', COUNT(*) FROM workspace.marts.mart_ociosidade_empresa_mensal
# MAGIC UNION ALL
# MAGIC SELECT 'aeroporto', COUNT(*) FROM workspace.marts.mart_ociosidade_aeroporto_mensal
# MAGIC UNION ALL
# MAGIC SELECT 'ranking', COUNT(*) FROM workspace.marts.mart_ranking_assentos_fantasma
# MAGIC UNION ALL
# MAGIC SELECT 'status_rota', COUNT(*) FROM workspace.analytics.mart_status_rota;

# COMMAND ----------

