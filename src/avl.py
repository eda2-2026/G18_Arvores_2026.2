from src.ordem import Ordem


class NoAVL:
    """Nó da Árvore AVL com controle de altura."""

    def __init__(self, ordem: Ordem):
        self.chave = ordem.chave
        self.ordem = ordem
        self.esq: NoAVL | None = None
        self.dir: NoAVL | None = None
        self.altura: int = 1


class AVL:
    """Árvore AVL auto-balanceada com contador de rotações."""

    def __init__(self):
        self.raiz: NoAVL | None = None
        self._tamanho: int = 0
        self.rotacoes: int = 0

    def __len__(self) -> int:
        return self._tamanho

    def altura(self) -> int:
        """Retorna a altura atual da árvore."""
        return self._altura(self.raiz)

    def _altura(self, no: NoAVL | None) -> int:
        return no.altura if no is not None else 0

    def _atualizar_altura(self, no: NoAVL) -> None:
        no.altura = 1 + max(self._altura(no.esq), self._altura(no.dir))

    def fator_balanceamento(self, no: NoAVL | None) -> int:
        """Fator = altura(esq) - altura(dir)."""
        if no is None:
            return 0
        return self._altura(no.esq) - self._altura(no.dir)

    def _rotacao_direita(self, y: NoAVL) -> NoAVL:
        """Rotação simples à direita."""
        self.rotacoes += 1
        x = y.esq
        t2 = x.dir

        x.dir = y
        y.esq = t2

        self._atualizar_altura(y)
        self._atualizar_altura(x)
        return x

    def _rotacao_esquerda(self, x: NoAVL) -> NoAVL:
        """Rotação simples à esquerda."""
        self.rotacoes += 1
        y = x.dir
        t2 = y.esq

        y.esq = x
        x.dir = t2

        self._atualizar_altura(x)
        self._atualizar_altura(y)
        return y

    def _rebalancear(self, no: NoAVL) -> NoAVL:
        """Atualiza altura do nó e aplica rotações se |fator| > 1."""
        self._atualizar_altura(no)
        fator = self.fator_balanceamento(no)

        # Pesado à esquerda
        if fator > 1:
            if self.fator_balanceamento(no.esq) < 0:
                # Rotação dupla Esquerda-Direita
                no.esq = self._rotacao_esquerda(no.esq)
            return self._rotacao_direita(no)

        # Pesado à direita
        if fator < -1:
            if self.fator_balanceamento(no.dir) > 0:
                # Rotação dupla Direita-Esquerda
                no.dir = self._rotacao_direita(no.dir)
            return self._rotacao_esquerda(no)

        return no

    def melhor(self) -> Ordem | None:
        """Retorna a ordem de menor chave (nó mais à esquerda)."""
        if self.raiz is None:
            return None
        atual = self.raiz
        while atual.esq is not None:
            atual = atual.esq
        return atual.ordem

    def buscar(self, chave: tuple[int, int]) -> Ordem | None:
        atual = self.raiz
        while atual is not None:
            if chave == atual.chave:
                return atual.ordem
            elif chave < atual.chave:
                atual = atual.esq
            else:
                atual = atual.dir
        return None

    def inserir(self, ordem: Ordem) -> None:
        """Insere uma ordem e rebalanceia os ancestrais no retorno da recursão."""
        self.raiz, inseriu = self._inserir_rec(self.raiz, ordem)
        if inseriu:
            self._tamanho += 1

    def _inserir_rec(self, no: NoAVL | None, ordem: Ordem) -> tuple[NoAVL, bool]:
        if no is None:
            return NoAVL(ordem), True

        if ordem.chave < no.chave:
            no.esq, inseriu = self._inserir_rec(no.esq, ordem)
        elif ordem.chave > no.chave:
            no.dir, inseriu = self._inserir_rec(no.dir, ordem)
        else:
            no.ordem = ordem
            return no, False

        return self._rebalancear(no), inseriu

    def remover(self, ordem: Ordem) -> bool:
        """Remove uma ordem por chave e rebalanceia até a raiz."""
        self.raiz, removeu = self._remover_rec(self.raiz, ordem.chave)
        if removeu:
            self._tamanho -= 1
        return removeu

    def _remover_rec(
        self, no: NoAVL | None, chave: tuple[int, int]
    ) -> tuple[NoAVL | None, bool]:
        if no is None:
            return None, False

        if chave < no.chave:
            no.esq, removeu = self._remover_rec(no.esq, chave)
        elif chave > no.chave:
            no.dir, removeu = self._remover_rec(no.dir, chave)
        else:
            # Nó encontrado: 0 ou 1 filho
            if no.esq is None:
                return no.dir, True
            if no.dir is None:
                return no.esq, True

            # 2 filhos: busca o sucessor (menor da subárvore direita)
            sucessor = no.dir
            while sucessor.esq is not None:
                sucessor = sucessor.esq

            no.chave = sucessor.chave
            no.ordem = sucessor.ordem
            no.dir, _ = self._remover_rec(no.dir, sucessor.chave)
            removeu = True

        if not removeu:
            return no, False

        return self._rebalancear(no), True

    def em_ordem(self) -> list[Ordem]:
        resultado = []
        self._em_ordem_rec(self.raiz, resultado)
        return resultado

    def _em_ordem_rec(self, no: NoAVL | None, acc: list[Ordem]) -> None:
        if no is not None:
            self._em_ordem_rec(no.esq, acc)
            acc.append(no.ordem)
            self._em_ordem_rec(no.dir, acc)