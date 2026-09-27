# Dicionário de dados

Aqui eu anotei como cada coluna chega no CSV da ANAC, como eu chamei no projeto e o que ela significa na prática.

Fonte: ANAC, Dados Estatísticos do Transporte Aéreo.
Arquivo: `Dados_Estatisticos.csv` (não vai para o GitHub).
Separador: ponto e vírgula (`;`).
Encoding: `utf-8-sig`.

Uma linha do arquivo é uma empresa, num mês, num trecho origem destino, com um tipo de voo.

Dois cuidados na leitura. A primeira linha é um aviso (`Atualizado em: 2026-09-21`), não é nome de coluna. Os nomes estão na segunda linha.

Uso o dado aberto da ANAC. Não é número oficial da Agência. O texto deles sobre cada variável está em:
https://www.gov.br/anac/pt-br/assuntos/dados-e-estatisticas/descricao-de-variaveis

A lista abaixo é o cabeçalho real do arquivo que eu baixei. Não inventei coluna.

---

## 1. Colunas do arquivo → nome no projeto

| # | Nome no CSV | Nome no projeto | Tipo | Uso | O que é |
|---:|---|---|---|---|---|
| 1 | `EMPRESA_SIGLA` | `empresa_sigla` | texto | sim | Código da empresa |
| 2 | `EMPRESA_NOME` | `empresa_nome` | texto | sim | Nome da empresa |
| 3 | `EMPRESA_NACIONALIDADE` | `empresa_nacionalidade` | texto | sim | País da empresa. Combustível só existe se for brasileira |
| 4 | `ANO` | `ano` | número | sim | Ano |
| 5 | `MES` | `mes` | número | sim | Mês (1 a 12) |
| 6 | `AEROPORTO_DE_ORIGEM_SIGLA` | `aero_origem_sigla` | texto | sim | Código do aeroporto de saída |
| 7 | `AEROPORTO_DE_ORIGEM_NOME` | `aero_origem_nome` | texto | sim | Nome do aeroporto de saída |
| 8 | `AEROPORTO_DE_ORIGEM_UF` | `aero_origem_uf` | texto | sim | Estado de saída (vazio se for fora do Brasil) |
| 9 | `AEROPORTO_DE_ORIGEM_REGIAO` | `aero_origem_regiao` | texto | sim | Região de saída |
| 10 | `AEROPORTO_DE_ORIGEM_PAIS` | `aero_origem_pais` | texto | sim | País de saída |
| 11 | `AEROPORTO_DE_ORIGEM_CONTINENTE` | `aero_origem_continente` | texto | sim | Continente de saída |
| 12 | `AEROPORTO_DE_DESTINO_SIGLA` | `aero_destino_sigla` | texto | sim | Código do aeroporto de chegada |
| 13 | `AEROPORTO_DE_DESTINO_NOME` | `aero_destino_nome` | texto | sim | Nome do aeroporto de chegada |
| 14 | `AEROPORTO_DE_DESTINO_UF` | `aero_destino_uf` | texto | sim | Estado de chegada |
| 15 | `AEROPORTO_DE_DESTINO_REGIAO` | `aero_destino_regiao` | texto | sim | Região de chegada |
| 16 | `AEROPORTO_DE_DESTINO_PAIS` | `aero_destino_pais` | texto | sim | País de chegada |
| 17 | `AEROPORTO_DE_DESTINO_CONTINENTE` | `aero_destino_continente` | texto | sim | Continente de chegada |
| 18 | `NATUREZA` | `natureza` | texto | filtro | Doméstica ou internacional |
| 19 | `GRUPO_DE_VOO` | `grupo_voo` | texto | filtro | Regular, não regular ou improdutivo |
| 20 | `PASSAGEIROS_PAGOS` | `passageiros_pagos` | número | sim | Pessoas que pagaram (promo e milhas entram aqui) |
| 21 | `PASSAGEIROS_GRATIS` | `passageiros_gratis` | número | sim | Pessoas no assento sem pagar (cortesia, funcionário) |
| 22 | `CARGA_PAGA_KG` | `carga_paga_kg` | número | não | Carga paga (kg). Fora do painel |
| 23 | `CARGA_GRATIS_KG` | `carga_gratis_kg` | número | não | Carga grátis (kg) |
| 24 | `CORREIO_KG` | `correio_kg` | número | não | Correio (kg) |
| 25 | `ASK` | `ask` | número | sim | Assentos oferecidos × km do trecho |
| 26 | `RPK` | `rpk` | número | sim | Só passageiros **pagos** × km. Não conta quem voou de graça |
| 27 | `ATK` | `atk` | número | não | Oferta de peso × km |
| 28 | `RTK` | `rtk` | número | não | Peso pago × km |
| 29 | `COMBUSTIVEL_LITROS` | `combustivel_litros` | número | só empresa BR | Litros no trecho. Empresa estrangeira vem vazio, e isso é esperado |
| 30 | `DISTANCIA_VOADA_KM` | `distancia_km` | número | apoio | Distância do trecho, em km |
| 31 | `DECOLAGENS` | `decolagens` | número | apoio | Quantas decolagens no mês |
| 32 | `CARGA_PAGA_KM` | `carga_paga_km` | número | não | Carga paga × km |
| 33 | `CARGA_GRATIS_KM` | `carga_gratis_km` | número | não | Carga grátis × km |
| 34 | `CORREIO_KM` | `correio_km` | número | não | Correio × km |
| 35 | `ASSENTOS` | `assentos` | número | **principal** | Assentos oferecidos no trecho. Existe no arquivo |
| 36 | `PAYLOAD` | `payload_kg` | número | não | Peso que o avião pode levar |
| 37 | `HORAS_VOADAS` | `horas_voadas` | número | não | Horas de voo |
| 38 | `BAGAGEM_KG` | `bagagem_kg` | número | não | Bagagem (kg). Em geral só empresa brasileira |

