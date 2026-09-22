-- Pergunta: quais meses voam mais vazios? Separar pandemia.
SELECT
  t.eh_pandemia,
  k.mes,
  SUM(k.assentos) AS assentos,
  SUM(k.assentos_fantasma) AS assentos_fantasma,
  SUM(k.assentos_fantasma) / NULLIF(SUM(k.assentos), 0) AS taxa_ociosidade
FROM workspace.marts.mart_kpi_rota_mensal k
JOIN workspace.marts.dim_tempo t ON k.ano_mes = t.ano_mes
GROUP BY t.eh_pandemia, k.mes
ORDER BY t.eh_pandemia, k.mes;