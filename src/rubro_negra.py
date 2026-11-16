from src.ordem import Ordem

VERMELHO = True
PRETO = False


class NoRN:
    """Nó da Árvore Rubro-Negra."""

    def __init__(
        self,
        ordem: Ordem | None,
        cor: bool = VERMELHO,
        nil: "NoRN | None" = None,
    ):
        self.ordem = ordem
        self.chave = ordem.chave if ordem is not None else None
        self.cor = cor
        self.esq: NoRN = nil if nil is not None else self
        self.dir: NoRN = nil if nil is not None else self
        self.pai: NoRN = nil if nil is not None else self


class RubroNegra:
    """Árvore Rubro-Negra com nó sentinela único (CLRS) e contador de rotações."""

    def __init__(self):
        # Sentinela único NIL (sempre PRETO)
        self.NIL = NoRN(None, cor=PRETO)
        self.NIL.esq = self.NIL
        self.NIL.dir = self.NIL
        self.NIL.pai = self.NIL

        self.raiz: NoRN = self.NIL
        self._tamanho: int = 0
        self.rotacoes: int = 0

    def __len__(self) -> int:
        return self._tamanho

    def melhor(self) -> Ordem | None:
        """Retorna a ordem de menor chave (nó mais à esquerda)."""
        if self.raiz == self.NIL:
            return None
        atual = self.raiz
        while atual.esq != self.NIL:
            atual = atual.esq
        return atual.ordem

    def buscar(self, chave: tuple[int, int]) -> Ordem | None:
        no = self._buscar_no(chave)
        return no.ordem if no != self.NIL else None

    def _buscar_no(self, chave: tuple[int, int]) -> NoRN:
        atual = self.raiz
        while atual != self.NIL:
            if chave == atual.chave:
                return atual
            elif chave < atual.chave:
                atual = atual.esq
            else:
                atual = atual.dir
        return self.NIL

    def _rotacao_esquerda(self, x: NoRN) -> None:
        """Rotação à esquerda atualizando ponteiros de pai."""
        self.rotacoes += 1
        y = x.dir
        x.dir = y.esq
        if y.esq != self.NIL:
            y.esq.pai = x

        y.pai = x.pai
        if x.pai == self.NIL:
            self.raiz = y
        elif x == x.pai.esq:
            x.pai.esq = y
        else:
            x.pai.dir = y

        y.esq = x
        x.pai = y

    def _rotacao_direita(self, y: NoRN) -> None:
        """Rotação à direita atualizando ponteiros de pai."""
        self.rotacoes += 1
        x = y.esq
        y.esq = x.dir
        if x.dir != self.NIL:
            x.dir.pai = y

        x.pai = y.pai
        if y.pai == self.NIL:
            self.raiz = x
        elif y == y.pai.dir:
            y.pai.dir = x
        else:
            y.pai.esq = x

        x.dir = y
        y.pai = x

    def inserir(self, ordem: Ordem) -> None:
        """Insere novo nó VERMELHO como na BST e corrige violações."""
        z = NoRN(ordem, cor=VERMELHO, nil=self.NIL)
        y = self.NIL
        x = self.raiz

        while x != self.NIL:
            y = x
            if z.chave < x.chave:
                x = x.esq
            elif z.chave > x.chave:
                x = x.dir
            else:
                x.ordem = ordem
                return

        z.pai = y
        if y == self.NIL:
            self.raiz = z
        elif z.chave < y.chave:
            y.esq = z
        else:
            y.dir = z

        self._tamanho += 1
        self._consertar_insercao(z)

    def _consertar_insercao(self, z: NoRN) -> None:
        """Sobe na árvore corrigindo conflitos Vermelho-Vermelho."""
        while z.pai.cor == VERMELHO:
            if z.pai == z.pai.pai.esq:
                tio = z.pai.pai.dir
                if tio.cor == VERMELHO:
                    # Caso 1: Tio é vermelho -> recolorir pai, tio e avô
                    z.pai.cor = PRETO
                    tio.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    z = z.pai.pai
                else:
                    if z == z.pai.dir:
                        # Caso 2: Tio preto e z é filho "de dentro" -> rotação no pai
                        z = z.pai
                        self._rotacao_esquerda(z)
                    # Caso 3: Tio preto e z é filho "de fora" -> rotação no avô
                    z.pai.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    self._rotacao_direita(z.pai.pai)
            else:
                # Espelho: pai é filho direito do avô
                tio = z.pai.pai.esq
                if tio.cor == VERMELHO:
                    z.pai.cor = PRETO
                    tio.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    z = z.pai.pai
                else:
                    if z == z.pai.esq:
                        z = z.pai
                        self._rotacao_direita(z)
                    z.pai.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    self._rotacao_esquerda(z.pai.pai)

        self.raiz.cor = PRETO

    def _transplantar(self, u: NoRN, v: NoRN) -> None:
        """Substitui a subárvore enraizada em u pela subárvore enraizada em v."""
        if u.pai == self.NIL:
            self.raiz = v
        elif u == u.pai.esq:
            u.pai.esq = v
        else:
            u.pai.dir = v
        v.pai = u.pai

    def _minimo(self, no: NoRN) -> NoRN:
        while no.esq != self.NIL:
            no = no.esq
        return no

    def remover(self, ordem: Ordem) -> bool:
        """Remove o nó pela chave e conserta o 'preto duplo' se um nó preto saiu."""
        z = self._buscar_no(ordem.chave)
        if z == self.NIL:
            return False

        y = z
        cor_original_y = y.cor

        if z.esq == self.NIL:
            x = z.dir
            self._transplantar(z, z.dir)
        elif z.dir == self.NIL:
            x = z.esq
            self._transplantar(z, z.esq)
        else:
            y = self._minimo(z.dir)
            cor_original_y = y.cor
            x = y.dir
            if y.pai == z:
                x.pai = y
            else:
                self._transplantar(y, y.dir)
                y.dir = z.dir
                y.dir.pai = y
            self._transplantar(z, y)
            y.esq = z.esq
            y.esq.pai = y
            y.cor = z.cor

        self._tamanho -= 1
        if cor_original_y == PRETO:
            self._consertar_remocao(x)

        return True

    def _consertar_remocao(self, x: NoRN) -> None:
        """Conserta o 'preto duplo' analisando os 4 casos do irmão w (CLRS)."""
        while x != self.raiz and x.cor == PRETO:
            if x == x.pai.esq:
                w = x.pai.dir
                if w.cor == VERMELHO:
                    # Caso 1: Irmão w é vermelho
                    w.cor = PRETO
                    x.pai.cor = VERMELHO
                    self._rotacao_esquerda(x.pai)
                    w = x.pai.dir

                if w.esq.cor == PRETO and w.dir.cor == PRETO:
                    # Caso 2: Irmão w é preto e seus dois filhos são pretos
                    w.cor = VERMELHO
                    x = x.pai
                else:
                    if w.dir.cor == PRETO:
                        # Caso 3: Irmão w é preto, filho esq vermelho, dir preto
                        w.esq.cor = PRETO
                        w.cor = VERMELHO
                        self._rotacao_direita(w)
                        w = x.pai.dir
                    # Caso 4: Irmão w é preto e filho direito é vermelho
                    w.cor = x.pai.cor
                    x.pai.cor = PRETO
                    w.dir.cor = PRETO
                    self._rotacao_esquerda(x.pai)
                    x = self.raiz
            else:
                # Espelho: x é filho direito
                w = x.pai.esq
                if w.cor == VERMELHO:
                    w.cor = PRETO
                    x.pai.cor = VERMELHO
                    self._rotacao_direita(x.pai)
                    w = x.pai.esq

                if w.dir.cor == PRETO and w.esq.cor == PRETO:
                    w.cor = VERMELHO
                    x = x.pai
                else:
                    if w.esq.cor == PRETO:
                        w.dir.cor = PRETO
                        w.cor = VERMELHO
                        self._rotacao_esquerda(w)
                        w = x.pai.esq
                    w.cor = x.pai.cor
                    x.pai.cor = PRETO
                    w.esq.cor = PRETO
                    self._rotacao_direita(x.pai)
                    x = self.raiz

        x.cor = PRETO
        self.NIL.cor = PRETO

    def altura(self) -> int:
        return self._altura_rec(self.raiz)

    def _altura_rec(self, no: NoRN) -> int:
        if no == self.NIL:
            return 0
        return 1 + max(self._altura_rec(no.esq), self._altura_rec(no.dir))

    def em_ordem(self) -> list[Ordem]:
        resultado = []
        self._em_ordem_rec(self.raiz, resultado)
        return resultado

    def _em_ordem_rec(self, no: NoRN, acc: list[Ordem]) -> None:
        if no != self.NIL:
            self._em_ordem_rec(no.esq, acc)
            acc.append(no.ordem)
            self._em_ordem_rec(no.dir, acc)