# De onde vêm os dados

O arquivo deste projeto é o CSV de Dados Estatísticos do Transporte Aéreo, publicado pela ANAC (Agência Nacional de Aviação Civil). O setor que cuida disso na Agência é o de acompanhamento de mercado. O e-mail que eles colocam no portal é `geac@anac.gov.br`.

É dado aberto. Dá para usar e adaptar, citando a ANAC. Eu cito: Fonte: ANAC, Dados Estatísticos do Transporte Aéreo. Elaboração própria.

Eles mesmos avisam que quem trabalha em cima do arquivo bruto pode chegar em totais diferentes do relatório oficial. Este projeto não é estatística oficial.

O CSV pesa uns 343 MB, então não sobe no GitHub. Este texto sobe, o hash sobe e o dicionário também.

## Arquivo que eu usei

| Campo | Valor |
|---|---|
| Nome | `Dados_Estatisticos.csv` |
| Download | https://sistemas.anac.gov.br/dadosabertos/Voos%20e%20opera%C3%A7%C3%B5es%20a%C3%A9reas/Dados%20Estat%C3%ADsticos%20do%20Transporte%20A%C3%A9reo/Dados_Estatisticos.csv |
| Página no navegador | https://www.gov.br/anac/pt-br/assuntos/dados-e-estatisticas/dados-estatisticos |
| Metadados | https://www.gov.br/anac/pt-br/acesso-a-informacao/dados-abertos/areas-de-atuacao/voos-e-operacoes-aereas/dados-estatisticos-do-transporte-aereo |
| Significado das variáveis | https://www.gov.br/anac/pt-br/assuntos/dados-e-estatisticas/descricao-de-variaveis |
| Primeira linha | recado da ANAC (`Atualizado em: ...`). Não é nome de coluna |
| Tamanho | 359.963.089 bytes (cerca de 343 MB) |
| SHA-256 | `D64D1E44FE9B99686C1D730AAD8684EEACD35AC671F4B1C5797B23C2B89F3CBC` |
| Encoding | `utf-8-sig` |
| Separador | `;` |
| Nomes de coluna entre aspas | sim |
| Linhas de dado | 1.099.729 (sem o aviso e sem o cabeçalho) |
| Caminho no Databricks | `/Volumes/workspace/raw/anac_files/Dados_Estatisticos.csv` |

Se for baixar de novo, usa o link da tabela e confere o SHA-256. Se o código mudar, a ANAC republicou o arquivo. Eles atualizam de tempos em tempos.

## Como o arquivo vem organizado

Linha 1: recado da ANAC. Não é coluna.
Linha 2: os 38 nomes.
Linha 3 em diante: os dados.

Se a leitura não pula a linha 1, o resto nasce com o nome errado. No Databricks o que funcionou foi `header=true`, `sep=;`, `encoding=UTF-8` e pular 1 linha.

## As 38 colunas, do jeito que vieram

Não é `EMPRESA (SIGLA)`. Os nomes oficiais são estes, sem acento:

`EMPRESA_SIGLA`; `EMPRESA_NOME`; `EMPRESA_NACIONALIDADE`; `ANO`; `MES`; `AEROPORTO_DE_ORIGEM_SIGLA`; `AEROPORTO_DE_ORIGEM_NOME`; `AEROPORTO_DE_ORIGEM_UF`; `AEROPORTO_DE_ORIGEM_REGIAO`; `AEROPORTO_DE_ORIGEM_PAIS`; `AEROPORTO_DE_ORIGEM_CONTINENTE`; `AEROPORTO_DE_DESTINO_SIGLA`; `AEROPORTO_DE_DESTINO_NOME`; `AEROPORTO_DE_DESTINO_UF`; `AEROPORTO_DE_DESTINO_REGIAO`; `AEROPORTO_DE_DESTINO_PAIS`; `AEROPORTO_DE_DESTINO_CONTINENTE`; `NATUREZA`; `GRUPO_DE_VOO`; `PASSAGEIROS_PAGOS`; `PASSAGEIROS_GRATIS`; `CARGA_PAGA_KG`; `CARGA_GRATIS_KG`; `CORREIO_KG`; `ASK`; `RPK`; `ATK`; `RTK`; `COMBUSTIVEL_LITROS`; `DISTANCIA_VOADA_KM`; `DECOLAGENS`; `CARGA_PAGA_KM`; `CARGA_GRATIS_KM`; `CORREIO_KM`; `ASSENTOS`; `PAYLOAD`; `HORAS_VOADAS`; `BAGAGEM_KG`

`ASSENTOS` está no arquivo. Não precisei inventar oferta.

O que cada uma significa está no `data_dictionary.md`.

## Anos que o CSV cobre

O arquivo vai de 2000 a 2026. 2026 veio incompleto, então deixei de fora. O projeto usa 2020 a 2025, anos inteiros.

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

2020 a 2025 somam 208.946 linhas. Esse é o recorte da tabela `workspace.raw.anac_dados_estatisticos`. No disco o CSV continua inteiro.

Não baixei um arquivo por ano. Veio um CSV só.

## O que bateu no Databricks

A leitura no workspace fechou com este inventário: 38 colunas, 1.099.729 linhas no arquivo todo, coluna de ano chamada `ANO`, soma 2020 a 2025 igual a 208.946.

Os valores reais de natureza e grupo de voo estão no `data_dictionary.md`, seção 6.
