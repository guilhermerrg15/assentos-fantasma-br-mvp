-- Pergunta: quais aeroportos mais “exportam” assentos vazios?
SELECT
  aero_sigla,
  MAX(aero_nome) AS aero_nome,
  MAX(aero_uf) AS aero_uf,
  SUM(assentos_fantasma) AS assentos_fantasma,
  SUM(assentos_fantasma) / NULLIF(SUM(assentos), 0) AS taxa_ociosidade
FROM workspace.marts.mart_ociosidade_aeroporto_mensal
WHERE ano BETWEEN 2022 AND 2025
GROUP BY aero_sigla
ORDER BY assentos_fantasma DESC
LIMIT 20;