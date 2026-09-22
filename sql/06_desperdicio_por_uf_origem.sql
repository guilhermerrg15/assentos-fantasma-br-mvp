-- Pergunta: onde a oferta ociosa nasce? (UF de origem, 2022–2025)
SELECT
  aero_origem_uf,
  SUM(assentos) AS assentos,
  SUM(assentos_fantasma) AS assentos_fantasma,
  SUM(assentos_fantasma) / NULLIF(SUM(assentos), 0) AS taxa_ociosidade
FROM workspace.marts.mart_kpi_rota_mensal
WHERE ano BETWEEN 2022 AND 2025
  AND aero_origem_uf IS NOT NULL
GROUP BY aero_origem_uf
ORDER BY assentos_fantasma DESC;