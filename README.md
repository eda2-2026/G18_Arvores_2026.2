# G18_Arvores_2026.2 — Livro de Ofertas

## Alunos
| Matrícula | Nome |
| --------- | ---- |
| 232001380 | Caio Vilas Boas Miranda |
| 232021516 | Guilherme Gusmão Nepomuceno |

## Vídeo de apresentação
[Link a ser adicionado]

## Descrição
Implementação de um Livro de Ofertas para ingressos, comparando o desempenho de **Min-Heap**, **BST iterativa**, **AVL** e **Rubro-Negra**.

**Regras do Livro:**
- O preço é um número inteiro em centavos.
- A melhor oferta é sempre a que tem o preço mais alto (na compra) ou mais baixo (na venda). Em caso de empate, vence a ordem mais antiga (FIFO).
- O casamento (trade) ocorre quando uma ordem nova cobre o preço da melhor oferta oposta.
- O preço do negócio é sempre ditado pelo preço da ordem que já estava descansando no livro.

## Estrutura do repositório
* **`src/`**: Algoritmos de árvore (`heap.py`, `bst.py`, `avl.py`, `rubro_negra.py`), regras de negócio (`ordem.py`, `livro.py`), gerador sintético (`gerador.py`) e CLI (`main.py`).
* **`tests/`**: Suíte de testes (`pytest`) validando propriedades de árvore, remoções e com um livro Gabarito (baseado em listas simples) assegurando os trades gerados.
* **`benchmark/`**: Script dos experimentos E1 a E4.

## Como executar

**1. Instalar dependências:**
```bash
pip install -r requirements.txt
```
**2. Rodar os testes:**

```bash
pytest -v
```

**3. Rodar a CLI (Demo):**

```bash
python3 src/main.py --estrutura rn --carga B --pre 200 --eventos 1000 --seed 42
```

**4. Rodar o Benchmark:**

```bash
python3 benchmark/benchmark.py
```

## Resultados do Benchmark
> **Ambiente:** Python 3.14.4 (CPython) | Linux 7.0.0-43-generic (x86_64)

*(Rode `python3 benchmark/benchmark.py` e cole as 4 tabelas geradas aqui)*

### Conclusões a partir dos números:

**E1: Tempo de Cancelamento**
Com 20.000 ordens, 1.000 cancelamentos arbitrários levaram 3,4 segundos no Heap simples (≈3,4 ms cada), contra ≈25 ms na AVL e ≈9 ms na Rubro-Negra. O tempo do Heap cresce proporcionalmente a $N$ pela busca linear, enquanto a AVL e a RN resolvem o cancelamento em tempo quase constante ($O(\log n)$) nessa faixa. A Rubro-Negra foi a mais rápida neste ambiente; no entanto, o E1 mede apenas o tempo total e não isola a causa exata dessa diferença.

**E2: Degeneração (Carga D)**
A BST sofre degeneração estrutural total e vira uma lista encadeada (altura = $N$). AVL e RN mantêm o equilíbrio e resolvem o fluxo crescente em milissegundos.

**E3: Inserção + 50% de Remoção (AVL vs Rubro-Negra)**
Com 100.000 nós e remoção aleatória, a AVL fez ~15% mais rotações estruturais que a RN (88.421 contra 76.691). Contudo, a Rubro-Negra foi ~3,4 vezes mais rápida. A economia mecânica de rotações é muito pequena para explicar tamanho ganho de tempo, o que indica que a diferença advém majoritariamente da implementação (a AVL utiliza um estilo recursivo e recalcula alturas em cada retorno).

**E4: Livro Completo (Cargas A, B e C)**
A Rubro-Negra apresentou a melhor performance geral neste ambiente. O Heap simples tem bom rendimento na leitura da Carga A, mas degrada severamente conforme a taxa de cancelamento sobe (Cargas B e C). Um detalhe evidenciado pelos números é que a Carga C sofre tantos cancelamentos (quase 40% efetivos) que termina a execução com o livro vazio, não medindo portanto as estruturas sob "alta carga", mas sim sob rápido esvaziamento.

## Limitações
1. O cancelamento de ordens que já foram removidas ou executadas gera um `False` passivo, mas na contagem de eventos, a "tentativa" ainda foi cobrada como um evento dinâmico.
2. A Carga C (60% de prob. de cancelamento) esvazia o livro quase por completo durante a medição.
3. As estruturas dependem da performance subjacente de dicionários e objetos do CPython, não sendo refletidas abstrações de baixo nível de memória (C/C++).
4. Todas as simulações e o ranking das estruturas estão condicionados às características de hardware e sistema operacional de uma única máquina (x86_64, Linux).
5. O Heap não possui dicionário de índices associado em memória, forçando busca $O(n)$ no cancelamento.

## Contribuições
* **Caio Miranda:** Responsável pela implementação e testes das estruturas `Ordem`, `MinHeap` e `Rubro-Negra` (com sentinela NIL). Escrita dos testes unitários e implementação dos experimentos E1 e E2 no Benchmark.
* **Guilherme Nepomuceno:** Responsável pela implementação e testes das estruturas `BST` iterativa e `AVL`. Montagem do motor `LivroDeOfertas`, gerador sintético, CLI interativa (`main.py`) e desenvolvimento dos experimentos E3 e E4 no Benchmark.