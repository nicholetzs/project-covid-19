-- MODELAGEM MULTIDIMENSIONAL - SCHEMA ESTRELA
-- COVID-19 ES 
-- Este script cria apenas as tabelas (DDL)
-- Não inclui carga de dados (Passo 4-6 do PDF vêm depois)

-- 1. DIMENSÃO TEMPO (role-playing × 6)
DROP TABLE IF EXISTS dim_tempo CASCADE;

CREATE TABLE dim_tempo (
    sk_tempo INT PRIMARY KEY,
    data DATE,
    dia SMALLINT,
    mes SMALLINT,
    ano SMALLINT,
    trimestre SMALLINT,
    nome_mes VARCHAR(15),
    dia_semana VARCHAR(15),
    ano_mes CHAR(7),                -- '2026-03'
    eh_fim_de_semana BOOLEAN,
    semana_epidemiologica SMALLINT
);

-- Membro "Desconhecido" para datas ausentes
INSERT INTO dim_tempo VALUES
(-1, NULL, NULL, NULL, NULL, NULL, 'Desconhecido', 'Desconhecido', 'N/D', FALSE, NULL);

-- ========================================
-- 2. DIMENSÃO LOCALIDADE
-- ========================================
DROP TABLE IF EXISTS dim_localidade CASCADE;

CREATE TABLE dim_localidade (
    sk_local SERIAL PRIMARY KEY,
    municipio VARCHAR(100),
    bairro VARCHAR(150),
    uf CHAR(2) DEFAULT 'ES',
    regiao_es VARCHAR(30),
    macrorregiao_saude VARCHAR(30),
    UNIQUE (municipio, bairro)
);

INSERT INTO dim_localidade (sk_local, municipio, bairro, uf, regiao_es, macrorregiao_saude)
OVERRIDING SYSTEM VALUE
VALUES (-1, 'Desconhecido', 'Desconhecido', 'ES', 'Desconhecida', 'Desconhecida');

-- ========================================
-- 3. DIMENSÃO PERFIL PACIENTE
-- ========================================
DROP TABLE IF EXISTS dim_perfil_paciente CASCADE;

CREATE TABLE dim_perfil_paciente (
    sk_perfil SERIAL PRIMARY KEY,
    sexo VARCHAR(20),
    faixa_etaria VARCHAR(30),
    raca_cor VARCHAR(30),
    escolaridade VARCHAR(100),
    gestante VARCHAR(40),
    profissional_saude VARCHAR(20),
    morador_rua VARCHAR(20),
    possui_deficiencia VARCHAR(20),
    UNIQUE (sexo, faixa_etaria, raca_cor, escolaridade, gestante, profissional_saude, morador_rua, possui_deficiencia)
);

INSERT INTO dim_perfil_paciente (sk_perfil, sexo, faixa_etaria, raca_cor, escolaridade, gestante, profissional_saude, morador_rua, possui_deficiencia)
OVERRIDING SYSTEM VALUE
VALUES (-1, 'Desconhecido', 'Desconhecida', 'Desconhecida', 'Desconhecida', 'Desconhecido', 'Desconhecido', 'Desconhecido', 'Desconhecido');

-- ========================================
-- 4. DIMENSÃO CLASSIFICAÇÃO
-- ========================================
DROP TABLE IF EXISTS dim_classificacao CASCADE;

CREATE TABLE dim_classificacao (
    sk_class SERIAL PRIMARY KEY,
    classificacao VARCHAR(50),
    evolucao VARCHAR(50),
    criterio_confirmacao VARCHAR(50),
    status_notificacao VARCHAR(30),
    UNIQUE (classificacao, evolucao, criterio_confirmacao, status_notificacao)
);

INSERT INTO dim_classificacao (sk_class, classificacao, evolucao, criterio_confirmacao, status_notificacao)
OVERRIDING SYSTEM VALUE
VALUES (-1, 'Desconhecida', 'Desconhecida', 'Desconhecido', 'Desconhecido');

-- ========================================
-- 5. DIMENSÃO SINTOMAS (junk dimension)
-- ========================================
DROP TABLE IF EXISTS dim_sintomas CASCADE;

CREATE TABLE dim_sintomas (
    sk_sint SERIAL PRIMARY KEY,
    febre VARCHAR(20),
    dif_respiratoria VARCHAR(20),
    tosse VARCHAR(20),
    coriza VARCHAR(20),
    dor_garganta VARCHAR(20),
    diarreia VARCHAR(20),
    cefaleia VARCHAR(20),
    UNIQUE (febre, dif_respiratoria, tosse, coriza, dor_garganta, diarreia, cefaleia)
);

INSERT INTO dim_sintomas (sk_sint, febre, dif_respiratoria, tosse, coriza, dor_garganta, diarreia, cefaleia)
OVERRIDING SYSTEM VALUE
VALUES (-1, 'Desconhecido', 'Desconhecido', 'Desconhecido', 'Desconhecido', 'Desconhecido', 'Desconhecido', 'Desconhecido');