“Uso = não” = a coluna fica guardada, mas não entra no painel.

---

## 2. Contas que eu criei (não vêm no CSV)

Calculei depois da limpeza. Nada disso existe no arquivo cru.

| Nome | Como se calcula | Em que unidade | Para que serve |
|---|---|---|---|
| `ano_mes` | ano × 100 + mês | 202305 = maio de 2023 | Juntar ano e mês |
| `passageiros_totais` | pagos + grátis | pessoas | Quem ocupou assento |
| `assentos_fantasma` | assentos − pessoas, sem ficar negativo | assentos | Assentos que decolaram vazios |
| `taxa_ociosidade` | assentos vazios ÷ assentos | 0 a 1 | Quanto da oferta foi vazia |
| `load_factor` | RPK ÷ ASK, no máximo 1,05 | 0 a 1 | Ocupação oficial (só quem pagou) |
| `ask_ocioso` | ASK − RPK, sem ficar negativo | assento × km | Oferta de km que não virou passageiro pago |
| `litros_por_pax` | combustível ÷ pessoas | litros por pessoa | Só empresa brasileira com combustível preenchido. Não vai ao painel principal |
| `eh_empresa_br` | nacionalidade contém “BRASIL” | sim / não | Quem informa combustível |
| `eh_pandemia` | ano = 2020 ou 2021 | sim / não | Esses anos não são “mês típico” |
| `rota_id` | origem + “-” + destino | texto | Ex.: `SBSP-SBRJ`. Ida e volta são rotas diferentes |
| `status_rota` | regras da seção 5 | texto | Situação da linha naquele mês |

---

## 3. O que identifica uma linha da tabela principal

Empresa + ano + mês + aeroporto de saída + aeroporto de chegada + natureza + grupo de voo.

Não pode repetir. Se repetir, a tabela está errada.

---

## 4. O que entra no painel (filtro padrão)

