from src.ordem import Ordem
from src.livro import LivroDeOfertas
from src.gerador import gerar_carga, executar_fluxo


def test_casamento_total_e_cancelamento_executada():
    livro = LivroDeOfertas("avl")
    livro.enviar(Ordem(1, "V", preco=1000, qtd=10, seq=1))
    negocios = livro.enviar(Ordem(2, "C", preco=1000, qtd=10, seq=2))

    assert len(negocios) == 1
    assert negocios[0].preco == 1000
    assert negocios[0].qtd == 10
    assert len(livro.compras) == 0
    assert len(livro.vendas) == 0

    # Cancelar ordem já executada deve ignorar e devolver False
    assert livro.cancelar(1) is False
    assert livro.cancelar(2) is False


def test_casamento_parcial_mantem_seq():
    livro = LivroDeOfertas("avl")
    livro.enviar(Ordem(1, "V", preco=1000, qtd=50, seq=1))
    livro.enviar(Ordem(2, "V", preco=1000, qtd=20, seq=2))

    # Compra 30 unidades: consome parte da ordem 1, que deve continuar no topo com seq=1
    negocios = livro.enviar(Ordem(3, "C", preco=1050, qtd=30, seq=3))
    assert len(negocios) == 1
    assert negocios[0].id_venda == 1
    assert negocios[0].preco == 1000  # Preço de quem já estava no livro
    assert negocios[0].qtd == 30

    melhor_v = livro.melhor_venda()
    assert melhor_v.id == 1
    assert melhor_v.qtd == 20
    assert melhor_v.seq == 1


def test_atravessando_varios_niveis_de_preco():
    livro = LivroDeOfertas("rn")
    livro.enviar(Ordem(1, "V", preco=1000, qtd=10, seq=1))
    livro.enviar(Ordem(2, "V", preco=1010, qtd=15, seq=2))
    livro.enviar(Ordem(3, "V", preco=1020, qtd=20, seq=3))

    # Compra de 35 a 1015: leva toda a #1 (10), toda a #2 (15) e 10 unidades ficam no livro
    negocios = livro.enviar(Ordem(4, "C", preco=1015, qtd=35, seq=4))
    assert len(negocios) == 2
    assert (negocios[0].preco, negocios[0].qtd) == (1000, 10)
    assert (negocios[1].preco, negocios[1].qtd) == (1010, 15)

    assert livro.melhor_compra().id == 4
    assert livro.melhor_compra().qtd == 10
    assert livro.melhor_venda().id == 3


def test_empate_preco_resolvido_por_chegada():
    livro = LivroDeOfertas("heap")
    livro.enviar(Ordem(10, "C", preco=2000, qtd=10, seq=1))
    livro.enviar(Ordem(11, "C", preco=2000, qtd=10, seq=2))

    negocios = livro.enviar(Ordem(12, "V", preco=1950, qtd=10, seq=3))
    assert len(negocios) == 1
    assert negocios[0].id_compra == 10  # Ordem 10 chegou primeiro (seq=1)


def test_equivalencia_entre_estruturas():
    """O mesmo fluxo com Heap, AVL, Rubro-Negra e BST gera exatamente os mesmos negócios."""
    eventos = gerar_carga("B", n_pre=200, n_eventos=800, seed=12345)

    resultados = {}
    for nome in ["heap", "avl", "rn", "bst"]:
        livro = LivroDeOfertas(nome)
        executar_fluxo(livro, eventos)
        resultados[nome] = livro.negocios

    assert len(resultados["heap"]) > 0
    assert resultados["heap"] == resultados["avl"]
    assert resultados["avl"] == resultados["rn"]
    assert resultados["rn"] == resultados["bst"]