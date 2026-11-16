from benchmark.benchmark import (
    experimento_e1,
    experimento_e2,
    experimento_e3,
    experimento_e4,
)


def test_smoke_experimentos_benchmark():
    """Roda os 4 experimentos em escala reduzida para garantir que não há erros."""
    r1 = experimento_e1(tamanhos=(50,), n_cancel=20, repeticoes=1)
    assert len(r1) == 1

    r2 = experimento_e2(tamanhos=(50,), repeticoes=1)
    assert len(r2) == 1
    assert r2[0]["alt_bst"] == 50
    assert r2[0]["alt_avl"] < r2[0]["alt_bst"]

    r3 = experimento_e3(tamanhos=(100,), repeticoes=1)
    assert len(r3) == 1
    assert r3[0]["alt_avl"] > 0
    assert r3[0]["alt_rn"] > 0

    r4 = experimento_e4(n_pre=30, n_eventos=100, repeticoes=1)
    assert set(r4.keys()) == {"A", "B", "C"}


    