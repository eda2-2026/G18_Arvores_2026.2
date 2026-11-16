import os
import platform
import random
import statistics
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ordem import Ordem
from src.heap import MinHeap
from src.bst import BST
from src.avl import AVL
from src.rubro_negra import RubroNegra
from src.livro import LivroDeOfertas
from src.gerador import gerar_carga, executar_fluxo


def medir_mediana(func, repeticoes: int = 3) -> float:
    """Executa `func()` `repeticoes` vezes e retorna a mediana do tempo em segundos."""
    tempos = []
    for _ in range(repeticoes):
        t0 = time.perf_counter()
        func()
        t1 = time.perf_counter()
        tempos.append(t1 - t0)
    return statistics.median(tempos)


def experimento_e1(
    tamanhos=(2000, 5000, 20000),
    n_cancel: int = 1000,
    repeticoes: int = 3,
    seed: int = 42,
) -> list[dict]:
    """
    E1: Tempo por cancelamento (Heap simples vs AVL vs Rubro-Negra).
    Popula o livro com `n` ordens e mede apenas o tempo de cancelar `n_cancel` ordens.
    """
    resultados = []
    for n in tamanhos:
        rng = random.Random(seed + n)
        precos = [rng.randint(100, 1_000_000) for _ in range(n)]
        indices_cancel = rng.sample(range(n), min(n_cancel, n))

        tempos_estrutura = {}
        for nome, cls in [("heap", MinHeap), ("avl", AVL), ("rn", RubroNegra)]:
            medicoes = []
            for _ in range(repeticoes):
                estrutura = cls()
                ordens = [Ordem(i + 1, "V", precos[i], 10, i + 1) for i in range(n)]
                for o in ordens:
                    estrutura.inserir(o)
                alvos = [ordens[idx] for idx in indices_cancel]

                # Mede exclusivamente o bloco de cancelamentos
                t0 = time.perf_counter()
                for alvo in alvos:
                    estrutura.remover(alvo)
                t1 = time.perf_counter()
                medicoes.append(t1 - t0)

            tempos_estrutura[nome] = statistics.median(medicoes)

        resultados.append(
            {
                "n": n,
                "n_cancel": len(indices_cancel),
                "t_heap_ms": tempos_estrutura["heap"] * 1000,
                "t_avl_ms": tempos_estrutura["avl"] * 1000,
                "t_rn_ms": tempos_estrutura["rn"] * 1000,
            }
        )
    return resultados


def experimento_e2(
    tamanhos=(1000, 2500, 5000),
    repeticoes: int = 3,
    seed: int = 42,
) -> list[dict]:
    """
    E2: Altura e tempo na Carga D (preços estritamente crescentes):
    BST iterativa contra AVL e Rubro-Negra.
    """
    resultados = []
    for n in tamanhos:
        eventos = gerar_carga("D", n_pre=0, n_eventos=n, seed=seed)
        linha = {"n": n}

        for nome, cls in [("bst", BST), ("avl", AVL), ("rn", RubroNegra)]:
            medicoes = []
            altura_final = 0
            for _ in range(repeticoes):
                est = cls()
                ordens = [ev.criar_ordem() for ev in eventos]
                t0 = time.perf_counter()
                for o in ordens:
                    est.inserir(o)
                t1 = time.perf_counter()
                medicoes.append(t1 - t0)
                altura_final = est.altura()

            linha[f"t_{nome}_ms"] = statistics.median(medicoes) * 1000
            linha[f"alt_{nome}"] = altura_final

        resultados.append(linha)
    return resultados


