{{ config(materialized='table') }}

with partidas as (
    select * from {{ ref('stg_brasileirao_partidas') }}
),

-- Vamos unificar os dados sob a perspectiva de cada time (seja mandante ou visitante)
desempenho_times as (
    -- Visão do Mandante
    select
        temporada,
        id_time_mandante as id_time,
        time_mandante as nome_time,
        gols_mandante as gols_feitos,
        gols_visitante as gols_sofridos,
        case 
            when gols_mandante > gols_visitante then 3
            when gols_mandante = gols_visitante then 1
            else 0
        end as pontos,
        case when gols_mandante > gols_visitante then 1 else 0 end as vitoria,
        case when gols_mandante = gols_visitante then 1 else 0 end as empate,
        case when gols_mandante < gols_visitante then 1 else 0 end as derrota
    from partidas

    union all

    -- Visão do Visitante
    select
        temporada,
        id_time_visitante as id_time,
        time_visitante as nome_time,
        gols_visitante as gols_feitos,
        gols_mandante as gols_sofridos,
        case 
            when gols_visitante > gols_mandante then 3
            when gols_visitante = gols_mandante then 1
            else 0
        end as pontos,
        case when gols_visitante > gols_mandante then 1 else 0 end as vitoria,
        case when gols_visitante = gols_mandante then 1 else 0 end as empate,
        case when gols_visitante < gols_mandante then 1 else 0 end as derrota
    from partidas
)

-- Agora agrupamos e somamos tudo para gerar a tabela final de classificação!
select
    row_number() over(
        partition by temporada 
        order by sum(pontos) desc, sum(vitoria) desc, (sum(gols_feitos) - sum(gols_sofridos)) desc
    ) as posicao,
    temporada,
    id_time,
    nome_time,
    count(*) as jogos_disputados,
    sum(pontos) as pontos_totais,
    sum(vitoria) as vitorias,
    sum(empate) as empates,
    sum(derrota) as derrotas,
    sum(gols_feitos) as gols_pro,
    sum(gols_sofridos) as gols_contra,
    (sum(gols_feitos) - sum(gols_sofridos)) as saldo_de_gols
from desempenho_times
group by temporada, id_time, nome_time
order by pontos_totais desc, vitorias desc, saldo_de_gols desc