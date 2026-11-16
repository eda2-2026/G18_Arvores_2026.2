from collections import deque
from src.ordem import Ordem


class NoBST:
    """Nó da Árvore Binária de Busca (BST)."""

    def __init__(self, ordem: Ordem):
        self.chave = ordem.chave
        self.ordem = ordem
        self.esq: NoBST | None = None
        self.dir: NoBST | None = None


class BST:
    """Árvore Binária de Busca sem balanceamento (100% iterativa)."""

    def __init__(self):
        self.raiz: NoBST | None = None
        self._tamanho: int = 0

    def __len__(self) -> int:
        return self._tamanho

    def buscar(self, chave: tuple[int, int]) -> Ordem | None:
        """Busca iterativa por uma chave."""
        atual = self.raiz
        while atual is not None:
            if chave == atual.chave:
                return atual.ordem
            elif chave < atual.chave:
                atual = atual.esq
            else:
                atual = atual.dir
        return None

    def melhor(self) -> Ordem | None:
        """Retorna a ordem de menor chave (nó mais à esquerda) de forma iterativa."""
        if self.raiz is None:
            return None
        atual = self.raiz
        while atual.esq is not None:
            atual = atual.esq
        return atual.ordem

    def inserir(self, ordem: Ordem) -> None:
        """Inserção iterativa na BST."""
        novo = NoBST(ordem)
        if self.raiz is None:
            self.raiz = novo
            self._tamanho += 1
            return

        atual = self.raiz
        pai = None
        while atual is not None:
            pai = atual
            if novo.chave < atual.chave:
                atual = atual.esq
            elif novo.chave > atual.chave:
                atual = atual.dir
            else:
                # Atualiza caso a mesma chave seja inserida
                atual.ordem = ordem
                return

        if novo.chave < pai.chave:
            pai.esq = novo
        else:
            pai.dir = novo
        self._tamanho += 1

    def remover(self, ordem: Ordem) -> bool:
        """
        Remoção iterativa com os 3 casos:
        1. Folha
        2. Um filho
        3. Dois filhos (substitui pelos dados do sucessor em-ordem)
        """
        chave = ordem.chave
        atual = self.raiz
        pai = None

        # 1. Localiza o nó a remover e seu pai
        while atual is not None and atual.chave != chave:
            pai = atual
            if chave < atual.chave:
                atual = atual.esq
            else:
                atual = atual.dir

        if atual is None:
            return False

        # 2. Caso com 2 filhos: reduz para o caso de 0 ou 1 filho
        # achando o sucessor em-ordem (menor da subárvore direita)
        if atual.esq is not None and atual.dir is not None:
            pai_suc = atual
            suc = atual.dir
            while suc.esq is not None:
                pai_suc = suc
                suc = suc.esq

            # Copia os dados do sucessor para o nó atual
            atual.chave = suc.chave
            atual.ordem = suc.ordem

            # Agora o alvo real de remoção passa a ser o sucessor
            atual = suc
            pai = pai_suc

        # 3. Caso com 0 ou 1 filho
        filho = atual.esq if atual.esq is not None else atual.dir

        if pai is None:
            self.raiz = filho
        elif pai.esq == atual:
            pai.esq = filho
        else:
            pai.dir = filho

        self._tamanho -= 1
        return True

    def altura(self) -> int:
        """Calcula a altura da árvore iterativamente (via BFS) para não estourar pilha."""
        if self.raiz is None:
            return 0
        fila = deque([(self.raiz, 1)])
        max_alt = 0
        while fila:
            no, alt = fila.popleft()
            if alt > max_alt:
                max_alt = alt
            if no.esq is not None:
                fila.append((no.esq, alt + 1))
            if no.dir is not None:
                fila.append((no.dir, alt + 1))
        return max_alt

    def em_ordem(self) -> list[Ordem]:
        """Percorre a árvore em-ordem iterativamente (pilha explícita)."""
        resultado = []
        pilha = []
        atual = self.raiz
        while pilha or atual is not None:
            while atual is not None:
                pilha.append(atual)
                atual = atual.esq
            atual = pilha.pop()
            resultado.append(atual.ordem)
            atual = atual.dir
        return resultado