-- Pergunta: volume vs taxa por empresa (2022–2025)
SELECT
  empresa_sigla,
  MAX(empresa_nome) AS empresa_nome,
  SUM(assentos) AS assentos,
  SUM(assentos_fantasma) AS assentos_fantasma,
  SUM(assentos_fantasma) / NULLIF(SUM(assentos), 0) AS taxa_ociosidade,
  LEAST(SUM(rpk) / NULLIF(SUM(ask), 0), 1.05) AS load_factor
FROM workspace.marts.mart_ociosidade_empresa_mensal
WHERE ano BETWEEN 2022 AND 2025
GROUP BY empresa_sigla
ORDER BY assentos_fantasma DESC;