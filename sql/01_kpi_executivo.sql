-- Pergunta: qual o tamanho do desperdício doméstico regular 2020–2025?
SELECT
  SUM(assentos) AS assentos,
  SUM(passageiros_totais) AS passageiros,
  SUM(assentos_fantasma) AS assentos_fantasma,
  SUM(assentos_fantasma) / NULLIF(SUM(assentos), 0) AS taxa_ociosidade,
  LEAST(SUM(rpk) / NULLIF(SUM(ask), 0), 1.05) AS load_factor,
  SUM(ask_ocioso) AS ask_ocioso
FROM workspace.marts.fct_voos_mensais;