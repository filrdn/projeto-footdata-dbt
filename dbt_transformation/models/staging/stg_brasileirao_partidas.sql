{{ config(materialized='view') }}

with dados_bronze as (
    select * from {{ source('api_raw', 'brasileirao_fixtures_bronze') }}
)

select
    id_partida,
    -- 1. Dados da Partida (Fixture)
    (dados_brutos -> 'fixture' ->> 'id')::int as id_fixture,
    (dados_brutos -> 'fixture' ->> 'referee') as arbitro,
    (dados_brutos -> 'fixture' ->> 'timezone') as fuso_horario,
    (dados_brutos -> 'fixture' ->> 'date')::timestamp as data_partida,
    
    -- 2. Dados do Campeonato (League)
    (dados_brutos -> 'league' ->> 'name') as nome_liga,
    (dados_brutos -> 'league' ->> 'season')::int as temporada,
    (dados_brutos -> 'league' ->> 'round') as rodada,

    -- 3. Times (Mandante e Visitante)
    (dados_brutos -> 'teams' -> 'home' ->> 'id')::int as id_time_mandante,
    (dados_brutos -> 'teams' -> 'home' ->> 'name') as time_mandante,
    (dados_brutos -> 'teams' -> 'away' ->> 'id')::int as id_time_visitante,
    (dados_brutos -> 'teams' -> 'away' ->> 'name') as time_visitante,

    -- 4. Gols
    (dados_brutos -> 'goals' ->> 'home')::int as gols_mandante,
    (dados_brutos -> 'goals' ->> 'away')::int as gols_visitante,
    
    -- 5. Auditoria
    carregado_em

from dados_bronze