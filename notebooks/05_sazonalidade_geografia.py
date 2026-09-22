# Databricks notebook source
# 05_sazonalidade_geografia
# H3: há meses e UFs com mais assento vazio
# Fonte: mart_kpi_rota_mensal + dim_tempo

from pyspark.sql import functions as F
import pandas as pd
import matplotlib.pyplot as plt
kpi = (
    spark.table("workspace.marts.mart_kpi_rota_mensal")
    .join(
        spark.table("workspace.marts.dim_tempo").select("ano_mes", "eh_pandemia"),
        on="ano_mes",
        how="left",
    )
)
print("linhas kpi:", kpi.count())

# COMMAND ----------

heat = (
    kpi.groupBy("ano", "mes")
    .agg(
        F.sum("assentos").alias("assentos"),
        F.sum("assentos_fantasma").alias("fantasma"),
    )
    .withColumn("taxa", F.col("fantasma") / F.col("assentos"))
    .toPandas()
)

pivot = heat.pivot(index="mes", columns="ano", values="taxa").sort_index()

plt.figure(figsize=(9, 5))
plt.imshow(pivot.values, aspect="auto")
plt.xticks(range(len(pivot.columns)), pivot.columns)
plt.yticks(range(12), range(1, 13))
plt.xlabel("Ano")
plt.ylabel("Mês")
plt.title("Taxa de ociosidade por mês e ano")
plt.colorbar(label="Assentos vazios / assentos")
plt.tight_layout()
plt.show()

display(spark.createDataFrame(heat.sort_values(["ano", "mes"])))

# COMMAND ----------

saz = (
    kpi.groupBy("eh_pandemia", "mes")
    .agg(
        F.sum("assentos").alias("assentos"),
        F.sum("assentos_fantasma").alias("fantasma"),
    )
    .withColumn("taxa", F.col("fantasma") / F.col("assentos"))
    .toPandas()
)

saz["periodo"] = saz["eh_pandemia"].map({True: "2020-21 pandemia", False: "2022-25"})

plt.figure(figsize=(8, 4))
for periodo, g in saz.groupby("periodo"):
    g = g.sort_values("mes")
    plt.plot(g["mes"], g["taxa"] * 100, marker="o", label=periodo)
plt.xticks(range(1, 13))
plt.xlabel("Mês")
plt.ylabel("Ociosidade (%)")
plt.title("Sazonalidade da ociosidade: pandemia vs pós")
plt.legend()
plt.tight_layout()
plt.show()

display(spark.createDataFrame(saz.sort_values(["eh_pandemia", "mes"])))

# COMMAND ----------

uf = (
    kpi.filter(F.col("ano").between(2022, 2025) & F.col("aero_origem_uf").isNotNull())
    .groupBy("aero_origem_uf")
    .agg(
        F.sum("assentos").alias("assentos"),
        F.sum("assentos_fantasma").alias("fantasma"),
    )
    .withColumn("taxa", F.col("fantasma") / F.col("assentos"))
    .orderBy(F.desc("fantasma"))
    .toPandas()
)

top = uf.head(12)

plt.figure(figsize=(8, 5))
plt.barh(top["aero_origem_uf"][::-1], top["fantasma"][::-1] / 1e6)
plt.xlabel("Assentos fantasma (milhões)")
plt.title("Top UF de origem — volume de assentos vazios (2022–2025)")
plt.tight_layout()
plt.show()

display(spark.createDataFrame(uf))

# COMMAND ----------

print("""
Conclusão

H3 — o desperdício não é igual em todo mês nem em toda UF.

Tempo (2022–2025):
- Mês mais ocioso: maio, 22,6%.
- Mês mais ocupado: novembro, 16,7%.
- Julho (férias) fica em 17,5% — mais cheio que a média.
- A diferença maio vs novembro é ~6 pontos: sazonalidade existe, mas a média da malha continua perto de 20%.
- 2020–21 é outro regime: março chega a 30,7%. Não use pandemia como "mês típico".

Espaço (origem, 2022–2025):
- Em VOLUME, São Paulo lidera (29,0 milhões de assentos fantasma), depois RJ, DF e MG.
  Isso acompanha o tamanho da malha, não prova pior gestão.
- Em TAXA, Acre lidera (38,0%), depois PA, MA e PI — rotas mais finas, Norte/Nordeste.
- Volume e taxa contam histórias diferentes: SP desperdiça mais assentos; AC voa mais vazio em %.

Caveat: UF de origem. Ociosidade alta no Norte pode ser aeronave mínima / malha de serviço, não "vergonha".
""")

# COMMAND ----------