def experimento_e3(
    tamanhos=(1000, 10000, 50000, 100000),
    repeticoes: int = 3,
    seed: int = 42,
) -> list[dict]:
    """
    E3: Altura final e número de rotações (AVL vs Rubro-Negra)
    com inserções e 50% de remoções aleatórias.
    """
    resultados = []
    for n in tamanhos:
        rng = random.Random(seed + n)
        precos = [rng.randint(100, 10_000_000) for _ in range(n)]
        indices_rem = rng.sample(range(n), n // 2)

        linha = {"n": n}
        for nome, cls in [("avl", AVL), ("rn", RubroNegra)]:
            medicoes = []
            alt_final = 0
            rot_final = 0

            for _ in range(repeticoes):
                est = cls()
                ordens = [Ordem(i + 1, "C", precos[i], 10, i + 1) for i in range(n)]
                alvos_rem = [ordens[idx] for idx in indices_rem]

                t0 = time.perf_counter()
                for o in ordens:
                    est.inserir(o)
                for alvo in alvos_rem:
                    est.remover(alvo)
                t1 = time.perf_counter()

                medicoes.append(t1 - t0)
                alt_final = est.altura()
                rot_final = est.rotacoes

            linha[f"alt_{nome}"] = alt_final
            linha[f"rot_{nome}"] = rot_final
            linha[f"t_{nome}_ms"] = statistics.median(medicoes) * 1000

        resultados.append(linha)
    return resultados


def experimento_e4(
    n_pre: int = 5000,
    n_eventos: int = 50000,
    repeticoes: int = 3,
    seed: int = 42,
) -> dict[str, dict]:
    resultados = {}
    for carga in ["A", "B", "C"]:
        eventos = gerar_carga(carga, n_pre=n_pre, n_eventos=n_eventos, seed=seed)
        tempos = {}
        
        # Para coletar métricas exatas
        livro_base = LivroDeOfertas("avl")
        efetivos = executar_fluxo(livro_base, eventos)
        negocios_count = len(livro_base.negocios)
        tamanho_final = len(livro_base.compras) + len(livro_base.vendas)
        eventos_cancel = sum(1 for e in eventos if e.tipo == "CANCELAR")

        for nome in ["heap", "avl", "rn"]:
            medicoes = []
            for _ in range(repeticoes):
                livro = LivroDeOfertas(nome)
                t0 = time.perf_counter()
                executar_fluxo(livro, eventos)
                t1 = time.perf_counter()
                medicoes.append(t1 - t0)

            tempos[nome] = statistics.median(medicoes) * 1000

        resultados[carga] = {
            "ev_cancel": eventos_cancel,
            "efetivos": efetivos,
            "tamanho_final": tamanho_final,
            "negocios": negocios_count,
            "t_heap_ms": tempos["heap"],
            "t_avl_ms": tempos["avl"],
            "t_rn_ms": tempos["rn"],
        }
    return resultados


def main() -> None:
    print("=" * 72)
    print(" BENCHMARK T3 ÁRVORES — LIVRO DE OFERTAS")
    print("=" * 72)
    print(f"Python  : {platform.python_version()} ({platform.python_implementation()})")
    print(f"Sistema : {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"CPU     : {platform.processor() or 'x86_64'}")
    print("=" * 72)

    print("\n### E1 — Tempo de 1.000 cancelamentos (ms) — Mediana de 3 repetições\n")
    r1 = experimento_e1()
    print("| N (ordens no livro) | Cancelamentos | Heap (ms) | AVL (ms) | Rubro-Negra (ms) |")
    print("|---:|---:|---:|---:|---:|")
    for row in r1:
        print(f"| {row['n']} | {row['n_cancel']} | {row['t_heap_ms']:.2f} | {row['t_avl_ms']:.2f} | {row['t_rn_ms']:.2f} |")

    print("\n### E2 — Carga D (preços crescentes): Altura e Tempo (ms)\n")
    r2 = experimento_e2()
    print("| N | Altura BST | Altura AVL | Altura RN | Tempo BST (ms) | Tempo AVL (ms) | Tempo RN (ms) |")
    print("|---:|---:|---:|---:|---:|---:|---:|")
    for row in r2:
        print(
            f"| {row['n']} | {row['alt_bst']} | {row['alt_avl']} | {row['alt_rn']} | "
            f"{row['t_bst_ms']:.2f} | {row['t_avl_ms']:.2f} | {row['t_rn_ms']:.2f} |"
        )

    print("\n### E3 — AVL vs Rubro-Negra: Altura Final, Rotações e Tempo (Inserção + 50% Remoção)\n")
    r3 = experimento_e3()
    print("| N | Altura AVL | Altura RN | Rotações AVL | Rotações RN | Tempo AVL (ms) | Tempo RN (ms) |")
    print("|---:|---:|---:|---:|---:|---:|---:|")
    for row in r3:
        print(
            f"| {row['n']} | {row['alt_avl']} | {row['alt_rn']} | "
            f"{row['rot_avl']} | {row['rot_rn']} | "
            f"{row['t_avl_ms']:.2f} | {row['t_rn_ms']:.2f} |"
        )

    print("\n### E4 — Tempo Total do Livro nas Cargas A, B e C\n")
    r4 = experimento_e4()
    print("| Carga | Ev. de Cancel. (%) | Canc. Efetivos | Tamanho Final | Negócios | Heap (ms) | AVL (ms) | Rubro-Negra (ms) |")
    print("|:---:|---:|---:|---:|---:|---:|---:|---:|")
    probs = {"A": "0%", "B": "30%", "C": "60%"}
    for carga, row in r4.items():
        print(
            f"| {carga} | {row['ev_cancel']} ({probs[carga]}) | {row['efetivos']} | {row['tamanho_final']} | {row['negocios']} | "
            f"{row['t_heap_ms']:.2f} | {row['t_avl_ms']:.2f} | {row['t_rn_ms']:.2f} |"
        )


if __name__ == "__main__":
    main()