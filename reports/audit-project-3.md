================================
ARCHITECTURE AUDIT REPORT
================================
Project: task-manager-api
Stack:   Python + Flask 3.0.0 (+ Flask-SQLAlchemy)
Files:   14 analyzed | ~1100 lines of code
Domain:  Task Manager API (tasks, users, categories, reports)

## Summary
CRITICAL: 2 | HIGH: 3 | MEDIUM: 3 | LOW: 2

## Findings

### [CRITICAL] Sensitive Data Leakage in Responses
File: models/user.py:16-25
Description: `to_dict()` inclui o campo `password` (hash) na serialização; login e create/update retornam o usuário via `to_dict()`.
Impact: Hash de senha exposto via API; facilita ataques offline.
Recommendation: Remover `password` do serializer público.

### [CRITICAL] Hardcoded Secrets / Credentials
File: app.py:13, services/notification_service.py:7-10
Description: `SECRET_KEY = 'super-secret-key-123'` e credenciais SMTP (`taskmanager@gmail.com` / `senha123`) hardcoded.
Impact: Segredos no repositório; risco de abuso do e-mail e da app.
Recommendation: Extrair para `config/settings.py` + env vars.

### [HIGH] Weak / Deprecated Cryptography
File: models/user.py:27-32
Description: Senhas hasheadas com `hashlib.md5` — algoritmo criptograficamente quebrado para senhas.
Impact: Senhas recuperáveis com rainbow tables.
Recommendation: `werkzeug.security.generate_password_hash` / `check_password_hash`.

### [HIGH] Fat Controller / Business Logic in Routes
File: routes/task_routes.py:1-299, routes/user_routes.py, routes/report_routes.py
Description: Blueprints concentram validação, queries, regras de overdue e serialização — sem camada Controller.
Impact: Rotas inchadas; difícil testar regras sem HTTP.
Recommendation: Introduzir `controllers/` e deixar routes como binding fino.

### [HIGH] Deprecated API — datetime.utcnow
File: models/task.py:15-16, models/user.py:14, seed.py, routes/task_routes.py:31
Description: Uso extensivo de `datetime.utcnow()` (deprecated desde Python 3.12).
Impact: Warnings e futura remoção da API.
Recommendation: `datetime.now(timezone.utc)` via helper `utcnow()`.

### [MEDIUM] N+1 Query Pattern
File: routes/task_routes.py:41-57
Description: Em `get_tasks`, para cada task faz `User.query.get` e `Category.query.get`.
Impact: 1 + 2N queries na listagem.
Recommendation: `joinedload(Task.user)` e `joinedload(Task.category)`.

### [MEDIUM] Code Duplication
File: routes/task_routes.py:30-39, routes/user_routes.py:171-180, models/task.py:50-60
Description: Lógica de `overdue` duplicada em listagem, detalhe, user tasks e model.
Impact: Drift de comportamento entre endpoints.
Recommendation: Centralizar em `Task.is_overdue()` e reutilizar em `to_dict()`.

### [MEDIUM] Deprecated API — Query.get
File: routes/task_routes.py:67, routes/user_routes.py:29
Description: `Model.query.get()` é legado no SQLAlchemy 2.x.
Impact: Warnings de depreciação; incompatibilidade futura.
Recommendation: `db.session.get(Model, id)`.

### [LOW] Unused Imports / Dead Code Smell
File: routes/task_routes.py:7, app.py:7, utils/helpers.py:57-108
Description: Imports não usados (`os, sys, time`, `json` em app); `process_task_data` definido mas não referenciado pelas routes.
Impact: Ruído e falsa sensação de utilidade.
Recommendation: Limpar imports; usar helper ou documentar como util compartilhado.

### [LOW] Magic Numbers / Scattered Constants
File: utils/helpers.py:110-116 vs routes duplicando literais 3/200/1-5
Description: Constantes definidas em helpers mas routes usam literais mágicos.
Impact: Divergência de regras de validação.
Recommendation: Fonte única em `config/settings.py`.

## Deprecated APIs
| Local | API deprecated | Equivalente moderno |
|---|---|---|
| models/user.py:29 | `hashlib.md5` para senhas | `werkzeug.security.generate_password_hash` |
| models/task.py:15 | `datetime.utcnow()` | `datetime.now(timezone.utc)` |
| routes/task_routes.py:67 | `Model.query.get()` | `db.session.get(Model, id)` |

## Proposed MVC Target Structure
```
task-manager-api/
├── config/settings.py
├── models/          # já existia — endurecer serializers/crypto
├── controllers/     # NOVO — orquestração
├── routes/          # views finas (binding HTTP)
├── middlewares/error_handler.py
├── services/
├── utils/
├── database.py
├── seed.py
└── app.py
```

## Refactoring Plan (Phase 3 preview)
1. Extrair config; remover secrets hardcoded
2. Criar controllers; emagrecer routes
3. Corrigir MD5, to_dict, utcnow, session.get
4. Eager load em listagem; centralizar overdue
5. Error handler central
6. Re-seed + validar todos os endpoints

================================
Total: 10 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y (confirmado pelo usuário na execução do desafio)
