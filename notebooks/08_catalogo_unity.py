# 08 — Comentários no Unity Catalog
# Arquivo Python normal (não precisa ser notebook).
# Rode no Databricks com o compute ligado, depois do notebook 02 (e do 07 para o cluster).
# Não muda número. Só grava descrição nas tabelas.

def run(sql):
    spark.sql(sql)


run(
    """
    COMMENT ON TABLE workspace.raw.anac_dados_estatisticos IS
    'Bronze. CSV da ANAC 2020-2025, colunas originais em texto. Uma linha = empresa + mes + trecho + natureza + grupo de voo. Fonte: Volume anac_files/Dados_Estatisticos.csv.'
    """
)
run(
    """
    COMMENT ON TABLE workspace.staging.stg_anac_voos IS
    'Silver. Mesmo grao do raw, com TRIM, tipos numericos, natureza_norm e grupo_voo_norm. Ainda inclui internacional e nao regular.'
    """
)
run(
    """
    COMMENT ON TABLE workspace.intermediate.int_voos_mensais IS
    'Silver. Domestico regular, assentos > 0, 2020-2025. Inclui assentos_fantasma, taxa_ociosidade, load_factor e status_rota.'
    """
)
run(
    """
    COMMENT ON TABLE workspace.marts.dim_tempo IS
    'Gold. Dimensao de tempo. Uma linha = um ano_mes. eh_pandemia = anos 2020 e 2021.'
    """
)
run(
    """
    COMMENT ON TABLE workspace.marts.dim_empresa IS
    'Gold. Dimensao de empresa. Uma linha = empresa_sigla. eh_empresa_br define quem informa combustivel.'
    """
)
run(
    """
    COMMENT ON TABLE workspace.marts.dim_aeroporto IS
    'Gold. Dimensao de aeroporto. Origens e destinos unidos. aero_uf vazio se for fora do Brasil.'
    """
)
run(
    """
    COMMENT ON TABLE workspace.marts.dim_rota IS
    'Gold. Dimensao de rota dirigida. rota_id = origem-destino. Ida e volta sao rotas diferentes.'
    """
)
run(
    """
    COMMENT ON TABLE workspace.marts.dim_natureza IS
    'Gold. Dimensao de natureza. Neste recorte so DOMESTICA.'
    """
)
run(
    """
    COMMENT ON TABLE workspace.marts.dim_grupo_voo IS
    'Gold. Dimensao de grupo de voo. Neste recorte so REGULAR.'
    """
)
run(
    """
    COMMENT ON TABLE workspace.marts.fct_voos_mensais IS
    'Gold. Fato mensal do esquema estrela. Chave: empresa + ano + mes + origem + destino + natureza + grupo_voo. Nao pode repetir. Linhagem: int_voos_mensais.'
    """
)

colunas_fato = {
    "empresa_sigla": "Codigo da empresa. Parte da chave.",
    "ano": "Ano do movimento. Dominio 2020-2025.",
    "mes": "Mes do movimento. Dominio 1-12.",
    "ano_mes": "Ano*100+mes. Ex.: 202305 = maio de 2023.",
    "rota_id": "Sigla origem + hifen + sigla destino. Ida e volta sao diferentes.",
    "assentos": "Assentos oferecidos no trecho no mes. Veio do CSV (ASSENTOS).",
    "passageiros_totais": "Pagos + gratis. Quem ocupou assento.",
    "assentos_fantasma": "Assentos menos pessoas, sem ficar negativo.",
    "taxa_ociosidade": "Assentos vazios / assentos. Dominio 0 a 1.",
    "load_factor": "RPK/ASK limitado em 1,05. Conta so passageiro pago.",
    "ask_ocioso": "ASK - RPK, sem ficar negativo.",
    "combustivel_litros": "Litros no trecho. Nulo em empresa estrangeira e normal.",
    "litros_por_pax": "Combustivel / pessoas. Nao usar como KPI executivo.",
    "status_rota": "FORA_ESCOPO, SUBOFERTA, ASSENTOS_FANTASMA, DESPERDICIO_MODERADO ou EFICIENTE.",
    "eh_empresa_br": "Verdadeiro se a nacionalidade contem BRASIL.",
    "natureza_norm": "DOMESTICA neste fato. Sem acento.",
    "grupo_voo_norm": "REGULAR neste fato. Sem acento.",
}

for col, texto in colunas_fato.items():
    run(
        f"ALTER TABLE workspace.marts.fct_voos_mensais ALTER COLUMN {col} COMMENT '{texto}'"
    )

run(
    """
    COMMENT ON TABLE workspace.marts.mart_kpi_rota_mensal IS
    'Gold. Rota + mes, empresas somadas. Recalcula taxa, load factor e status_rota depois da soma.'
    """
)
run(
    """
    COMMENT ON TABLE workspace.marts.mart_ociosidade_empresa_mensal IS
    'Gold. Empresa + mes. Alimenta a pagina executiva do dashboard.'
    """
)
run(
    """
    COMMENT ON TABLE workspace.marts.mart_ociosidade_aeroporto_mensal IS
    'Gold. Aeroporto de origem + mes.'
    """
)
run(
    """
    COMMENT ON TABLE workspace.marts.mart_ranking_assentos_fantasma IS
    'Gold. Uma rota no periodo 2022-2025 com pelo menos 10 mil assentos. rank_volume e rank_taxa.'
    """
)
run(
    """
    COMMENT ON TABLE workspace.analytics.mart_status_rota IS
    'Gold. Copia do KPI de rota com o selo status_rota, para a pagina de analise.'
    """
)
run(
    """
    COMMENT ON TABLE workspace.analytics.rota_clusters IS
    'Gold. Uma rota (2022-2025, >=12 meses, >=50 mil assentos) com cluster_id 0-4 e cluster_nome. Gerado no notebook 07. Silhouette ~0,32.'
    """
)

print("comentarios gravados")

tabelas = spark.sql(
    """
    SELECT table_schema, table_name, comment
    FROM system.information_schema.tables
    WHERE table_catalog = 'workspace'
      AND table_schema IN ('raw', 'staging', 'intermediate', 'marts', 'analytics')
      AND table_type <> 'VIEW'
    ORDER BY table_schema, table_name
    """
)
display(tabelas)

colunas = spark.sql(
    """
    SELECT column_name, data_type, comment
    FROM system.information_schema.columns
    WHERE table_catalog = 'workspace'
      AND table_schema = 'marts'
      AND table_name = 'fct_voos_mensais'
    ORDER BY ordinal_position
    """
)
display(colunas)
