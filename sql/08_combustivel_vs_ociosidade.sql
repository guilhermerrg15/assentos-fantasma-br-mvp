-- Pergunta: L/pax piora com ociosidade? Só empresa BR e combustível preenchido (H5)
SELECT
  CASE
    WHEN taxa_ociosidade < 0.20 THEN '0-20%'
    WHEN taxa_ociosidade < 0.28 THEN '20-28%'
    WHEN taxa_ociosidade < 0.40 THEN '28-40%'
    ELSE '40%+'
  END AS faixa_ociosidade,
  COUNT(*) AS n,
  AVG(litros_por_pax) AS litros_por_pax_medio
FROM workspace.marts.fct_voos_mensais
WHERE eh_empresa_br = TRUE
  AND combustivel_litros IS NOT NULL
  AND litros_por_pax IS NOT NULL
  AND ano BETWEEN 2022 AND 2025
GROUP BY 1
ORDER BY 1;