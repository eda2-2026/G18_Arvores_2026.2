import random
from dataclasses import dataclass
from src.ordem import Ordem


@dataclass
class Evento:
    """
    Evento do fluxo sintético:
    tipo = 'ENVIAR' (usa dados da ordem) ou 'CANCELAR' (usa id_alvo).
    Guardamos os atributos primitivos para instanciar uma Ordem nova em cada
    estrutura durante o benchmark, evitando efeitos colaterais de mutação de qtd.
    """
    tipo: str  # "ENVIAR" ou "CANCELAR"
    id_ordem: int = 0
    lado: str = "C"
    preco: int = 0
    qtd: int = 0
    seq: int = 0
    id_cancelar: int = 0

    def criar_ordem(self) -> Ordem:
        return Ordem(self.id_ordem, self.lado, self.preco, self.qtd, self.seq)


def gerar_carga(
    carga: str,
    n_pre: int = 1000,
    n_eventos: int = 5000,
    seed: int = 42,
) -> list[Evento]:
    """
    Gera o fluxo de eventos sintéticos conforme a especificação da seção 5:
    - Pré-carrega `n_pre` ordens longe do spread para manter o livro populado.
    - A: 0% cancelamento
    - B: 30% cancelamento
    - C: 60% cancelamento
    - D: Preços de venda crescendo sempre (degeneração da BST)
    """
    carga = carga.upper()
    probs_cancel = {"A": 0.0, "B": 0.30, "C": 0.60, "D": 0.0}
    if carga not in probs_cancel:
        raise ValueError("A carga deve ser 'A', 'B', 'C' ou 'D'.")

    rng = random.Random(seed)
    prob_cancel = probs_cancel[carga]
    eventos: list[Evento] = []
    ids_abertos: list[int] = []

    preco_ref = 100_00  # R$ 100,00 em centavos
    prox_id = 1
    prox_seq = 1

    # 1. Caso especial Carga D: Preços de venda estritamente crescentes (sem casamento)
    if carga == "D":
        total = n_pre + n_eventos
        for i in range(total):
            preco = preco_ref + (i + 1) * 10
            qtd = rng.randint(1, 50)
            eventos.append(
                Evento("ENVIAR", prox_id, "V", preco, qtd, prox_seq)
            )
            prox_id += 1
            prox_seq += 1
        return eventos

    # 2. Pré-carregamento do "livro grande" (ordens longe do spread que não se cruzam)
    for _ in range(n_pre):
        lado = "C" if rng.random() < 0.5 else "V"
        dist = rng.randint(50, 500)
        preco = (preco_ref - dist) if lado == "C" else (preco_ref + dist)
        preco = max(10, preco)
        qtd = rng.randint(10, 100)

        eventos.append(Evento("ENVIAR", prox_id, lado, preco, qtd, prox_seq))
        ids_abertos.append(prox_id)
        prox_id += 1
        prox_seq += 1

    # 3. Fluxo dinâmico com passeio aleatório do preço de referência
    for _ in range(n_eventos):
        if ids_abertos and rng.random() < prob_cancel:
            # Escolhe uma ordem aberta aleatória para cancelar (swap-and-pop O(1))
            idx = rng.randrange(len(ids_abertos))
            id_alvo = ids_abertos[idx]
            ids_abertos[idx] = ids_abertos[-1]
            ids_abertos.pop()
            eventos.append(Evento("CANCELAR", id_cancelar=id_alvo))
        else:
            # Passeio aleatório no preço de referência
            preco_ref = max(500, preco_ref + rng.choice([-10, -5, 0, 5, 10]))
            lado = "C" if rng.random() < 0.5 else "V"

            # Deslocamento que permite algumas ordens cruzarem o spread (-20 a +60)
            desloc = rng.randint(-20, 60)
            if lado == "C":
                preco = max(10, preco_ref - desloc)
            else:
                preco = max(10, preco_ref + desloc)

            qtd = rng.randint(5, 80)
            eventos.append(Evento("ENVIAR", prox_id, lado, preco, qtd, prox_seq))
            ids_abertos.append(prox_id)
            prox_id += 1
            prox_seq += 1

    return eventos


def executar_fluxo(livro, eventos: list) -> int:
    """
    Aplica uma lista de eventos e retorna a quantidade de cancelamentos efetivos.
    """
    cancelamentos_efetivos = 0
    for ev in eventos:
        if ev.tipo == "ENVIAR":
            livro.enviar(ev.criar_ordem())
        elif ev.tipo == "CANCELAR":
            sucesso = livro.cancelar(ev.id_cancelar)
            if sucesso:
                cancelamentos_efetivos += 1
    return cancelamentos_efetivos