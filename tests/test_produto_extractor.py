import pytest
from src.extractor.produto_extractor import *


def test_get_column_name_retorna_primeira_ocorrencia():
    df = pd.DataFrame(columns=["dsp1", "dsp2", "qtd_total"])
    result = get_column_name(df, variacoes_estoque)
    assert result == "dsp1"

def test_get_column_name_codigo_barras():
    df = pd.DataFrame(columns=["ean", "produto", "valor"])
    result = get_column_name(df, variacoes_codigo_barras)

    assert result == "ean"

def test_get_column_name_sem_match():
    df = pd.DataFrame(columns=["AAA", "BBB", "CCC"])
    result = get_column_name(df, variacoes_descricao)
    assert result is None

def test_get_column_index_match_simples():
    df = pd.DataFrame([
        ["A", "produto em estoque", "vendas"],
        ["foo", "10", "100"],
        ["bar", "20", "200"]
    ])
    index = get_column_index(df, variacoes_estoque)
    assert index == 1

def test_get_column_index_sem_match():
    df = pd.DataFrame([
        ["A", "mes", "vendas"],
        ["foo", "1", "100"],
        ["bar", "2", "200"]
    ])
    index = get_column_index(df, variacoes_estoque)
    assert index == -1


def test_extract_products():
    assert extract_products("../mapa.xlsx", "Mapa Farmix MG", [], []) == None
