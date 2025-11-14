from src.models.produto import Produto

def test_cria_produto():
    prod = Produto("1234567890123", "Sabonete", 10)

    assert prod.ean == "1234567890123"
    assert prod.descricao == "Sabonete"
    assert prod.estoque == 10

def test_str_produto():
    prod = Produto("111", "Teste", 5)
    texto = str(prod)
    assert "Produto(EAN=111" in texto
