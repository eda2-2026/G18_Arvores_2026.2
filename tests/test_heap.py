import random
from src.ordem import Ordem
from src.heap import MinHeap


def validar_invariante_heap(heap: MinHeap) -> None:
    """Verifica se todo pai tem chave menor ou igual à de seus filhos."""
    n = len(heap.dados)
    for i in range(n):
        esq = 2 * i + 1
        dir_ = 2 * i + 2
        if esq < n:
            assert heap.dados[i].chave <= heap.dados[esq].chave, (
                f"Violação de heap entre pai {i} e filho esq {esq}"
            )
        if dir_ < n:
            assert heap.dados[i].chave <= heap.dados[dir_].chave, (
                f"Violação de heap entre pai {i} e filho dir {dir_}"
            )


def test_heap_inserir_e_remover_raiz():
    rng = random.Random(123)
    heap = MinHeap()
    ordens = [Ordem(i, "V", rng.randint(100, 5000), 10, i) for i in range(1, 101)]

    for o in ordens:
        heap.inserir(o)
        validar_invariante_heap(heap)

    assert len(heap) == 100
    assert heap.melhor().chave == min(o.chave for o in ordens)

    extraidas = []
    while len(heap) > 0:
        extraidas.append(heap.remover_raiz().chave)
        validar_invariante_heap(heap)

    assert extraidas == sorted(o.chave for o in ordens)


def test_heap_remover_ordem_qualquer():
    """Testa cancelamento de ordens no meio do heap (incluindo caso que exige sift-up)."""
    rng = random.Random(999)
    heap = MinHeap()
    ativas = []

    for i in range(1, 150):
        o = Ordem(i, "C", rng.randint(100, 10000), 10, i)
        heap.inserir(o)
        ativas.append(o)
        validar_invariante_heap(heap)

    # Remove 60 ordens aleatórias de posições arbitrárias
    rng.shuffle(ativas)
    for _ in range(60):
        alvo = ativas.pop()
        assert heap.remover(alvo) is True
        validar_invariante_heap(heap)

    # Tentar remover ordem que já saiu deve retornar False
    assert heap.remover(Ordem(99999, "C", 500, 10, 99999)) is False

    # O restante deve sair perfeitamente ordenado
    restantes = [heap.remover_raiz().chave for _ in range(len(heap))]
    assert restantes == sorted(o.chave for o in ativas)