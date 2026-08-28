# Financial Assistant API

Assistente financeiro que responde perguntas em linguagem natural
(ex: *"quanto gastei em mercado esse mês?"*) consultando um banco de
transações. A pergunta é convertida em uma query SQL por um LLM
(Claude), executada no banco, e o resultado é retornado pela API.

## Por que esse projeto

Este projeto foi feito para demonstrar três habilidades ao mesmo
tempo: lógica de programação em Python, uso de SQL/banco de dados, e
uso prático de uma API de IA para resolver um problema real — três
pontos centrais em vagas de tecnologia e dados.

## Stack

- **Python 3.11+**
- **FastAPI** — framework para os endpoints da API
- **SQLite** — banco de dados leve, sem necessidade de servidor
- **Pandas** — leitura e tratamento do CSV de transações
- **Anthropic API (Claude)** — conversão de linguagem natural em SQL

## Estrutura do projeto

```
financial-assistant/
├── app/
│   ├── main.py          # FastAPI app e endpoint /ask
│   ├── database.py      # conexão e execução segura de queries no SQLite
│   ├── models.py        # schema da tabela e modelos Pydantic
│   ├── llm_service.py   # chamada à API da Anthropic
│   └── import_data.py   # script que carrega o CSV no banco
├── data/
│   └── transactions.csv # dados de exemplo
├── tests/
│   └── test_endpoints.py
├── requirements.txt
└── README.md
```

## Como rodar

1. Clone o repositório e entre na pasta:

```bash
git clone <seu-repositorio>
cd financial-assistant
```

2. Crie um ambiente virtual e instale as dependências:

```bash
python -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure sua chave da API da Anthropic:

```bash
export ANTHROPIC_API_KEY="sua-chave-aqui"
```

4. Importe os dados de exemplo para o banco:

```bash
python -m app.import_data
```

5. Suba a API:

```bash
uvicorn app.main:app --reload
```

6. Teste o endpoint (com a API rodando em outro terminal):

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "quanto eu gastei em mercado?"}'
```

## Rodando os testes

```bash
pytest
```

## Decisões técnicas

- **Somente queries SELECT são permitidas.** Como a query SQL é
  gerada por um LLM a partir de texto livre, existe risco do modelo
  gerar comandos destrutivos (`DROP`, `DELETE`, `UPDATE`). Por isso,
  `database.py` valida que toda query começa com `SELECT` antes de
  executá-la.
- **SQLite ao invés de Postgres/MySQL** — escolhido para manter o
  projeto simples de rodar localmente sem depender de infraestrutura
  externa, já que o foco aqui é a lógica de negócio, não a operação
  de um banco de produção.
- **Separação em módulos** (`database.py`, `llm_service.py`,
  `models.py`) ao invés de um único arquivo — facilita testes
  isolados e deixa claro onde cada responsabilidade vive.

## Possíveis melhorias futuras

- Autenticação simples (API key ou JWT) no endpoint `/ask`
- Cache de perguntas repetidas para economizar chamadas ao LLM
- Suporte a mais de uma tabela (ex: separar receitas e despesas)
- Endpoint para categorização automática de novas transações usando IA
