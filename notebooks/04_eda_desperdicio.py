# Databricks notebook source
# 04_eda_desperdicio
# H1: parte relevante da oferta doméstica regular opera com ociosidade alta (>= 28%)
# H2: o desperdício se concentra em poucas rotas (Pareto)
# Fonte: workspace.marts (doméstico regular, assentos > 0, 2020–2025)
# Caveat: ociosidade alta ≠ má gestão (malha, aeronave mínima, pandemia, carga)

from pyspark.sql import functions as F
import matplotlib.pyplot as plt
import pandas as pd

fct = spark.table("workspace.marts.fct_voos_mensais")
print("linhas:", fct.count())

# COMMAND ----------

h1 = (
    fct.agg(
        F.sum("assentos").alias("assentos"),
        F.sum("assentos_fantasma").alias("fantasma"),
        F.sum(F.when(F.col("taxa_ociosidade") >= 0.28, F.col("assentos")).otherwise(0)).alias("assentos_alta_ociosidade"),
    )
    .withColumn("taxa_ociosidade_geral", F.col("fantasma") / F.col("assentos"))
    .withColumn("share_assentos_alta_ociosidade", F.col("assentos_alta_ociosidade") / F.col("assentos"))
)

display(h1)

# COMMAND ----------

bins = (
    fct.withColumn(
        "faixa",
        F.when(F.col("taxa_ociosidade") < 0.20, "0-20%")
         .when(F.col("taxa_ociosidade") < 0.28, "20-28%")
         .when(F.col("taxa_ociosidade") < 0.40, "28-40%")
         .otherwise("40%+"),
    )
    .groupBy("faixa")
    .agg(F.sum("assentos").alias("assentos"))
    .toPandas()
)

ordem = ["0-20%", "20-28%", "28-40%", "40%+"]
bins["faixa"] = pd.Categorical(bins["faixa"], categories=ordem, ordered=True)
bins = bins.sort_values("faixa")

plt.figure(figsize=(8, 4))
plt.bar(bins["faixa"].astype(str), bins["assentos"] / 1e6)
plt.ylabel("Assentos (milhões)")
plt.xlabel("Taxa de ociosidade da linha (empresa-rota-mês)")
plt.title("Distribuição da oferta por faixa de ociosidade")
plt.tight_layout()
plt.show()

# COMMAND ----------

pareto = spark.sql("""
WITH r AS (
  SELECT
    rota_id,
    SUM(assentos_fantasma) AS fantasma
  FROM workspace.marts.mart_ranking_assentos_fantasma
  GROUP BY rota_id
),
o AS (
  SELECT
    rota_id,
    fantasma,
    SUM(fantasma) OVER () AS total,
    SUM(fantasma) OVER (ORDER BY fantasma DESC) AS acum
  FROM r
)
SELECT
  COUNT(*) AS n_rotas,
  SUM(CASE WHEN acum / total <= 0.50 THEN 1 ELSE 0 END) AS rotas_50pct,
  SUM(CASE WHEN acum / total <= 0.80 THEN 1 ELSE 0 END) AS rotas_80pct,
  MAX(total) AS fantasma_total
FROM o
""")

display(pareto)

# COMMAND ----------

curva = spark.sql("""
WITH r AS (
  SELECT rota_id, SUM(assentos_fantasma) AS fantasma
  FROM workspace.marts.mart_ranking_assentos_fantasma
  GROUP BY rota_id
),
o AS (
  SELECT
    ROW_NUMBER() OVER (ORDER BY fantasma DESC) AS rank,
    COUNT(*) OVER () AS n,
    SUM(fantasma) OVER (ORDER BY fantasma DESC) / SUM(fantasma) OVER () AS share_acum
  FROM r
)
SELECT rank, n, share_acum, rank / n AS share_rotas
FROM o
ORDER BY rank
""").toPandas()

plt.figure(figsize=(8, 4))
plt.plot(curva["share_rotas"] * 100, curva["share_acum"] * 100)
plt.xlabel("% das rotas (ranking, as mais ociosas primeiro)")
plt.ylabel("% acumulado dos assentos fantasma")
plt.title("Pareto do desperdício (2022–2025, piso 10 mil assentos)")
plt.axhline(80, linestyle="--", linewidth=1)
plt.tight_layout()
plt.show()

# COMMAND ----------

print("""
Conclusão

H1 — ociosidade alta é minoria da oferta, não o padrão.
- Taxa geral de ociosidade (assentos vazios / assentos): 19,7%.
- Só 16,7% dos assentos estão em linhas com ociosidade >= 28%.
- Isso NÃO confirma “a maior parte da malha voa vazia”. Confirma que existe uma fatia material (~1 em 6 assentos) em linhas folgadas demais.
- 19,7% de vazio é compatível com folga comercial normal (15–25%). O problema está na cauda (28% e 40%+), não na média.

H2 — há concentração, mas não é 80/20 clássico.
- O ranking (2022–2025, piso 10 mil assentos) tem 891 rotas.
- 90 rotas (~10%) concentram 50% dos assentos fantasma.
- 281 rotas (~32%) concentram 80% dos assentos fantasma.
- Há Pareto na metade do desperdício (poucas rotas puxam metade). Para chegar a 80% precisa de quase 1/3 das rotas — concentração moderada, não um punhado de “vilões”.

Caveats
- H1 usa o fato 2020–2025 (inclui pandemia). H2 usa só 2022–2025.
- Status ASSENTOS_FANTASMA no mês é raro e intermitente (máx. 4 meses/ano).
- Ociosidade alta ≠ má gestão: aeronave mínima, malha, hub, carga, 2020–21.
""")