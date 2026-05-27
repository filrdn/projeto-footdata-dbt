Pipeline de Dados do Brasileirão: Da API ao Insight com dbt e Postgres

Este projeto implementa uma esteira de dados analítica *end-to-end* utilizando o conceito de **Modern Data Stack**. O objetivo é extrair dados brutos de partidas de futebol via API REST, processá-los utilizando a **Arquitetura Medalhão** (Bronze, Silver e Gold) e disponibilizar uma tabela de classificação oficial totalmente agregada e performática.

Arquitetura do Projeto e Fluxo de Dados

O ecossistema foi desenhado simulando um ambiente de produção moderno:

[ API REST ] 
     │ (Request em Python)
     ▼
┌────────────────────────────────────────────────────────┐
│               POSTGRESQL (DATA LAKEHOUSE)              │
│                                                        │
│  🥉 Camada Bronze: Ingestão de dados brutos em JSONB   │
│         │                                              │
│         ▼ (Parsing JSONB + dbt Models)                │
│  🥈 Camada Silver: Tabelas de Staging e Typagem        │
│         │                                              │
│         ▼ (Window Functions + Agregações dbt)          │
│  🥇 Camada Gold: Fato Classificação (Materialized)    │
└────────────────────────────────────────────────────────┘