| Campo | Fica no painel se | Valor que usamos |
|---|---|---|
| Ano | 2020 a 2025 | já cortado na tabela raw |
| Natureza | só doméstica | `DOMESTICA` (no arquivo vem `DOMÉSTICA`) |
| Grupo de voo | só regular | `REGULAR` |
| Assentos | maior que zero | tira voo só de carga das contas de assento vazio |

O resto continua nas tabelas cruas, para conferência.

---

## 5. Situação da rota no mês (`status_rota`)

Vale a **primeira** regra que encaixar:

| Nome | Quando |
|---|---|
| `FORA_ESCOPO` | menos de 5.000 assentos no mês |
| `SUBOFERTA` | ocupação oficial ≥ 92% |
| `ASSENTOS_FANTASMA` | 40% ou mais vazios **e** pelo menos 10.000 assentos |
| `DESPERDICIO_MODERADO` | 28% ou mais vazios |
| `EFICIENTE` | o que sobrar |

Muito assento vazio, sozinho, não prova que a empresa geriu mal.
Pode ser avião grande demais, ligação de malha, hub, carga ou pandemia.

---

## 6. Valores reais que apareceram no arquivo (recorte 2020–2025)

| Campo | O que veio no arquivo | Como usamos |
|---|---|---|
| Natureza | `DOMÉSTICA` (138.884) e `INTERNACIONAL` (70.062) | filtro = `DOMESTICA` |
| Grupo de voo | `REGULAR` (129.382), `NÃO REGULAR` (55.299), `IMPRODUTIVO` (24.265) | filtro = `REGULAR` |
| Empresa brasileira | nacionalidade com a palavra BRASIL | `eh_empresa_br` = sim |

---

## 7. O que o painel não mostra

Carga, correio, ATK, RTK, payload, horas voadas e bagagem.
Ficam na tabela limpa, sem uso inventado.

---

## 8. Pegadinhas

Tem duas ocupações no mesmo projeto. “Assentos vazios” conta todo mundo que ocupou a poltrona. O load factor da ANAC conta só quem pagou.

Combustível vazio em empresa estrangeira é esperado. Load factor acima de 100% aparece por arredondamento; eu limito em 105% e conto se passou.

2020 e 2021 são pandemia. Não servem de mês típico.

Este arquivo não tem preço, não tem o motivo do vazio e não tem cada voo. Só o mês.

Na lista das rotas mais vazias em %, o load factor às vezes não fecha com a conta de assentos. Nessa conversa eu fico com o ranking de volume.

---

## 9. Catálogo das tabelas do modelo

O Unity Catalog no Databricks tem os mesmos objetos. Abaixo, para cada tabela, o que ela é, o que uma linha representa, de onde veio e os campos.

O dado anda assim: CSV da ANAC, Volume, `raw`, `staging`, `intermediate`, depois `marts` (fato, dimensões, marts) e `analytics`.

### 9.1 `workspace.raw.anac_dados_estatisticos`

É o bruto de 2020 a 2025, do jeito que veio no CSV. Só cortei o ano.

Uma linha: empresa + mês + trecho origem destino + natureza + grupo de voo.

Veio do Volume `anac_files/Dados_Estatisticos.csv`. Sem rename e sem filtro de doméstico ou regular. Umas 208.946 linhas, 38 colunas.

Os campos são os 38 nomes da seção 1. Na leitura todos entram como texto. `NATUREZA` vem `DOMÉSTICA` ou `INTERNACIONAL`. `GRUPO_DE_VOO` vem `REGULAR`, `NÃO REGULAR` ou `IMPRODUTIVO`. `ANO` de 2020 a 2025 neste recorte. `MES` de 1 a 12. Assentos e passageiros, quando preenchidos, são zero ou mais. Também podem vir vazios.

### 9.2 `workspace.staging.stg_anac_voos`

Mesmo conteúdo do `raw`, só que com nome interno, tipo certo e texto limpo. A linha ainda pode ser internacional ou não regular.

