# De onde vêm os dados — Assentos Fantasma BR

## Quem publicou e como usar

- **Fonte:** Agência Nacional de Aviação Civil (ANAC) — Dados Estatísticos do Transporte Aéreo
- **Setor na ANAC:** acompanhamento de mercado (e-mail `geac@anac.gov.br`)
- **Uso:** dado aberto do governo. Pode usar e adaptar, **citando a ANAC**
- **Como citar:** Fonte: ANAC — Dados Estatísticos do Transporte Aéreo. Elaboração própria.
- **Aviso da própria ANAC:** quem usa o arquivo bruto pode chegar em totais
  diferentes dos relatórios oficiais. Este projeto **não** é estatística oficial.

O CSV é grande (~343 MB) e **não vai para o GitHub**.
Este texto, o código de verificação (hash) e o dicionário **vão**.

---

## Arquivo que o projeto usa

| O quê | Valor |
|---|---|
| Nome | `Dados_Estatisticos.csv` |
| Onde baixar | https://sistemas.anac.gov.br/dadosabertos/Voos%20e%20opera%C3%A7%C3%B5es%20a%C3%A9reas/Dados%20Estat%C3%ADsticos%20do%20Transporte%20A%C3%A9reo/Dados_Estatisticos.csv |
| Página para ler no navegador | https://www.gov.br/anac/pt-br/assuntos/dados-e-estatisticas/dados-estatisticos |
| Página de metadados | https://www.gov.br/anac/pt-br/acesso-a-informacao/dados-abertos/areas-de-atuacao/voos-e-operacoes-aereas/dados-estatisticos-do-transporte-aereo |
| Significado das variáveis | https://www.gov.br/anac/pt-br/assuntos/dados-e-estatisticas/descricao-de-variaveis |
| Primeira linha do arquivo | recado da ANAC (`Atualizado em: …`). Não é nome de coluna |
| Tamanho | 359.963.089 bytes (cerca de 343 MB) |
| Código de verificação SHA-256 | `D64D1E44FE9B99686C1D730AAD8684EEACD35AC671F4B1C5797B23C2B89F3CBC` |
| Letras do arquivo | `utf-8-sig` |
| Separador das colunas | `;` |
| Nomes de coluna entre aspas | sim |
| Linhas de dado | 1.099.729 (sem a linha de aviso e sem o cabeçalho) |
| Onde ficou no Databricks | `/Volumes/workspace/raw/anac_files/Dados_Estatisticos.csv` |

Para baixar de novo: use o link da tabela. Depois confira o SHA-256.
Se o código for outro, o arquivo mudou (a ANAC atualiza o CSV de tempos em tempos).

---

## Como o arquivo é organizado

1. **Linha 1:** recado da ANAC. **Não** é nome de coluna.  
2. **Linha 2:** nomes das 38 colunas.  
3. **Linha 3 em diante:** os dados.

Se a leitura não pular a linha 1, as colunas saem erradas.

No Databricks funcionou assim: `header=true`, `sep=;`, `encoding=UTF-8`, pular 1 linha.

---

## Nomes das 38 colunas (como vieram no arquivo)

Não são `EMPRESA (SIGLA)`. São assim, sem acento:

`EMPRESA_SIGLA`; `EMPRESA_NOME`; `EMPRESA_NACIONALIDADE`; `ANO`; `MES`; `AEROPORTO_DE_ORIGEM_SIGLA`; `AEROPORTO_DE_ORIGEM_NOME`; `AEROPORTO_DE_ORIGEM_UF`; `AEROPORTO_DE_ORIGEM_REGIAO`; `AEROPORTO_DE_ORIGEM_PAIS`; `AEROPORTO_DE_ORIGEM_CONTINENTE`; `AEROPORTO_DE_DESTINO_SIGLA`; `AEROPORTO_DE_DESTINO_NOME`; `AEROPORTO_DE_DESTINO_UF`; `AEROPORTO_DE_DESTINO_REGIAO`; `AEROPORTO_DE_DESTINO_PAIS`; `AEROPORTO_DE_DESTINO_CONTINENTE`; `NATUREZA`; `GRUPO_DE_VOO`; `PASSAGEIROS_PAGOS`; `PASSAGEIROS_GRATIS`; `CARGA_PAGA_KG`; `CARGA_GRATIS_KG`; `CORREIO_KG`; `ASK`; `RPK`; `ATK`; `RTK`; `COMBUSTIVEL_LITROS`; `DISTANCIA_VOADA_KM`; `DECOLAGENS`; `CARGA_PAGA_KM`; `CARGA_GRATIS_KM`; `CORREIO_KM`; `ASSENTOS`; `PAYLOAD`; `HORAS_VOADAS`; `BAGAGEM_KG`

A coluna **`ASSENTOS` existe**. Não foi preciso inventar oferta.

O significado de cada uma está em `docs/data_dictionary.md`.

---

## Anos que o arquivo cobre

O CSV vai de **2000 a 2026** (o último ano pode estar incompleto).

O projeto usa só **2020 a 2025** (anos inteiros).  
O ano mais recente incompleto ficou de fora.

| Ano | Linhas | Meses no arquivo |
|---|---:|---|
| 2000 | 47.988 | 12 |
| 2001 | 48.816 | 12 |
| 2002 | 45.335 | 12 |
| 2003 | 39.821 | 12 |
| 2004 | 40.302 | 12 |
| 2005 | 39.880 | 12 |
| 2006 | 44.000 | 12 |
| 2007 | 45.856 | 12 |
| 2008 | 38.553 | 12 |
| 2009 | 37.983 | 12 |
| 2010 | 44.898 | 12 |
| 2011 | 47.638 | 12 |
| 2012 | 49.604 | 12 |
| 2013 | 47.589 | 12 |
| 2014 | 45.928 | 12 |
| 2015 | 44.119 | 12 |
| 2016 | 39.505 | 12 |
| 2017 | 39.443 | 12 |
| 2018 | 39.754 | 12 |
| 2019 | 37.850 | 12 |
| 2020 | 26.951 | 12 |
| 2021 | 28.660 | 12 |
| 2022 | 35.809 | 12 |
| 2023 | 39.157 | 12 |
| 2024 | 40.381 | 12 |
| 2025 | 37.988 | 12 |
| 2026 | 25.921 | incompleto (fora do projeto) |

Soma **2020–2025:** **208.946** linhas.  
Esse é o recorte gravado na tabela `workspace.raw.anac_dados_estatisticos`.  
O arquivo no disco continua inteiro (todos os anos).

Não baixei planilha por ano. O CSV único veio completo.

---

## Conferência no Databricks

A leitura no workspace bateu com este inventário:

- 38 colunas  
- 1.099.729 linhas no arquivo todo  
- coluna de ano = `ANO`  
- soma 2020–2025 = 208.946  

Natureza e grupo de voo (valores reais) estão no `data_dictionary.md`, seção 6.