-- ========================================
-- 6. DIMENSÃO COMORBIDADE (junk dimension)
-- ========================================
DROP TABLE IF EXISTS dim_comorbidade CASCADE;

CREATE TABLE dim_comorbidade (
    sk_como SERIAL PRIMARY KEY,
    com_pulmao VARCHAR(20),
    com_cardio VARCHAR(20),
    com_renal VARCHAR(20),
    com_diabetes VARCHAR(20),
    com_tabagismo VARCHAR(20),
    com_obesidade VARCHAR(20),
    UNIQUE (com_pulmao, com_cardio, com_renal, com_diabetes, com_tabagismo, com_obesidade)
);

INSERT INTO dim_comorbidade (sk_como, com_pulmao, com_cardio, com_renal, com_diabetes, com_tabagismo, com_obesidade)
OVERRIDING SYSTEM VALUE
VALUES (-1, 'Desconhecido', 'Desconhecido', 'Desconhecido', 'Desconhecido', 'Desconhecido', 'Desconhecido');

-- ========================================
-- 7. DIMENSÃO TESTE
-- ========================================
DROP TABLE IF EXISTS dim_teste CASCADE;

CREATE TABLE dim_teste (
    sk_teste SERIAL PRIMARY KEY,
    tipo_teste_rapido VARCHAR(60),
    resultado_rt_pcr VARCHAR(30),
    resultado_teste_rap VARCHAR(30),
    resultado_sorologia VARCHAR(30),
    resultado_sorol_igg VARCHAR(30),
    UNIQUE (tipo_teste_rapido, resultado_rt_pcr, resultado_teste_rap, resultado_sorologia, resultado_sorol_igg)
);

INSERT INTO dim_teste (sk_teste, tipo_teste_rapido, resultado_rt_pcr, resultado_teste_rap, resultado_sorologia, resultado_sorol_igg)
OVERRIDING SYSTEM VALUE
VALUES (-1, 'Desconhecido', 'Desconhecido', 'Desconhecido', 'Desconhecido', 'Desconhecido');

-- ========================================
-- 8. TABELA FATO (grão: 1 notificação)
-- ========================================
DROP TABLE IF EXISTS fato_notif_covid CASCADE;

CREATE TABLE fato_notif_covid (
    sk_fato BIGSERIAL PRIMARY KEY,

    -- Dimensões de tempo (role-playing × 6)
    sk_data_notificacao INT NOT NULL REFERENCES dim_tempo(sk_tempo),
    sk_data_cadastro INT NOT NULL REFERENCES dim_tempo(sk_tempo),
    sk_data_diagnostico INT NOT NULL REFERENCES dim_tempo(sk_tempo),
    sk_data_coleta INT NOT NULL REFERENCES dim_tempo(sk_tempo),
    sk_data_encerramento INT NOT NULL REFERENCES dim_tempo(sk_tempo),
    sk_data_obito INT NOT NULL REFERENCES dim_tempo(sk_tempo),

    -- Dimensões descritivas
    sk_local INT NOT NULL REFERENCES dim_localidade(sk_local),
    sk_perfil INT NOT NULL REFERENCES dim_perfil_paciente(sk_perfil),
    sk_class INT NOT NULL REFERENCES dim_classificacao(sk_class),
    sk_sint INT NOT NULL REFERENCES dim_sintomas(sk_sint),
    sk_como INT NOT NULL REFERENCES dim_comorbidade(sk_como),
    sk_teste INT NOT NULL REFERENCES dim_teste(sk_teste),

    -- Medidas aditivas
    qtd_notificacao SMALLINT NOT NULL DEFAULT 1,
    flag_confirmado SMALLINT NOT NULL DEFAULT 0,
    flag_obito_covid SMALLINT NOT NULL DEFAULT 0,
    flag_internado SMALLINT NOT NULL DEFAULT 0,
    flag_cura SMALLINT NOT NULL DEFAULT 0,

    -- Medidas semi-aditivas
    idade_anos SMALLINT,
    dias_notif_encerramento INT,
    dias_notif_obito INT
);

-- ========================================
-- ÍNDICES RECOMENDADOS (OLAP)
-- ========================================
CREATE INDEX idx_fato_data_notif ON fato_notif_covid (sk_data_notificacao);
CREATE INDEX idx_fato_local ON fato_notif_covid (sk_local);
CREATE INDEX idx_fato_class ON fato_notif_covid (sk_class);
CREATE INDEX idx_fato_perfil ON fato_notif_covid (sk_perfil);

-- ========================================
-- RESUMO DO MODELO
-- ========================================
-- Dimensões: 7 (tempo, localidade, perfil, classificacao, sintomas, comorbidade, teste)
-- Fato: 1 (notif_covid)
-- Grão de negócio: 1 linha da fato = 1 notificação de COVID-19
-- Role-playing: 6 FKs de tempo na fato (notificação, cadastro, diagnóstico, coleta, encerramento, óbito)
-- Junk dimensions: dim_sintomas, dim_comorbidade (consolidam flags booleanas)
-- Known members: SK -1 é "Desconhecido" em toda dimensão (evita NULLs nas FKs)
