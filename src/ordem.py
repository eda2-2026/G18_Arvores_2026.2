class Ordem:
    """Representa uma ordem limite de compra ou venda no livro de ofertas."""

    def __init__(self, id_ordem: int, lado: str, preco: int, qtd: int, seq: int):
        if lado not in ("C", "V"):
            raise ValueError("O lado da ordem deve ser 'C' (compra) ou 'V' (venda).")
        if preco <= 0 or qtd <= 0:
            raise ValueError("Preço e quantidade devem ser inteiros positivos.")

        self.id = id_ordem
        self.lado = lado      # 'C' para Compra, 'V' para Venda
        self.preco = preco    # Inteiro em centavos
        self.qtd = qtd        # Quantidade de ativos
        self.seq = seq        # Sequencial de chegada para desempate (FIFO)

    @property
    def chave(self) -> tuple[int, int]:
        """
        Retorna a chave de prioridade da ordem.
        Compra: (-preco, seq) -> maior preço tem menor chave numérica.
        Venda:  (preco, seq)  -> menor preço tem menor chave numérica.
        Em ambos os casos, a menor chave representa a melhor oferta.
        """
        if self.lado == "C":
            return (-self.preco, self.seq)
        return (self.preco, self.seq)

    def __repr__(self) -> str:
        return (
            f"Ordem(id={self.id}, lado='{self.lado}', "
            f"preco={self.preco}, qtd={self.qtd}, seq={self.seq})"
        )