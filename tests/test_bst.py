import random
from src.ordem import Ordem
from src.bst import BST


def test_bst_inserir_buscar_remover_tres_casos():
    bst = BST()
    # Chaves (preco, seq) para venda
    precos = [500, 300, 700, 200, 400, 600, 800, 350, 450]
    ordens = [Ordem(i + 1, "V", p, 10, i + 1) for i, p in enumerate(precos)]

    for o in ordens:
        bst.inserir(o)

    assert len(bst) == len(ordens)
    assert bst.melhor().preco == 200
    assert bst.buscar(ordens[4].chave) == ordens[4]

    # Caso 1: remover folha (200)
    assert bst.remover(ordens[3]) is True
    assert bst.melhor().preco == 300

    # Caso 2: remover nó com 1 filho (300 agora só tem filho direito 400)
    assert bst.remover(ordens[1]) is True

    # Caso 3: remover raiz com 2 filhos (500)
    assert bst.remover(ordens[0]) is True

    chaves_em_ordem = [o.chave for o in bst.em_ordem()]
    assert chaves_em_ordem == sorted(chaves_em_ordem)
    assert len(bst) == len(ordens) - 3


def test_bst_degenerada_sem_recursion_error():
    """Com 1500 preços crescentes, a árvore vira uma lista de altura 1500 sem estourar pilha."""
    bst = BST()
    n = 1500
    for i in range(1, n + 1):
        bst.inserir(Ordem(i, "V", i * 10, 5, i))

    assert len(bst) == n
    assert bst.altura() == n
    assert bst.melhor().preco == 10