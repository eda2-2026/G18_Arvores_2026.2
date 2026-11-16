import random
import pytest
from src.ordem import Ordem
from src.rubro_negra import RubroNegra, NoRN, VERMELHO, PRETO


def validar_rubro_negra(rn: RubroNegra, seed_info: int = 0) -> None:
    """
    Valida as 5 propriedades da Árvore Rubro-Negra + ordem da BST:
    1. Todo nó é vermelho ou preto.
    2. A raiz é preta.
    3. Toda folha (NIL) é preta.
    4. Se um nó é vermelho, seus dois filhos são pretos (sem vermelho-vermelho).
    5. Todos os caminhos de um nó até folhas NIL têm a mesma altura preta (black-height).
    """
    # Propriedade 3: sentinela NIL é preto
    assert rn.NIL.cor == PRETO, f"[seed={seed_info}] Sentinela NIL não é preto!"

    if rn.raiz == rn.NIL:
        return

    # Propriedade 2: a raiz é preta
    assert rn.raiz.cor == PRETO, f"[seed={seed_info}] A raiz não é preta!"
    assert rn.raiz.pai == rn.NIL, f"[seed={seed_info}] Pai da raiz não é NIL!"

    def _checar(no: NoRN, min_k, max_k) -> int:
        if no == rn.NIL:
            return 1  # NIL conta como 1 preto

        # Propriedade 1
        assert no.cor in (VERMELHO, PRETO), f"[seed={seed_info}] Cor inválida"

        # Ordem de BST
        if min_k is not None:
            assert no.chave > min_k, f"[seed={seed_info}] Violação BST esq"
        if max_k is not None:
            assert no.chave < max_k, f"[seed={seed_info}] Violação BST dir"

        # Consistência de ponteiros de pai
        if no.esq != rn.NIL:
            assert no.esq.pai == no, f"[seed={seed_info}] Ponteiro pai esq quebrado"
        if no.dir != rn.NIL:
            assert no.dir.pai == no, f"[seed={seed_info}] Ponteiro pai dir quebrado"

        # Propriedade 4: nó vermelho só tem filhos pretos
        if no.cor == VERMELHO:
            assert no.esq.cor == PRETO and no.dir.cor == PRETO, (
                f"[seed={seed_info}] Conflito Vermelho-Vermelho no nó {no.chave}"
            )

        bh_esq = _checar(no.esq, min_k, no.chave)
        bh_dir = _checar(no.dir, no.chave, max_k)

        # Propriedade 5: mesma altura preta nos dois lados
        assert bh_esq == bh_dir, (
            f"[seed={seed_info}] Altura preta diferente ({bh_esq} != {bh_dir}) em {no.chave}"
        )

        return bh_esq + (1 if no.cor == PRETO else 0)

    _checar(rn.raiz, None, None)


@pytest.mark.parametrize("seed", [10, 42, 99, 2026, 7777])
def test_rubro_negra_aleatorio_com_seed(seed: int):
    rng = random.Random(seed)
    rn = RubroNegra()
    ativas: list[Ordem] = []

    for i in range(1, 250):
        o = Ordem(i, "C", rng.randint(100, 10000), 10, i)
        rn.inserir(o)
        ativas.append(o)
        validar_rubro_negra(rn, seed_info=seed)

    rng.shuffle(ativas)
    while ativas:
        alvo = ativas.pop()
        assert rn.remover(alvo) is True, f"Falha ao remover na seed {seed}"
        validar_rubro_negra(rn, seed_info=seed)

        if len(ativas) % 40 == 0:
            chaves_rn = [o.chave for o in rn.em_ordem()]
            assert chaves_rn == sorted(o.chave for o in ativas), f"Falha na seed {seed}"

    assert len(rn) == 0