# Databricks notebook source
# 06_combustivel
# H5: litros por pax sobem com a ociosidade?
# Filtro: eh_empresa_br, combustivel e litros_por_pax não nulos, 2022–2025
# Caveat: combustível ANAC só para empresas brasileiras; aeronave/distância também movem L/pax

from pyspark.sql import functions as F
import pandas as pd
import matplotlib.pyplot as plt

base = (
    spark.table("workspace.marts.fct_voos_mensais")
    .filter(F.col("ano").between(2022, 2025))
    .filter(F.col("eh_empresa_br") == True)
    .filter(F.col("combustivel_litros").isNotNull())
    .filter(F.col("litros_por_pax").isNotNull())
    .filter(F.col("passageiros_totais") > 0)
)

print("linhas no recorte combustível:", base.count())

# COMMAND ----------

faixas = (
    base.withColumn(
        "faixa",
        F.when(F.col("taxa_ociosidade") < 0.20, "0-20%")
         .when(F.col("taxa_ociosidade") < 0.28, "20-28%")
         .when(F.col("taxa_ociosidade") < 0.40, "28-40%")
         .otherwise("40%+"),
    )
    .groupBy("faixa")
    .agg(
        F.count("*").alias("n"),
        F.avg("litros_por_pax").alias("litros_por_pax_medio"),
        F.avg("taxa_ociosidade").alias("ociosidade_media"),
    )
    .toPandas()
)

ordem = ["0-20%", "20-28%", "28-40%", "40%+"]
faixas["faixa"] = pd.Categorical(faixas["faixa"], categories=ordem, ordered=True)
faixas = faixas.sort_values("faixa")

display(spark.createDataFrame(faixas))

plt.figure(figsize=(8, 4))
plt.bar(faixas["faixa"].astype(str), faixas["litros_por_pax_medio"])
plt.ylabel("Litros por passageiro (média)")
plt.xlabel("Faixa de ociosidade")
plt.title("L/pax vs ociosidade — empresas BR, 2022–2025")
plt.tight_layout()
plt.show()

# COMMAND ----------

n = base.count()
amostra = base.select("taxa_ociosidade", "litros_por_pax")
if n > 20000:
    amostra = amostra.sample(False, 20000 / n, seed=42)

pdf = amostra.toPandas()
corr = pdf["taxa_ociosidade"].corr(pdf["litros_por_pax"])
print("linhas usadas na correlação:", len(pdf))
print("correlação ociosidade vs L/pax:", round(corr, 3))

# COMMAND ----------

print("""
Conclusão

H5 — só se confirma na cauda extrema, não na malha típica.

- 0–20%: 37,9 L/pax (n=27.137)
- 20–28%: 35,0 L/pax (n=11.357)
- 28–40%: 36,4 L/pax (n=8.171)
- 40%+: 208,9 L/pax (n=9.438)

Até 40% de ociosidade o combustível por passageiro é estável (~36 L).
No 40%+ o L/pax explode. Motivo mais provável: POUCOS passageiros no denominador
(voo quase vazio), não necessariamente "gastou mais querosene por má gestão".
Correlação ociosidade vs L/pax = 0,20 (fraca, amostra ~20 mil linhas).

Decisão de produto:
- NÃO colocar L/pax como KPI da página executiva.
- Usar combustível só na página de ciência / caveat.
- Preferir ASK ocioso e assentos fantasma como métricas centrais.

Caveat: combustível ANAC só em empresa brasileira. L/pax mistura ociosidade,
distância e tipo de aeronave. Outliers com poucos pax distorcem a média da faixa 40%+.
""")