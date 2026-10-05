================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask 3.1.1
Files:   4 analyzed | ~900 lines of code
Domain:  E-commerce API (produtos, pedidos, usuários)

## Summary
CRITICAL: 5 | HIGH: 2 | MEDIUM: 2 | LOW: 2

## Findings

### [CRITICAL] SQL Injection / Query String Concatenation
File: models.py:28-50, models.py:109-111, models.py:285-299
Description: Queries montadas por concatenação de strings com input do usuário (`"WHERE id = " + str(id)`, INSERT com nome/email/senha concatenados, busca com LIKE concatenado). Endpoint `/admin/query` em app.py:59-78 executa SQL arbitrário do body.
Impact: Comprometimento total do banco (leitura/escrita/drop).
Recommendation: Parameterized queries (`?`) em todos os Models; remover endpoint de SQL livre.

### [CRITICAL] Hardcoded Secrets / Credentials
File: app.py:7
Description: `SECRET_KEY = "minha-chave-super-secreta-123"` hardcoded no código-fonte.
Impact: Chave previsível permite forjar sessões/tokens se usada em produção.
Recommendation: Extrair para `config/settings.py` + variável de ambiente `SECRET_KEY`.

### [CRITICAL] Sensitive Data Leakage in Responses
File: controllers.py:276-289, models.py:72-87
Description: `health_check` retorna `secret_key`, path do DB e flag debug. `get_todos_usuarios` inclui campo `senha` em plaintext na resposta JSON.
Impact: Vazamento de segredos e credenciais via API pública.
Recommendation: Serializer sem senha; health mínimo sem secrets.

### [CRITICAL] Plaintext Password Storage
File: models.py:105-120, database.py:75-82
Description: Senhas armazenadas e comparadas em plaintext (`senha = '" + senha + "'`).
Impact: Em caso de vazamento do banco, todas as contas são comprometidas.
Recommendation: Hash com `werkzeug.security.generate_password_hash` / `check_password_hash`.

### [CRITICAL] God Class / God Module
File: models.py:1-314
Description: Arquivo único concentra queries e regras de negócio de produtos, usuários, pedidos e relatórios (~314 linhas, 4 domínios).
Impact: Impossível testar em isolamento; qualquer mudança afeta múltiplos domínios.
Recommendation: Separar em `produto_model`, `usuario_model`, `pedido_model` + controllers por domínio.

### [HIGH] Fat Controller / Business Logic in Routes
File: controllers.py:24-62, controllers.py:188-220
Description: Controllers concentram validação detalhada, side-effects de notificação (prints de email/SMS/push) e acesso direto a `get_db` no health.
Impact: Acoplamento ao HTTP; regras não reutilizáveis.
Recommendation: Mover orquestração limpa para controllers MVC; validação compartilhada; routes finas.

### [HIGH] Mutable Global State
File: database.py:4-10
Description: `db_connection = None` global compartilhado entre requests com `check_same_thread=False`.
Impact: Estado global dificulta testes e pode gerar condições de corrida.
Recommendation: Inicialização explícita no composition root via factory/`init_db`.

### [MEDIUM] N+1 Query Pattern
File: models.py:171-201, models.py:203-233
Description: Para cada pedido, abre cursor e busca itens; para cada item, busca nome do produto — 1 + N + M queries.
Impact: Latência cresce com volume de pedidos/itens.
Recommendation: JOIN único agregando pedidos + itens + produtos.

### [MEDIUM] Missing Validation / Insecure Endpoints
File: app.py:47-78
Description: `/admin/reset-db` e `/admin/query` sem autenticação; permitem apagar todo o banco ou executar SQL arbitrário.
Impact: Destruição de dados e RCE via SQL por qualquer cliente.
Recommendation: Remover endpoints ou proteger com auth forte.

### [LOW] Magic Numbers
File: models.py:256-262
Description: Faixas de desconto `10000/0.1`, `5000/0.05`, `1000/0.02` sem constantes nomeadas.
Impact: Manutenção difícil; risco de alterar literal errado.
Recommendation: Constantes em `config/settings.py` (`DESCONTO_TIER_*`).

### [LOW] Poor Logging / String Concatenation
File: controllers.py:8, controllers.py:57
Description: Logs via `"Listando " + str(len(produtos))` em vez de f-strings; prints de debug espalhados.
Impact: Legibilidade e padronização de logs.
Recommendation: Logging estruturado / f-strings; remover prints de produção.

## Deprecated APIs
| Local | API deprecated | Equivalente moderno |
|---|---|---|
| models.py:105-120 | Comparação de senha em plaintext | `werkzeug.security.check_password_hash` |
| (N/A explícito datetime) | — | — |

## Proposed MVC Target Structure
```
src/
├── config/settings.py
├── models/
│   ├── produto_model.py
│   ├── usuario_model.py
│   └── pedido_model.py
├── controllers/
│   ├── produto_controller.py
│   ├── usuario_controller.py
│   ├── pedido_controller.py
│   └── health_controller.py
├── views/routes.py
├── middlewares/error_handler.py
├── database.py
└── app.py
app.py  # entry point
```

## Refactoring Plan (Phase 3 preview)
1. Extrair config e remover secrets hardcoded
2. Criar models com queries parametrizadas e hash de senha
3. Criar controllers por domínio; views apenas roteando
4. Remover endpoints admin inseguros
5. Corrigir N+1 com JOINs; serializers sem senha
6. Validar boot + endpoints

================================
Total: 11 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y (confirmado pelo usuário na execução do desafio)