Saí de um `SELECT` no `raw`: TRIM, UPPER, `TRY_CAST`, `natureza_norm` e `grupo_voo_norm` sem acento, `ano_mes` = ano vezes 100 mais o mês.

Campos que mais importam:

| Campo | Tipo | Domínio / regra | Origem |
|---|---|---|---|
| `empresa_sigla` | texto | código da empresa, sem espaço nas pontas | `EMPRESA_SIGLA` |
| `ano`, `mes` | inteiro | ano 2020–2025; mês 1–12 | `ANO`, `MES` |
| `ano_mes` | inteiro | 202001 a 202512 | calculado |
| `natureza` | texto | como no arquivo (`DOMÉSTICA`, …) | `NATUREZA` |
| `natureza_norm` | texto | `DOMESTICA` ou `INTERNACIONAL` | `NATUREZA` sem acento |
| `grupo_voo_norm` | texto | `REGULAR`, `NAO REGULAR`, `IMPRODUTIVO` | `GRUPO_DE_VOO` sem acento |
| `assentos` | inteiro | ≥ 0 ou nulo | `ASSENTOS` |
| `passageiros_pagos`, `passageiros_gratis` | inteiro | ≥ 0 ou nulo | CSV |
| `ask`, `rpk`, `combustivel_litros` | decimal | ≥ 0 ou nulo | CSV |
| carga, correio, ATK, RTK, payload, horas, bagagem | decimal | guardados, fora do painel | CSV |

### 9.3 `workspace.intermediate.int_voos_mensais`

Aqui entra o filtro do projeto e as contas. Uma linha é empresa-trecho-mês doméstico regular com `assentos > 0`.

Filtro no `staging`: `natureza_norm = 'DOMESTICA'`, `grupo_voo_norm = 'REGULAR'` e `assentos > 0`.

Os campos novos estão na seção 2. `status_rota` é um destes, na primeira regra que encaixar (seção 5): `FORA_ESCOPO`, `SUBOFERTA`, `ASSENTOS_FANTASMA`, `DESPERDICIO_MODERADO`, `EFICIENTE`. `taxa_ociosidade` vai de 0 a 1. `load_factor` vai de 0 a 1,05.

### 9.4 Dimensões (`workspace.marts`)

Todas saem de valores distintos do intermediário. Sem fonte de fora.

**`dim_tempo`**. Uma linha é um `ano_mes`.

| Campo | Tipo | Domínio | Origem |
|---|---|---|---|
| `ano` | inteiro | 2020–2025 | intermediário |
| `mes` | inteiro | 1–12 | intermediário |
| `ano_mes` | inteiro | chave | intermediário |
| `trimestre` | inteiro | 1–4 | calculado do mês |
| `semestre` | inteiro | 1 ou 2 | calculado do mês |
| `eh_pandemia` | verdadeiro/falso | verdadeiro se ano 2020 ou 2021 | calculado |

**`dim_empresa`**. Uma linha é uma `empresa_sigla`. Campos: `empresa_sigla`, `empresa_nome`, `empresa_nacionalidade` (textos) e `eh_empresa_br` (verdadeiro ou falso). Saí de um `MAX` por sigla no intermediário.

**`dim_aeroporto`**. Uma linha é um `aero_sigla`. Campos: `aero_sigla`, `aero_nome`, `aero_uf`, `aero_regiao`, `aero_pais`, `aero_continente`. `aero_uf` pode vir vazio se o aeroporto for fora do Brasil. Juntei origens e destinos (`UNION ALL`) e fiquei com um registro por sigla.

**`dim_rota`**. Uma linha é um `rota_id` (`SBSP-SBRJ`). Ida e volta são rotas diferentes. Campos: `rota_id`, siglas e nomes de origem e destino, UFs, regiões, `eh_domestica` (sempre verdadeiro neste recorte).

**`dim_natureza`**. `natureza` e `natureza_norm`. Neste recorte só doméstica.

**`dim_grupo_voo`**. `grupo_voo` e `grupo_voo_norm`. Neste recorte só regular.

