import pytest
from utils.normalizacao import *


def test_remove_numeros_e_simbolos():
    texto = "123teste ./23@teste"

    result = remove_numeros_e_simbolos(texto)
    assert result == "teste teste"


def test_remove_letras():
    texto = "123teste ./23@teste"

    result = remove_letras(texto)
    assert result == "123 ./23@"


