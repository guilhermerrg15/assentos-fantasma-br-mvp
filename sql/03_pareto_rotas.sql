-- Pergunta: o desperdício se concentra em poucas rotas? (H2, 2022–2025)
WITH base AS (
  SELECT
    rota_id,
    assentos_fantasma,
    SUM(assentos_fantasma) OVER () AS total_fantasma,
    SUM(assentos_fantasma) OVER (ORDER BY assentos_fantasma DESC) AS fantasma_acum
  FROM workspace.marts.mart_ranking_assentos_fantasma
)
SELECT
  COUNT(*) AS n_rotas,
  SUM(CASE WHEN fantasma_acum / NULLIF(total_fantasma, 0) <= 0.50 THEN 1 ELSE 0 END) AS rotas_ate_50pct,
  SUM(CASE WHEN fantasma_acum / NULLIF(total_fantasma, 0) <= 0.80 THEN 1 ELSE 0 END) AS rotas_ate_80pct
FROM base;