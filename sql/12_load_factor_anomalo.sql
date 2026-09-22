-- Pergunta: qualidade — LF estourado ou ASK nulo com assentos?
SELECT
  COUNT(*) FILTER (WHERE load_factor > 1.05) AS lf_acima_cap,
  COUNT(*) FILTER (WHERE ask IS NULL AND assentos > 0) AS ask_nulo_com_assento,
  COUNT(*) FILTER (WHERE taxa_ociosidade < 0 OR taxa_ociosidade > 1) AS ociosidade_invalida
FROM workspace.marts.fct_voos_mensais;