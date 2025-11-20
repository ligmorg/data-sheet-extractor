import pytest
from src.extractor.produto_extractor import *


def test_extract_products():
    assert extract_products("../mapa.xlsx", "Mapa Farmix MG", [], []) == None
