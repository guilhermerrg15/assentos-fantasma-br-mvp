-- Rotas que ficaram com muito assento vazio (status ASSENTOS_FANTASMA)
-- em pelo menos 4 meses do mesmo ano.
-- O corte de 8 meses não achou ninguém: o máximo no dado é 4 meses.

SELECT
  ano,
  rota_id,
  COUNT(*) AS qtd_meses,
  SUM(assentos_fantasma) AS assentos_vazios
FROM workspace.marts.mart_kpi_rota_mensal
WHERE status_rota = 'ASSENTOS_FANTASMA'
GROUP BY ano, rota_id
HAVING COUNT(*) >= 4
ORDER BY qtd_meses DESC, assentos_vazios DESC;