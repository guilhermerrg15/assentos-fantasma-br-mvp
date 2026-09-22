# Dicionário de dados — Assentos Fantasma BR

Explica o nome de cada coluna: como vem no arquivo da ANAC,
como ficou no projeto e o que significa.

**Fonte:** ANAC — Dados Estatísticos do Transporte Aéreo  
**Arquivo:** `Dados_Estatisticos.csv` (não vai para o GitHub)  
**Separador:** ponto e vírgula (`;`)  
**Letras do arquivo:** `utf-8-sig`  
**Uma linha do arquivo é:** uma empresa, em um mês, em um trecho
origem → destino, com um tipo de voo.

**Cuidado ao ler o CSV:**
- A primeira linha é um aviso (`Atualizado em: 2026-09-21`). Não é nome de coluna.
- Os nomes das colunas estão na segunda linha.

Este trabalho usa o dado aberto da ANAC e **não** é um número oficial da Agência.  
Textos oficiais das variáveis:  
https://www.gov.br/anac/pt-br/assuntos/dados-e-estatisticas/descricao-de-variaveis

Nenhuma coluna da lista abaixo foi inventada. É o cabeçalho real
do arquivo baixado em 21/09/2026.

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
| 29 | `COMBUSTIVEL_LITROS` | `combustivel_litros` | número | só empresa BR | Litros no trecho. Empresa estrangeira vem vazio — isso é normal |
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

## 2. Contas que o projeto cria (não vêm no CSV)

Feitas depois da limpeza, nunca no arquivo cru.

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

Muito assento vazio **não** quer dizer, sozinho, que a empresa geriu mal
(avião grande demais, ligação de serviço, hub, carga, pandemia).

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

## 8. Pegadinhas (leia antes de interpretar um número)

1. **Duas ocupações.** “Assentos vazios” conta todo mundo no assento.
   O load factor da ANAC conta só quem pagou.
2. **Combustível vazio** em empresa estrangeira é normal.
3. **Load factor acima de 100%** pode aparecer (arredondamento).
   Limitamos em 105% e contamos se passou.
4. **2020 e 2021** são pandemia. Não use como mês típico.
5. Não existe preço, motivo do vazio nem dado de cada voo — só o mês.
6. Na lista das rotas “mais vazias em %”, o load factor às vezes
   não combina com a conta de assentos. Nessa conversa, use o ranking de **volume**.