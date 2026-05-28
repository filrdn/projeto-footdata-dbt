# Pipeline de Dados do Brasileirão: Da API ao com dbt e Postgres

Este projeto implementa uma esteira de dados analítica end-to-end utilizando o conceito de Modern Data Stack. O objetivo é extrair dados brutos de partidas de futebol via API REST, processá-los utilizando a Arquitetura Medalhão (Bronze, Silver e Gold) e disponibilizar uma tabela de classificação oficial totalmente agregada e performática.

## Arquitetura do Projeto e Fluxo de Dados

O ecossistema foi desenhado simulando um ambiente de produção moderno:

* **Camada Bronze:** Ingestão dos dados brutos da API via script Python e armazenamento nativo no PostgreSQL utilizando o tipo de dado JSONB para suportar dados semiestruturados.
* **Camada Silver:** Parsing do JSONB, limpeza, eliminação de duplicadas e tipagem dos dados utilizando modelos de staging no dbt materializados como Views.
* **Camada Gold:** Aplicação de Window Functions (ROW_NUMBER) e agregações para calcular os critérios de desempate e a tabela de classificação. Materializado como Tabela física para otimizar a performance de leitura.

## Tecnologias Utilizadas

* **Python:** Scripts de extração e request da API REST.
* **PostgreSQL:** Banco de dados relacional atuando como Data Lakehouse local.
* **dbt Core:** Transformação de dados, documentação, testes e gerenciamento de linhagem (lineage).
* **Git:** Versionamento de código.

## Como Executar o Projeto

1. Clone o repositório para sua máquina local.
2. Configure as credenciais do seu banco de dados PostgreSQL no arquivo profiles.yml do dbt.
3. Execute o script Python contido na pasta scripts para realizar a ingestão dos dados na camada Bronze.
4. Navegue até a pasta dbt_transformation e execute o comando "dbt run" no terminal para processar as camadas Silver e Gold.
