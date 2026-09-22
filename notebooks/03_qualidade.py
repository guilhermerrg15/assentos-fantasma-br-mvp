# Databricks notebook source
# MAGIC %sql
# MAGIC -- 03_qualidade
# MAGIC -- Assentos Fantasma BR — testes do fato e das dims
# MAGIC -- Recorte: doméstico regular, assentos > 0, 2020–2025

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   COUNT(*) AS n_fct,
# MAGIC   MIN(ano) AS ano_min,
# MAGIC   MAX(ano) AS ano_max,
# MAGIC   COUNT(DISTINCT ano_mes) AS n_ano_mes
# MAGIC FROM workspace.marts.fct_voos_mensais;

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
# MAGIC SELECT
# MAGIC   COUNT(*) FILTER (WHERE assentos < 0) AS assentos_negativos,
# MAGIC   COUNT(*) FILTER (WHERE passageiros_pagos < 0 OR passageiros_gratis < 0) AS pax_negativos,
# MAGIC   COUNT(*) FILTER (WHERE taxa_ociosidade < 0 OR taxa_ociosidade > 1) AS ociosidade_invalida,
# MAGIC   COUNT(*) FILTER (WHERE load_factor > 1.05) AS lf_acima_cap,
# MAGIC   COUNT(*) FILTER (WHERE ask IS NULL AND assentos > 0) AS ask_nulo_com_assento
# MAGIC FROM workspace.marts.fct_voos_mensais;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT natureza_norm, grupo_voo_norm, COUNT(*) AS n
# MAGIC FROM workspace.marts.fct_voos_mensais
# MAGIC GROUP BY ALL
# MAGIC ORDER BY n DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT status_rota, COUNT(*) AS n
# MAGIC FROM workspace.marts.fct_voos_mensais
# MAGIC GROUP BY status_rota
# MAGIC ORDER BY n DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   (SELECT COUNT(*) FROM workspace.marts.fct_voos_mensais f
# MAGIC    LEFT JOIN workspace.marts.dim_empresa d ON f.empresa_sigla = d.empresa_sigla
# MAGIC    WHERE d.empresa_sigla IS NULL) AS orfao_empresa,
# MAGIC   (SELECT COUNT(*) FROM workspace.marts.fct_voos_mensais f
# MAGIC    LEFT JOIN workspace.marts.dim_tempo t ON f.ano_mes = t.ano_mes
# MAGIC    WHERE t.ano_mes IS NULL) AS orfao_tempo,
# MAGIC   (SELECT COUNT(*) FROM workspace.marts.fct_voos_mensais f
# MAGIC    LEFT JOIN workspace.marts.dim_rota r ON f.rota_id = r.rota_id
# MAGIC    WHERE r.rota_id IS NULL) AS orfao_rota;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   COUNT(*) AS n_br,
# MAGIC   COUNT(combustivel_litros) AS n_com_combustivel,
# MAGIC   ROUND(COUNT(combustivel_litros) / COUNT(*) * 100, 1) AS pct_preenchido
# MAGIC FROM workspace.marts.fct_voos_mensais
# MAGIC WHERE eh_empresa_br = TRUE;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT empresa_sigla, ano, mes, rota_id, assentos, ask, rpk
# MAGIC FROM workspace.marts.fct_voos_mensais
# MAGIC WHERE ask IS NULL AND assentos > 0;

# COMMAND ----------

