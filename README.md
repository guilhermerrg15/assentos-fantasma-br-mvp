# Assentos Fantasma BR

| Campo | Valor |
|---|---|
| Aluno | Guilherme Ricardo Rezende Gomes |
| Matrícula | 405026000876 |
| Data | Setembro/2026 |
| Disciplina | Sprint Machine Learning & Analytics, MVP |
| Trabalho | Construção de um pipeline de dados na nuvem |
| Dataset | ANAC, Dados Estatísticos do Transporte Aéreo (CSV público) |
| Tipo de problema | Engenharia de dados e análise de ociosidade de assentos na malha doméstica regular |
| Repositório | https://github.com/guilhermerrg15/assentos-fantasma-br-mvp |

Fiz este projeto no Databricks Free Edition. A ideia é simples: os relatórios de aviação no Brasil quase sempre falam de quantas pessoas voaram, e quase nunca de quantos assentos decolaram vazios. Eu quis olhar esse segundo número na malha doméstica regular, de 2020 a 2025, com o CSV público da ANAC.

O arquivo original é grande demais para o GitHub, então ele não está aqui. O que está no repositório é o código, o dicionário e os prints.

## Contexto de Negócios e Perguntas (Etapa 2 e 4.1)

### Problema

Se você só soma passageiro, some a oferta que foi embora vazia. Quem olha malha, aeroporto ou política pública acaba vendo só metade da história.

No começo eu também pensei em tratar assento vazio como sinal de má gestão. Depois, mexendo no dado, ficou claro que não é bem assim. As vezes o avião é grande demais para o trecho, as vezes a rota existe mais por ligação de malha do que por demanda, às vezes é efeito de 2020 e 2021. O vazio existe. O motivo, este CSV não conta.

### Perguntas de negócio

Estas foram as perguntas que eu anotei antes de modelar. Deixei as oito, inclusive as que no fim responderam pouco.

1. Quantos assentos decolam vazios na malha doméstica regular (2020 a 2025)?
2. Esse vazio se concentra em poucas rotas?
3. Quais rotas e empresas têm mais volume de assentos vazios, e quais são as mais vazias em porcentagem?
4. O vazio muda conforme o mês? 2020 e 2021 se comportam igual aos anos seguintes?
5. O vazio se concentra em alguns estados de origem?
6. Dá para achar, no mesmo recorte, rota lotada e rota muito vazia?
7. O combustível por passageiro piora onde há mais assento vazio?
8. Dá para agrupar rotas em tipos (lotada, eficiente, ociosa, instável)?

A 7 só se segura na faixa bem extrema. A 8 até gera cinco grupos, mas eles se misturam. Comento isso na análise e de novo na autoavaliação.

### De onde saiu o dado bruto

Peguei um CSV só, o de Dados Estatísticos do Transporte Aéreo da ANAC. Não passei por Kaggle nem por planilha já recortada. O arquivo inteiro vai de 2000 a 2026. Eu fiquei com 2020 a 2025, que são os anos cheios.

Uma linha não é um voo. É o total daquela empresa, naquele mês, naquele trecho origem destino, com um tipo de natureza e de grupo de voo.

São 38 colunas. As que de fato empurram o problema: `ASSENTOS`, `PASSAGEIROS_PAGOS`, `PASSAGEIROS_GRATIS`, `ASK`, `RPK`, empresa, ano, mês, os aeroportos, `NATUREZA`, `GRUPO_DE_VOO` e `COMBUSTIVEL_LITROS`.

A primeira linha do arquivo é um recado (`Atualizado em: ...`). Cabeçalho de verdade só na segunda. E `ASSENTOS` está lá. Não precisei inventar oferta.

O restante das colunas, com tipo e significado, está em `[docs/data_dictionary.md](docs/data_dictionary.md)`. Link, tamanho e hash ficam em `[docs/data_sources.md](docs/data_sources.md)`.

### Licença

