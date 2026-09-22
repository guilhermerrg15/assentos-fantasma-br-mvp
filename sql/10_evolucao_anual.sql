-- Pergunta: passageiros sobem e ociosidade cai ao longo de 2020–2025?
SELECT
  ano,
  SUM(passageiros_totais) AS passageiros,
  SUM(assentos) AS assentos,
  SUM(assentos_fantasma) AS assentos_fantasma,
  SUM(assentos_fantasma) / NULLIF(SUM(assentos), 0) AS taxa_ociosidade,
  LEAST(SUM(rpk) / NULLIF(SUM(ask), 0), 1.05) AS load_factor
FROM workspace.marts.fct_voos_mensais
GROUP BY ano
ORDER BY ano;