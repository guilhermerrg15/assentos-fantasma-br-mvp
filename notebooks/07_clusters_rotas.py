# Databricks notebook source
# MAGIC %pip install scikit-learn --quiet

# COMMAND ----------

# MAGIC %restart_python

# COMMAND ----------

# Unidade: rota dirigida, 2022–2025 (fora da pandemia no treino)
# Filtro: >= 12 meses e >= 50 mil assentos no período
# Features: ociosidade média, variação, load factor, log(assentos)
# Sem L/pax: a Etapa 7 mostrou que essa métrica explode na cauda e distorce cluster

from pyspark.sql import functions as F
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

rotas = (
    spark.table("workspace.marts.mart_kpi_rota_mensal")
    .filter(F.col("ano").between(2022, 2025))
    .groupBy("rota_id")
    .agg(
        F.count("*").alias("n_meses"),
        F.sum("assentos").alias("assentos"),
        F.avg("taxa_ociosidade").alias("ociosidade_media"),
        F.stddev("taxa_ociosidade").alias("ociosidade_dp"),
        F.avg("load_factor").alias("lf_medio"),
        F.sum("assentos_fantasma").alias("assentos_fantasma"),
    )
    .filter(F.col("n_meses") >= 12)
    .filter(F.col("assentos") >= 50000)
    .filter(F.col("ociosidade_dp").isNotNull())
    .filter(F.col("lf_medio").isNotNull())
)

pdf = rotas.toPandas()
print("rotas no recorte:", len(pdf))
display(spark.createDataFrame(pdf.head(10)))

# COMMAND ----------

pdf = pdf.copy()
pdf["log_assentos"] = np.log(pdf["assentos"])

features = ["ociosidade_media", "ociosidade_dp", "lf_medio", "log_assentos"]
X = pdf[features].to_numpy()
Xz = StandardScaler().fit_transform(X)

linhas = []
for k in range(3, 7):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(Xz)
    sil = silhouette_score(Xz, labels)
    linhas.append({"k": k, "silhouette": sil})
    print(k, round(sil, 3))

sil_df = pd.DataFrame(linhas)
plt.figure(figsize=(6, 3))
plt.plot(sil_df["k"], sil_df["silhouette"], marker="o")
plt.xlabel("k")
plt.ylabel("Silhouette")
plt.title("Escolha de k")
plt.tight_layout()
plt.show()

# COMMAND ----------

K = 5 

km = KMeans(n_clusters=K, random_state=42, n_init=10)
pdf["cluster_id"] = km.fit_predict(Xz)
sil_final = silhouette_score(Xz, pdf["cluster_id"])
print("k:", K, "silhouette:", round(sil_final, 3))

perfil = (
    pdf.groupby("cluster_id")
    .agg(
        n=("rota_id", "count"),
        ociosidade_media=("ociosidade_media", "mean"),
        ociosidade_dp=("ociosidade_dp", "mean"),
        lf_medio=("lf_medio", "mean"),
        assentos_medio=("assentos", "mean"),
        fantasma_medio=("assentos_fantasma", "mean"),
    )
    .reset_index()
)
display(spark.createDataFrame(perfil))

# COMMAND ----------

mapa = {
    0: "INSTAVEL",
    1: "ALTO_VOLUME_EFICIENTE",
    2: "OCIOSO_CRONICO",
    3: "LOTADO",
    4: "OCIOSO_MODERADO",
}

pdf["cluster_nome"] = pdf["cluster_id"].map(mapa)
print(pdf["cluster_nome"].value_counts())

# COMMAND ----------

out = spark.createDataFrame(
    pdf[["rota_id", "n_meses", "assentos", "assentos_fantasma",
         "ociosidade_media", "ociosidade_dp", "lf_medio",
         "cluster_id", "cluster_nome"]]
)

(
    out.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("workspace.analytics.rota_clusters")
)

spark.sql("SELECT cluster_nome, COUNT(*) AS n FROM workspace.analytics.rota_clusters GROUP BY cluster_nome").show()
print("silhouette final:", round(sil_final, 3))

# COMMAND ----------

plt.figure(figsize=(8, 5))
for nome, g in pdf.groupby("cluster_nome"):
    plt.scatter(g["ociosidade_media"], g["lf_medio"], s=18, alpha=0.7, label=nome)
plt.xlabel("Ociosidade média")
plt.ylabel("Load factor médio")
plt.title(f"Clusters de rota (k={K}, silhouette={sil_final:.3f})")
plt.legend()
plt.tight_layout()
plt.show()

# COMMAND ----------

