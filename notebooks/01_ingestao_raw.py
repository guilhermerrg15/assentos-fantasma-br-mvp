# Databricks notebook source
display(dbutils.fs.ls("/Volumes/workspace/raw/anac_files/"))

# COMMAND ----------

path = "/Volumes/workspace/raw/anac_files/Dados_Estatisticos.csv"

df_head = (
    spark.read
    .option("header", "true")
    .option("sep", ";")
    .option("encoding", "UTF-8")
    .option("inferSchema", "false")
    .option("skipRows", "1")
    .csv(path)
    .limit(5)
)

display(df_head)
print(len(df_head.columns), "colunas")
print(df_head.columns)

# COMMAND ----------

from pyspark.sql import functions as F

df = (
    spark.read
    .option("header", "true")
    .option("sep", ";")
    .option("encoding", "UTF-8")
    .option("inferSchema", "false")
    .option("skipRows", "1")
    .csv(path)
)

ano_col = [c for c in df.columns if c.upper().replace("Ê", "E").startswith("ANO")][0]
print("coluna ano:", ano_col)
print("n colunas:", len(df.columns))

display(df.groupBy(ano_col).count().orderBy(ano_col))
print("linhas totais:", df.count())

# COMMAND ----------

raw = df.where(F.col(ano_col).cast("int").between(2020, 2025))

print("linhas 2020-2025 (antes do write):", raw.count())
print("colunas (sem rename):", len(raw.columns))

(
    raw.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("workspace.raw.anac_dados_estatisticos")
)

display(
    spark.sql("""
        SELECT
          COUNT(*) AS n,
          MIN(CAST(ANO AS INT)) AS ano_min,
          MAX(CAST(ANO AS INT)) AS ano_max,
          COUNT(DISTINCT ANO) AS n_anos
        FROM workspace.raw.anac_dados_estatisticos
    """)
)

display(
    spark.sql("""
        SELECT ANO, COUNT(*) AS n
        FROM workspace.raw.anac_dados_estatisticos
        GROUP BY ANO
        ORDER BY CAST(ANO AS INT)
    """)
)

# COMMAND ----------

