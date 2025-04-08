# Backend Tudo Fresco

Este é o backend do projeto **Tudo Fresco**, responsável por gerenciar requisições de API, interações com o banco de dados e a lógica de negócios do sistema de gerenciamento de alimentos orgânicos.

## Configuração Inicial

Para configurar o ambiente de desenvolvimento:

1. **Clone o repositório**
   ```bash
   git clone git@github.com:Tudo-Fresco/backend.git
   cd tudo-fresco-backend
   ```

2. **Instale as dependências com Poetry**
   ```bash
   poetry install
   ```

3. **Ative o ambiente virtual**
   ```bash
   poetry shell
   ```

## Rodando a Aplicação

Para iniciar o servidor localmente:

```bash
poetry run python main.py
```

A API estará disponível em [http://localhost:5000](http://localhost:5000) (confirme a porta no código, se necessário).

## Testes

Os testes unitários são executados com `pytest`. Use os comandos abaixo:

### Rodar testes com cobertura:
```bash
poetry run pytest --cov=tests
```

### Gerar relatório de cobertura em HTML:
```bash
poetry run pytest --cov=app --cov-report=html
```

Para visualizar o relatório, abra o arquivo `htmlcov/index.html` no navegador.

## Comandos Básicos do Poetry

- **Instalar dependências**: `poetry install`
- **Ativar ambiente virtual**: `poetry shell`
- **Executar comandos no ambiente**: `poetry run <comando>`
- **Adicionar uma nova dependência**: `poetry add <pacote>`
- **Atualizar dependências**: `poetry update`

## Notas

Certifique-se de configurar variáveis de ambiente em um arquivo `.env`, se necessário.

## Criar um Migration nova do banco
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head