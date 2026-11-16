import os
import sys
import pytest

# Adiciona a raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ordem import Ordem


@pytest.fixture
def fabrica_ordem():
    """Fixture auxiliar para criar ordens rapidamente nos testes."""
    seq_counter = 0

    def _criar(id_ordem: int, lado: str = "C", preco: int = 1000, qtd: int = 10, seq: int | None = None) -> Ordem:
        nonlocal seq_counter
        seq_counter += 1
        s = seq if seq is not None else seq_counter
        return Ordem(id_ordem, lado, preco, qtd, s)

    return _criar