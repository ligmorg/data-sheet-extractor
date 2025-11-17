import pytest
from models.produto import Produto
from utils.helpers import *

def test_ean_valido_true():
    assert ean_valido("1234567890123") is True
    assert ean_valido("01234567890123") is True


def test_ean_valido_false():
    assert ean_valido("abc") is False
    assert ean_valido("123") is False
    assert ean_valido("") is False


def test_produto_unico_true():
    p1 = Produto("1234567890123", "Prod A", 10)
    lista = [p1]

    assert produto_unico("9999999999999", lista) is True


def test_produto_unico_false():
    p1 = Produto("1234567890123", "Prod A", 10)
    lista = [p1]

    assert produto_unico("1234567890123", lista) is False


def test_valida_coluna_estoque_true(capsys):
    result = valida_coluna_estoque(3, "Sheet1")

    captured = capsys.readouterr()
    assert "faltando" not in captured.out
    assert result is True


def test_valida_coluna_estoque_false(capsys):
    result = valida_coluna_estoque(-1, "Sheet X")

    captured = capsys.readouterr()
    assert "Coluna Estoque faltando na planilha Sheet X" in captured.out
    assert result is False
