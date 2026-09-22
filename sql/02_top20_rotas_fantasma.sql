-- Pergunta: quais rotas mais geram assentos fantasma? (piso do ranking)
SELECT *
FROM workspace.marts.mart_ranking_assentos_fantasma
ORDER BY rank_volume
LIMIT 20;