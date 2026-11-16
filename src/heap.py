from src.ordem import Ordem


class MinHeap:
    """Min-Heap próprio baseado em lista (sem usar heapq)."""

    def __init__(self):
        self.dados: list[Ordem] = []

    def __len__(self) -> int:
        return len(self.dados)

    def melhor(self) -> Ordem | None:
        """Retorna a ordem de menor chave (raiz) sem removê-la."""
        if not self.dados:
            return None
        return self.dados[0]

    def inserir(self, ordem: Ordem) -> None:
        """Insere no final da lista e sobe o elemento até restaurar o heap."""
        self.dados.append(ordem)
        self._sift_up(len(self.dados) - 1)

    def remover_raiz(self) -> Ordem | None:
        """Remove e retorna a raiz (menor chave) em O(log n)."""
        if not self.dados:
            return None
        if len(self.dados) == 1:
            return self.dados.pop()

        raiz = self.dados[0]
        # Coloca o último na raiz e desce (sift-down)
        self.dados[0] = self.dados.pop()
        self._sift_down(0)
        return raiz

    def remover(self, ordem: Ordem) -> bool:
        """
        Remove uma ordem qualquer.
        Se estiver na raiz (caso do casamento total), faz em O(log n).
        Se for cancelamento arbitrário, faz busca linear O(n) + ajuste O(log n).
        """
        if not self.dados:
            return False

        # Atalho rápido se for exatamente a raiz
        if self.dados[0].id == ordem.id:
            self.remover_raiz()
            return True

        # Busca linear O(n) pela posição da ordem
        idx = -1
        for i, item in enumerate(self.dados):
            if item.id == ordem.id:
                idx = i
                break

        if idx == -1:
            return False

        ultimo = self.dados.pop()
        # Se o elemento removido não era o último da lista, substitui e corrige
        if idx < len(self.dados):
            self.dados[idx] = ultimo
            # Um dos dois fará o trabalho, o outro sairá imediatamente
            self._sift_up(idx)
            self._sift_down(idx)

        return True

    def _sift_up(self, idx: int) -> None:
        """Sobe o elemento no índice `idx` enquanto a chave for menor que a do pai."""
        while idx > 0:
            pai = (idx - 1) // 2
            if self.dados[idx].chave < self.dados[pai].chave:
                self.dados[idx], self.dados[pai] = self.dados[pai], self.dados[idx]
                idx = pai
            else:
                break

    def _sift_down(self, idx: int) -> None:
        """Desce o elemento no índice `idx` trocando pelo menor dos filhos."""
        n = len(self.dados)
        while True:
            menor = idx
            esq = 2 * idx + 1
            dir_ = 2 * idx + 2

            if esq < n and self.dados[esq].chave < self.dados[menor].chave:
                menor = esq
            if dir_ < n and self.dados[dir_].chave < self.dados[menor].chave:
                menor = dir_

            if menor != idx:
                self.dados[idx], self.dados[menor] = self.dados[menor], self.dados[idx]
                idx = menor
            else:
                break