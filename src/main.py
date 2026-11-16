import argparse
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.livro import LivroDeOfertas
from src.gerador import gerar_carga, executar_fluxo


def formatar_reais(centavos: int) -> str:
    return f"R$ {centavos / 100:,.2f}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="CLI do Livro de Ofertas (T3 - Árvores)"
    )
    parser.add_argument(
        "--estrutura",
        choices=["heap", "bst", "avl", "rn"],
        default="avl",
        help="Estrutura de dados do livro (padrão: avl)",
    )
    parser.add_argument(
        "--carga",
        choices=["A", "B", "C", "D"],
        default="B",
        help="Tipo de carga sintética A, B, C ou D (padrão: B)",
    )
    parser.add_argument(
        "--pre",
        type=int,
        default=200,
        help="Ordens pré-carregadas no livro (padrão: 200)",
    )
    parser.add_argument(
        "--eventos",
        type=int,
        default=1000,
        help="Quantidade de eventos dinâmicos (padrão: 1000)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Seed para reprodutibilidade (padrão: 42)",
    )
    args = parser.parse_args()

    print("=" * 60)
    print(f" LIVRO DE OFERTAS — Ativo: INGRESSO_SHOW (Lote Único)")
    print(f" Estrutura: {args.estrutura.upper()} | Carga: {args.carga} | Seed: {args.seed}")
    print("=" * 60)

    eventos = gerar_carga(
        carga=args.carga,
        n_pre=args.pre,
        n_eventos=args.eventos,
        seed=args.seed,
    )
    livro = LivroDeOfertas(args.estrutura)
    executar_fluxo(livro, eventos)

    melhor_c = livro.melhor_compra()
    melhor_v = livro.melhor_venda()

    print(f"Total de eventos processados : {len(eventos)}")
    print(f"Negócios realizados (trades) : {len(livro.negocios)}")
    print(f"Ordens abertas na Compra     : {len(livro.compras)}")
    print(f"Ordens abertas na Venda      : {len(livro.vendas)}")
    print("-" * 60)

    if melhor_c:
        print(
            f"Melhor Compra (Bid) : {formatar_reais(melhor_c.preco)} "
            f"(qtd={melhor_c.qtd}, id={melhor_c.id}, seq={melhor_c.seq})"
        )
    else:
        print("Melhor Compra (Bid) : Vazio")

    if melhor_v:
        print(
            f"Melhor Venda  (Ask) : {formatar_reais(melhor_v.preco)} "
            f"(qtd={melhor_v.qtd}, id={melhor_v.id}, seq={melhor_v.seq})"
        )
    else:
        print("Melhor Venda  (Ask) : Vazio")

    if livro.negocios:
        print("-" * 60)
        print("Últimos 5 negócios executados:")
        for neg in livro.negocios[-5:]:
            print(
                f"  • Compra #{neg.id_compra} x Venda #{neg.id_venda} -> "
                f"{neg.qtd} un. a {formatar_reais(neg.preco)}"
            )
    print("=" * 60)


if __name__ == "__main__":
    main()