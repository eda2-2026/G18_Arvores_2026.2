from src.gerador import gerar_carga


def test_reprodutibilidade_seed():
    c1 = gerar_carga("B", n_pre=50, n_eventos=200, seed=77)
    c2 = gerar_carga("B", n_pre=50, n_eventos=200, seed=77)
    assert c1 == c2


def test_cargas_proporcao_cancelamentos():
    carga_a = gerar_carga("A", n_pre=50, n_eventos=500, seed=1)
    assert all(ev.tipo == "ENVIAR" for ev in carga_a)

    carga_b = gerar_carga("B", n_pre=100, n_eventos=500, seed=1)
    canc_b = sum(1 for ev in carga_b if ev.tipo == "CANCELAR")

    carga_c = gerar_carga("C", n_pre=100, n_eventos=500, seed=1)
    canc_c = sum(1 for ev in carga_c if ev.tipo == "CANCELAR")

    assert canc_c > canc_b > 0


def test_carga_d_precos_estritamente_crescentes():
    carga_d = gerar_carga("D", n_pre=50, n_eventos=100, seed=1)
    precos = [ev.preco for ev in carga_d]
    assert precos == sorted(precos)
    assert len(set(precos)) == len(precos)