É dado aberto da ANAC. Pode usar, desde que cite a fonte. Eu cito assim: Fonte: ANAC, Dados Estatísticos do Transporte Aéreo. Elaboração própria.

A própria Agência avisa que totais feitos em cima do arquivo bruto podem não bater com o relatório oficial. Este trabalho não é estatística oficial.

## Carga dos Dados (Etapa 4.2)

Na conta gratuita o notebook não alcança o site da ANAC. Então baixei o CSV no computador e mandei para o Volume. São uns 343 MB.

1. Download do [Dados_Estatisticos.csv](https://sistemas.anac.gov.br/dadosabertos/Voos%20e%20opera%C3%A7%C3%B5es%20a%C3%A9reas/Dados%20Estat%C3%ADsticos%20do%20Transporte%20A%C3%A9reo/Dados_Estatisticos.csv). O SHA-256 que eu conferi está em `docs/data_sources.md`.
2. Upload para `/Volumes/workspace/raw/anac_files/Dados_Estatisticos.csv`.
3. O `[notebooks/01_ingestao_raw.py](notebooks/01_ingestao_raw.py)` lê o arquivo (pula a linha 1, separador `;`, UTF-8), corta 2020 a 2025 (208.946 linhas) e grava `workspace.raw.anac_dados_estatisticos`.

Três decisões dessa leitura, porque cada uma me quebrou a cabeça no começo:

Pulei a linha 1. Sem isso, o Spark trata o recado da ANAC como nome de coluna e o resto desanda.

Deixei tudo como texto na entrada (`inferSchema=false`). O CSV chega sujo. Tipo certo eu acerto na limpeza, não na primeira leitura.

Cortei o ano já no `raw`. O arquivo tem cerca de 1,1 milhão de linhas. Eu só ia usar 2020 a 2025 de qualquer jeito.

O Volume no Catalog:

![CSV no Volume](docs/catalog_volume.png)

## Modelagem e Catálogo de Dados (Etapa 4.3)

### Como eu organizei as tabelas

Fui de esquema estrela porque o que eu queria perguntar era sempre alguma variação de “o que aconteceu naquele mês, para aquela empresa, naquele trecho”.

O fato (`fct_voos_mensais`) guarda o acontecido. As dimensões guardam o “quando”, o “quem” e o “de onde para onde”.

Uma linha do fato é empresa + ano + mês + origem + destino + natureza + grupo de voo. Se essa chave repetir, a tabela está errada. Eu testo isso no notebook de qualidade.

### Camadas

No curso isso aparece como medalhão. Eu não renomeei schema para bronze/silver/gold, mas a ordem é essa: chega cru, eu limpo, depois deixo pronto para o painel.


| Camada               | Schema                   | O que tem                                         |
| -------------------- | ------------------------ | ------------------------------------------------- |
| Como veio            | `workspace.raw`          | `anac_dados_estatisticos` (CSV 2020 a 2025)       |
| Limpo                | `workspace.staging`      | `stg_anac_voos` (nome, tipo, acento)              |
| Com as contas        | `workspace.intermediate` | `int_voos_mensais` (doméstico regular + métricas) |
| Pronto para o painel | `workspace.marts`        | fato, 6 dimensões e os marts                      |
| Análise              | `workspace.analytics`    | status, cluster e as views do dashboard           |


Campo a campo, tipo e de onde veio cada coluna: `[docs/data_dictionary.md](docs/data_dictionary.md)`, seções 1, 2 e 9.

Resumo do que cada tabela representa:


| Tabela                                   | Uma linha é                                     | De onde veio               |
| ---------------------------------------- | ----------------------------------------------- | -------------------------- |
| `raw.anac_dados_estatisticos`            | empresa-trecho-mês como no CSV                  | Volume, anos 2020 a 2025   |
| `staging.stg_anac_voos`                  | a mesma linha, limpa                            | `raw`                      |
| `intermediate.int_voos_mensais`          | só doméstico regular com assento                | `staging` + as contas      |
| `marts.dim_tempo`                        | um ano-mês                                      | distintos do intermediário |
| `marts.dim_empresa`                      | uma empresa                                     | distintos do intermediário |
| `marts.dim_aeroporto`                    | um aeroporto                                    | origem e destino juntos    |
| `marts.dim_rota`                         | um par origem-destino                           | distintos do intermediário |
| `marts.dim_natureza`                     | um tipo de natureza                             | distintos do intermediário |
| `marts.dim_grupo_voo`                    | um grupo de voo                                 | distintos do intermediário |
| `marts.fct_voos_mensais`                 | o fato do mês                                   | intermediário              |
| `marts.mart_kpi_rota_mensal`             | rota + mês (empresas somadas)                   | fato                       |
| `marts.mart_ociosidade_empresa_mensal`   | empresa + mês                                   | fato                       |
| `marts.mart_ociosidade_aeroporto_mensal` | aeroporto de origem + mês                       | fato                       |
| `marts.mart_ranking_assentos_fantasma`   | uma rota (2022 a 2025, piso de 10 mil assentos) | fato                       |
| `analytics.mart_status_rota`             | rota-mês com o selo                             | KPI de rota                |
| `analytics.rota_clusters`                | uma rota com o tipo                             | notebook `07`              |


Caminho do dado: CSV da ANAC, Volume, `raw`, `staging`, `intermediate`, fato e dimensões, depois marts e analytics.

Prints do fato no Unity Catalog (a lista de colunas não cabe numa tela só):

![Catálogo da tabela fato, página 1](docs/catalog_fato.png)
![Catálogo da tabela fato, página 2](docs/catalog_fato_2.png)

## Pipeline de Dados (Etapa 4.4)

Separei em vários notebooks. Um arquivo só ia ficar impossível de achar as coisas. O Job `assentos-fantasma-br-mvp` roda `02`, `03` e `07`, nessa ordem, depois que o `01` já gravou o `raw`.


| Ordem   | Arquivo                                                                                                                      | Função                                           |
| ------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| 1       | `[notebooks/01_ingestao_raw.py](notebooks/01_ingestao_raw.py)`                                                               | lê o Volume e grava o `raw`                      |
| 2       | `[notebooks/02_modelo_dimensional.py](notebooks/02_modelo_dimensional.py)`                                                   | staging, intermediário, dims, fato, marts, views |
| 3       | `[notebooks/03_qualidade.py](notebooks/03_qualidade.py)`                                                                     | testes. Não cria tabela de negócio               |
| 4 a 6   | `[04](notebooks/04_eda_desperdicio.py)`, `[05](notebooks/05_sazonalidade_geografia.py)`, `[06](notebooks/06_combustivel.py)` | gráficos e números da análise                    |
| 7       | `[notebooks/07_clusters_rotas.py](notebooks/07_clusters_rotas.py)`                                                           | grava `rota_clusters`                            |
| depois  | `[notebooks/08_catalogo_unity.py](notebooks/08_catalogo_unity.py)`                                                           | texto das tabelas no Catalog                     |
| à parte | `[sql/](sql/)`                                                                                                               | 12 consultas, de `01` a `12`                     |


O que eu transformei, e por quê:

A linha 1 do CSV é aviso. Se eu não pulo, as 38 colunas nascem com o nome errado.

`NATUREZA` vem `DOMÉSTICA`, com acento. Eu gero `natureza_norm` sem acento para o filtro não quebrar no dia em que a ANAC mudar um caractere. O mesmo em grupo de voo.

Números chegam como texto. `TRY_CAST` vira inteiro ou decimal. Sem isso eu não somo assento com passageiro.

Filtro: doméstico, regular, assentos maior que zero. Internacional, não regular, improdutivo e linha só de carga saem da conta de assento vazio. Continuam no `raw` e no `staging` se eu precisar conferir.

O CSV não tem “assento fantasma”. Eu calculo `passageiros_totais`, `assentos_fantasma`, `taxa_ociosidade`, `load_factor`, `ask_ocioso` e `status_rota` no intermediário. O painel lê número já fechado.

Dimensões saem do intermediário. Empresa, mês, aeroporto e rota viram tabela de apoio, e eu paro de reler o CSV para cada gráfico.

Os marts somam empresa na mesma rota e mês, ou fecham o ranking 2022 a 2025 com piso de 10 mil assentos. Sem isso o dashboard recalcularia o grão a cada visual.

O notebook `07` pega rota com pelo menos 12 meses e 50 mil assentos (2022 a 2025) e tenta achar 5 tipos. A página 5 do painel usa isso.

Tabelas gravadas no Catalog:

![Schemas analytics, intermediate e marts](docs/catalog_tabelas.png)
![Schemas raw e staging](docs/catalog_tabelas_2.png)

## Qualidade de Dados (Etapa 4.5)

Isso está no `[03_qualidade.py](notebooks/03_qualidade.py)` e na query `[sql/12_load_factor_anomalo.sql](sql/12_load_factor_anomalo.sql)`. Passei pelos cinco eixos que o enunciado pede.

Completude. Combustível vazio em empresa estrangeira é regra da ANAC, não buraco meu. Não completei com zero. Achei 2 linhas com `ASK` nulo e assento maior que zero. No volume do fato isso é ruído; contei e deixei. Passageiro nulo eu trato como zero na ocupação do assento (`COALESCE`), senão o assento oferecido some da conta.

Consistência. Natureza no arquivo: `DOMÉSTICA` e `INTERNACIONAL`. Eu trabalho com `DOMESTICA` sem acento. Grupo de voo: `REGULAR`, `NÃO REGULAR`, `IMPRODUTIVO`. O painel fica só no regular. Mês de 1 a 12 e ano de 2020 a 2025, conferidos no `raw` e no fato.

Unicidade. Zero duplicata na chave do fato. Se aparecesse, eu parava.

Acurácia. Assento ou passageiro negativo: zero linhas. Taxa de ociosidade fora de 0 a 1: zero linhas. Load factor (RPK/ASK) às vezes passa de 100% por arredondamento da ANAC. Eu corto em 105% e a query 12 conta quem passou.

Extremos. O selo `ASSENTOS_FANTASMA` (40% ou mais vazios e pelo menos 10 mil assentos no mês) é raro. Eu tinha colocado um corte de 8 meses no ano e voltei zero rota. O máximo no dado é 4 meses, em 4 rotas. Ajustei a query 11 para isso, em vez de insistir num vilão que não existe. `litros_por_pax` explode quando quase ninguém embarcou. Por isso essa conta não foi para o KPI da página 1.

Órfão do fato para empresa, tempo e rota: zero.

## Análise de Dados (Etapa 4.5)

Usei SQL no Databricks, uns gráficos em Python e o dashboard Assentos Fantasma BR (5 páginas). Abaixo, cada pergunta do começo.

### Pergunta 1. Quantos assentos decolam vazios (2020 a 2025)?

Cerca de 115,37 milhões de assentos vazios. Taxa de ociosidade 19,7%. Load factor 81,3%. ASK ocioso por volta de 114,82 bilhões.

Vinte por cento vazio, no agregado, não me parece colapso. Folga de 15% a 25% é comum nesse setor. Só uns 17% dos assentos estão em linhas com 28% ou mais de vazio. O que me incomodou foi a cauda, não a média.

Consulta: `[sql/01_kpi_executivo.sql](sql/01_kpi_executivo.sql)`. Notebook: `[04_eda_desperdicio.py](notebooks/04_eda_desperdicio.py)`.

![Página executiva, KPIs e série](docs/p01_pt1.png)
![Página executiva, volume por empresa](docs/p01_pt2.png)

### Pergunta 2. O vazio se concentra em poucas rotas?

Na metade do desperdício, sim. Não é aquele 80/20 de livro.

No ranking 2022 a 2025 (piso de 10 mil assentos, 891 rotas), 90 rotas (cerca de 10%) levam 50% dos assentos vazios. Para chegar em 80% eu preciso de 281 rotas, uns 32%. Tem concentração. Não tem um punhado de culpado.

Notebook `04` e `[sql/03_pareto_rotas.sql](sql/03_pareto_rotas.sql)`.

### Pergunta 3. Volume versus taxa

As duas listas não contam a mesma coisa, e isso me confundiu na primeira vez.

No volume, ganham rotas grandes (São Paulo a Rio, por exemplo). Sobram muitos assentos porque a malha é enorme. A taxa fica perto de 25%.

Na taxa, sobem rotas menores. Nessa lista o load factor da ANAC às vezes não fecha com a conta de assento. Quando eu preciso escolher uma conversa só, fico com o ranking de volume.

Nas empresas o volume acompanha o tamanho da malha (LATAM, Azul, Gol). Mais vazio em número absoluto não prova que a empresa voa pior.

![Top 20 por volume](docs/p02_pt1.png)
![Top 20 por taxa](docs/p02_pt2.png)

### Pergunta 4. O vazio muda com o mês? 2020 e 2021 são iguais?

Muda um pouco. Misturar pandemia com mês “normal” bagunça a leitura.

De 2022 a 2025, maio é o mais vazio (22,6%) e novembro o mais cheio (16,7%). Julho, que é férias, fica perto de 17,5%. Seis pontos entre maio e novembro. Existe sazonalidade, mas a malha inteira continua girando perto de 20%.

2020 e 2021 são outro filme. Em março da pandemia a taxa sobe muito. Eu não usaria esses anos para falar de mês típico.

![Sazonalidade](docs/p04.png)

### Pergunta 5. O vazio se concentra em alguns estados de origem?

Em volume, São Paulo puxa (uns 29 milhões de assentos vazios de 2022 a 2025), depois RJ, DF e MG. É tamanho de malha.

Em taxa a ordem vira. Estados do Norte e do Nordeste com malha mais fina ficam mais vazios em porcentagem. Acre, por exemplo, perto de 38%. Volume alto não é a mesma coisa que voar mais vazio em %.

![Por UF de origem](docs/p03_pt1.png)
![Por região de origem](docs/p03_pt2.png)

### Pergunta 6. Existe rota lotada e rota muito vazia ao mesmo tempo?

Existe. A maior parte dos rotas-mês cai em `EFICIENTE`. Tem `SUBOFERTA` (lotada) e tem `ASSENTOS_FANTASMA` (muito vazia). Esse último é raro e não se segura o ano inteiro: ninguém ficou 8 meses assim. O teto foi 4 meses, em 4 rotas.

![Status da rota](docs/p05_pt1.png)

### Pergunta 7. Combustível por passageiro piora com o vazio?

Só quando a ociosidade passa de 40%. No resto da malha, não. Por isso a pergunta ficou no objetivo e a métrica não foi para o KPI da capa.

Empresas brasileiras, 2022 a 2025, com combustível preenchido:


| Faixa de ociosidade | Litros por passageiro (média) |
| ------------------- | ----------------------------- |
| 0 a 20%             | 37,9                          |
| 20 a 28%            | 35,0                          |
| 28 a 40%            | 36,4                          |
| 40% ou mais         | 208,9                         |


Até 40% o número fica parado perto de 36 litros. Depois explode. O que mais faz sentido para mim é poucos passageiros no denominador, não a empresa queimando querosene à toa. A correlação deu uns 0,20. Fraca. E combustível neste arquivo só existe em empresa brasileira.

Notebook: `[06_combustivel.py](notebooks/06_combustivel.py)`. Query: `[sql/08_combustivel_vs_ociosidade.sql](sql/08_combustivel_vs_ociosidade.sql)`.

### Pergunta 8. Dá para agrupar rotas em tipos?

Dá para tentar. Eu não chamaria de divisão limpa.

Peguei 683 rotas (2022 a 2025, no mínimo 12 meses e 50 mil assentos) e saíram 5 nomes: `LOTADO`, `ALTO_VOLUME_EFICIENTE`, `OCIOSO_MODERADO`, `OCIOSO_CRONICO`, `INSTAVEL`.

O silhouette ficou 0,32. Os pontos se misturam no gráfico, e eu deixei assim. Preferi não forçar quatro rótulos bonitos.

![Tipos de rota](docs/p05_pt2.png)

### O que isso responde no conjunto

O ponto de partida era o relatório que só conta quem voou. O pipeline mostra a oferta que saiu vazia, com número, lugar e mês.

Tem vazio de verdade (cerca de 115 milhões de assentos). A média perto de 20% não é o fim da malha. Poucas rotas grandes carregam metade do volume. As “mais vazias em %” são outra lista. Mês e estado mudam o recorte, mas não a tese: o problema mora na cauda e nas pontes grandes, não num Brasil inteiro voando vazio.

Lotado e muito vazio convivem. Crônico no calendário, o muito vazio quase não aparece. Combustível e cluster eu testei porque estavam no objetivo. Sozinhos, não sustentam decisão. E assento vazio, sozinho, continua sem provar má gestão.

## Autoavaliação

Eu consegui fechar o ciclo na nuvem: pergunta, coleta, dado no Databricks, modelo, ETL, qualidade e resposta no SQL, no Python e no painel.

Das oito perguntas, 1 a 6 têm número e print. A 7 só vale na faixa de 40% para cima. A 8 tem cinco grupos e uma separação fraca (0,32). As duas ficaram no texto de propósito.

O que mais me atrasou: o CSV de 343 MB. A conta Free não baixa da ANAC pelo notebook, então foi download local e upload no Volume. A primeira linha do arquivo não é cabeçalho; se a leitura ignora isso, todas as colunas nascem erradas. O corte de “8 meses fantasma no ano” voltou zero linha, e o dado só tem 4 meses no teto. `litros_por_pax` mente quando quase ninguém embarcou. O cluster não separa como nos exemplos de aula.

Se eu for além deste MVP, eu juntaria preço de passagem (este arquivo não tem), tentaria dado voo a voo se a ANAC publicar, e pensaria duas vezes antes de insistir em k-means. Também deixaria um jeito de atualizar quando eles republicarem o CSV, porque o hash muda.

O que este trabalho não tem, e eu sei: motivo do assento vazio, cada decolagem isolada, preço. Combustível só em empresa brasileira. 2020 e 2021 não servem de mês típico.

## Como repetir

1. Baixe o CSV pelo link de `docs/data_sources.md` e envie para `/Volumes/workspace/raw/anac_files/`.
2. Rode `[notebooks/01_ingestao_raw.py](notebooks/01_ingestao_raw.py)`.
3. Rode o Job `assentos-fantasma-br-mvp` (notebooks `02`, `03` e `07`) ou rode esses três na ordem.
4. Se quiser as descrições no Catalog, rode `[notebooks/08_catalogo_unity.py](notebooks/08_catalogo_unity.py)`.
5. Abra o dashboard Assentos Fantasma BR.

Tudo isso no Databricks Free Edition, tabela Delta, Unity Catalog. Não usei Colab.

## O que tem neste repositório

`notebooks/` tem ingestão, modelo, qualidade, análise, cluster e o script de comentário do Catalog. `sql/` tem as 12 consultas. `docs/data_sources.md` tem URL, tamanho e hash. `docs/data_dictionary.md` é o dicionário. Os prints do dashboard são `docs/p01_pt1.png` até `docs/p05_pt2.png`. Os do Catalog são `catalog_volume.png`, `catalog_tabelas.png`, `catalog_tabelas_2.png`, `catalog_fato.png` e `catalog_fato_2.png`.

O dashboard e as tabelas ficam no Databricks.

## O que não vai no GitHub

O CSV da ANAC. Senha, token do Databricks, token do GitHub.