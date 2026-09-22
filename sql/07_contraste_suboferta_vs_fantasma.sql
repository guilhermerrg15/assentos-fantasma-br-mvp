-- Pergunta: no mesmo recorte, quantas rotas-mês em cada status? (H4)
SELECT
  ano,
  status_rota,
  COUNT(*) AS n_rotas_mes,
  SUM(assentos_fantasma) AS assentos_fantasma
FROM workspace.marts.mart_kpi_rota_mensal
WHERE status_rota <> 'FORA_ESCOPO'
GROUP BY ano, status_rota
ORDER BY ano, status_rota;