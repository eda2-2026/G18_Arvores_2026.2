from dataclasses import dataclass
from src.ordem import Ordem
from src.heap import MinHeap
from src.bst import BST
from src.avl import AVL
from src.rubro_negra import RubroNegra

ESTRUTURAS = {
    "heap": MinHeap,
    "bst": BST,
    "avl": AVL,
    "rn": RubroNegra,
    "rubro_negra": RubroNegra,
}


@dataclass
class Negocio:
    """Representa um casamento (trade) executado no livro."""
    id_compra: int
    id_venda: int
    preco: int
    qtd: int


class LivroDeOfertas:
    """
    Livro de ofertas que casa ordens de compra e venda usando
    qualquer estrutura que implemente: inserir, remover, melhor e __len__.
    """

    def __init__(self, estrutura="avl"):
        if isinstance(estrutura, str):
            chave = estrutura.lower()
            if chave not in ESTRUTURAS:
                raise ValueError(f"Estrutura desconhecida: {estrutura}")
            cls = ESTRUTURAS[chave]
        else:
            cls = estrutura

        self.compras = cls()
        self.vendas = cls()
        self.ordens_ativas: dict[int, Ordem] = {}
        self.negocios: list[Negocio] = []

    def melhor_compra(self) -> Ordem | None:
        return self.compras.melhor()

    def melhor_venda(self) -> Ordem | None:
        return self.vendas.melhor()

    def _cruza(self, nova: Ordem, melhor_oposta: Ordem) -> bool:
        """Verifica se há cruzamento de preço (compra >= venda)."""
        if nova.lado == "C":
            return nova.preco >= melhor_oposta.preco
        return melhor_oposta.preco >= nova.preco

    def enviar(self, ordem: Ordem) -> list[Negocio]:
        """
        Processa uma nova ordem limite:
        1. Casa imediatamente enquanto houver preço compatível no lado oposto.
        2. O preço do negócio é sempre o da ordem que já estava no livro.
        3. Se sobrar quantidade, insere o saldo no livro mantendo o mesmo seq.
        """
        lado_oposto = self.vendas if ordem.lado == "C" else self.compras
        meu_lado = self.compras if ordem.lado == "C" else self.vendas
        negocios_gerados: list[Negocio] = []

        while ordem.qtd > 0 and len(lado_oposto) > 0:
            melhor = lado_oposto.melhor()
            if melhor is None or not self._cruza(ordem, melhor):
                break

            q = min(ordem.qtd, melhor.qtd)
            id_c = ordem.id if ordem.lado == "C" else melhor.id
            id_v = melhor.id if ordem.lado == "C" else ordem.id

            # Regra: preço do negócio é o da ordem que já estava no livro (melhor)
            negocio = Negocio(
                id_compra=id_c,
                id_venda=id_v,
                preco=melhor.preco,
                qtd=q,
            )
            self.negocios.append(negocio)
            negocios_gerados.append(negocio)

            ordem.qtd -= q
            melhor.qtd -= q

            # Se a ordem do livro esgotou, remove da árvore e do dicionário ativo
            if melhor.qtd == 0:
                lado_oposto.remover(melhor)
                self.ordens_ativas.pop(melhor.id, None)

        # Se sobrou quantidade na ordem agressora, entra no livro
        if ordem.qtd > 0:
            meu_lado.inserir(ordem)
            self.ordens_ativas[ordem.id] = ordem

        return negocios_gerados

    def cancelar(self, id_ordem: int) -> bool:
        """
        Cancela uma ordem aberta pelo id.
        Se já foi totalmente executada ou não existe, ignora e retorna False.
        """
        ordem = self.ordens_ativas.pop(id_ordem, None)
        if ordem is None:
            return False

        lado = self.compras if ordem.lado == "C" else self.vendas
        return lado.remover(ordem)