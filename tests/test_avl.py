import random
from src.ordem import Ordem
from src.avl import AVL, NoAVL


def validar_avl(arvore: AVL) -> None:
    """Valida recursivamente ordem de BST, alturas e |fator| <= 1 em todos os nós."""

    def _checar(no: NoAVL | None, min_k, max_k) -> int:
        if no is None:
            return 0
        if min_k is not None:
            assert no.chave > min_k, f"Violação de BST: {no.chave} <= {min_k}"
        if max_k is not None:
            assert no.chave < max_k, f"Violação de BST: {no.chave} >= {max_k}"

        alt_esq = _checar(no.esq, min_k, no.chave)
        alt_dir = _checar(no.dir, no.chave, max_k)

        alt_real = 1 + max(alt_esq, alt_dir)
        assert no.altura == alt_real, f"Altura incorreta no nó {no.chave}"

        fator = alt_esq - alt_dir
        assert abs(fator) <= 1, f"Fator de balanceamento inválido: {fator}"
        return alt_real

    _checar(arvore.raiz, None, None)


def test_avl_sequencia_aleatoria_com_seed():
    seed = 2026
    rng = random.Random(seed)
    avl = AVL()
    ativas: list[Ordem] = []

    for i in range(1, 300):
        o = Ordem(i, "V", rng.randint(100, 5000), 10, i)
        avl.inserir(o)
        ativas.append(o)
        validar_avl(avl)

    # Remove metade aleatoriamente e valida a cada passo
    rng.shuffle(ativas)
    for _ in range(150):
        alvo = ativas.pop()
        assert avl.remover(alvo) is True
        validar_avl(avl)

    chaves_arvore = [o.chave for o in avl.em_ordem()]
    chaves_gabarito = sorted(o.chave for o in ativas)
    assert chaves_arvore == chaves_gabarito
    assert avl.rotacoes > 0