### 9.5 `workspace.marts.fct_voos_mensais`

É o fato. Daqui saem os marts, os testes de qualidade e o painel.

A chave é a mesma do intermediário: empresa + mês + trecho + natureza + grupo. As colunas vieram do `int_voos_mensais`, sem JOIN extra.

| Campo | Tipo | Domínio | Origem |
|---|---|---|---|
| `empresa_sigla` | texto | chave | intermediário |
| `empresa_nome`, `empresa_nacionalidade` | texto | texto livre / país | intermediário |
| `eh_empresa_br` | verdadeiro/falso | combustível só faz sentido se verdadeiro | nacionalidade contém BRASIL |
| `ano`, `mes`, `ano_mes` | inteiro | 2020–2025; 1–12 | intermediário |
| `aero_origem_*`, `aero_destino_*` | texto | sigla, nome, UF, região | intermediário |
| `rota_id` | texto | `ORIGEM-DESTINO` | concatenação |
| `natureza`, `natureza_norm`, `grupo_voo`, `grupo_voo_norm` | texto | ver 9.2 | intermediário |
| `passageiros_pagos`, `passageiros_gratis`, `passageiros_totais` | inteiro | ≥ 0 | CSV + soma |
| `assentos`, `assentos_fantasma` | inteiro | ≥ 0; fantasma ≤ assentos | CSV + conta |
| `taxa_ociosidade` | decimal | 0 a 1 | conta |
| `ask`, `rpk`, `ask_ocioso` | decimal | ≥ 0 ou nulo | CSV + conta |
| `load_factor` | decimal | 0 a 1,05 | RPK/ASK limitado |
| `combustivel_litros`, `litros_por_pax`, `eficiencia_combustivel` | decimal | nulo se estrangeira ou sem pax | CSV + conta |
| `distancia_km`, `decolagens` | decimal / inteiro | ≥ 0 ou nulo | CSV |
| `status_rota` | texto | 5 selos da seção 5 | regra |

### 9.6 Marts de consumo

**`mart_kpi_rota_mensal`**. Uma linha é uma rota + um mês, com as empresas somadas. `GROUP BY` no fato. Recalculo taxa, load factor e `status_rota` depois da soma. Campos: `rota_id`, aeroportos, ano, mês, totais de pax, assentos, fantasma, ASK, RPK, decolagens, combustível, taxa, load factor, status.

**`mart_ociosidade_empresa_mensal`**. Uma linha é uma empresa + um mês. Também sai de um `GROUP BY` no fato.

**`mart_ociosidade_aeroporto_mensal`**. Uma linha é um aeroporto de origem + um mês. Mesmo tipo de agregação.

**`mart_ranking_assentos_fantasma`**. Uma linha é uma rota de 2022 a 2025, só se `assentos >= 10000`. Tem `rank_volume` e `rank_taxa`.

**`analytics.mart_status_rota`**. Cópia mais curta do KPI de rota (rota-mês + selo).

**`analytics.rota_clusters`**. Uma linha é uma rota do recorte de treino (2022 a 2025, pelo menos 12 meses e 50 mil assentos).

| Campo | Tipo | Domínio | Origem |
|---|---|---|---|
| `rota_id` | texto | igual à dim | KPI de rota |
| `n_meses` | inteiro | ≥ 12 | contagem |
| `assentos`, `assentos_fantasma` | número | ≥ 0 | soma |
| `ociosidade_media`, `ociosidade_dp`, `lf_medio` | decimal | 0–1 / ≥ 0 | média e desvio |
| `cluster_id` | inteiro | 0 a 4 | K-means |
| `cluster_nome` | texto | `INSTAVEL`, `ALTO_VOLUME_EFICIENTE`, `OCIOSO_CRONICO`, `LOTADO`, `OCIOSO_MODERADO` | mapa do notebook 07 |

Views `vw_pbi_*` em `analytics` não são tabelas novas: só leem os marts para o dashboard.