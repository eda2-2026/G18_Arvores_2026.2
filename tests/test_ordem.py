import pytest
from src.ordem import Ordem


def test_chave_prioridade_compra():
    # Compra: maior preço tem menor chave (-preco, seq)
    o1 = Ordem(1, "C", preco=1050, qtd=10, seq=1)
    o2 = Ordem(2, "C", preco=1100, qtd=10, seq=2)
    assert o2.chave < o1.chave


def test_chave_prioridade_venda():
    # Venda: menor preço tem menor chave (preco, seq)
    o1 = Ordem(1, "V", preco=1050, qtd=10, seq=2)
    o2 = Ordem(2, "V", preco=1100, qtd=10, seq=1)
    assert o1.chave < o2.chave


def test_desempate_por_seq():
    # Mesmo preço: quem chegou antes (menor seq) tem menor chave
    c1 = Ordem(1, "C", preco=1000, qtd=10, seq=1)
    c2 = Ordem(2, "C", preco=1000, qtd=10, seq=2)
    assert c1.chave < c2.chave

    v1 = Ordem(3, "V", preco=1000, qtd=10, seq=5)
    v2 = Ordem(4, "V", preco=1000, qtd=10, seq=8)
    assert v1.chave < v2.chave


def test_validacao_ordem_invalida():
    with pytest.raises(ValueError):
        Ordem(1, "X", 1000, 10, 1)
    with pytest.raises(ValueError):
        Ordem(1, "C", 0, 10, 1)
    with pytest.raises(ValueError):
        Ordem(1, "V", 1000, -5, 1)