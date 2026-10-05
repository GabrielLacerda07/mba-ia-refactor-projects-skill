================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy
Stack:   JavaScript + Express 4.18.2
Files:   3 analyzed | ~170 lines of code
Domain:  LMS API com fluxo de checkout (cursos, matrículas, pagamentos)

## Summary
CRITICAL: 3 | HIGH: 3 | MEDIUM: 2 | LOW: 2

## Findings

### [CRITICAL] God Class / God Module
File: src/AppManager.js:1-141
Description: Classe única concentra init de DB, seeds, rotas HTTP e regras de checkout/relatório/delete.
Impact: Impossível isolar testes; qualquer mudança no checkout afeta o restante.
Recommendation: Separar database, models, controllers e views/routes.

### [CRITICAL] Hardcoded Secrets / Credentials
File: src/utils.js:1-7
Description: Credenciais de DB, payment gateway (`pk_live_...`) e SMTP hardcoded no código.
Impact: Vazamento de chaves de produção no repositório.
Recommendation: `config/settings.js` + variáveis de ambiente.

### [CRITICAL] Sensitive Data Leakage in Responses / Logs
File: src/AppManager.js:45
Description: Número completo do cartão logado em plaintext (`Processando cartão ${cc}`).
Impact: PCI/PII em logs; risco regulatório e de fraude.
Recommendation: Mascarar cartão (`****4444`) nos logs.

### [HIGH] Fat Controller / Business Logic in Routes
File: src/AppManager.js:28-78
Description: Handler de `/api/checkout` com callback hell: busca curso → usuário → cria user → pagamento → matrícula → audit.
Impact: Fluxo ilegível; tratamento de erro inconsistente; difícil reutilizar.
Recommendation: Controller async/await orquestrando models.

### [HIGH] Weak / Deprecated Cryptography
File: src/utils.js:17-23
Description: `badCrypto` usa Base64 truncado em loop como "hash" de senha.
Impact: Senhas trivialmente reversíveis.
Recommendation: `crypto.scryptSync` com salt (ou bcrypt).

### [HIGH] Mutable Global State
File: src/utils.js:9-15
Description: `globalCache` e `totalRevenue` mutáveis em nível de módulo; `logAndCache` altera estado global.
Impact: Estado compartilhado entre requests; testes não isolados.
Recommendation: Remover cache global; efeitos colaterais explícitos.

### [MEDIUM] N+1 Query Pattern
File: src/AppManager.js:80-128
Description: Relatório financeiro itera cursos → enrollments → user → payment com queries aninhadas.
Impact: Explosão de queries sob volume.
Recommendation: JOIN único agregando receita e alunos.

### [MEDIUM] Missing Validation / Insecure Endpoints
File: src/AppManager.js:131-137
Description: `DELETE /api/users/:id` remove usuário deixando matrículas/pagamentos órfãos ("ficaram sujos no banco").
Impact: Inconsistência referencial no banco.
Recommendation: Delete em cascata (payments → enrollments → user) em transação.

### [LOW] Magic Numbers / Poor Naming
File: src/AppManager.js:29-33
Description: Variáveis `u`, `e`, `p`, `cid`, `cc` e body keys abreviadas (`usr`, `eml`, `pwd`).
Impact: Código difícil de ler e manter.
Recommendation: Nomes descritivos (`userName`, `email`, `cardNumber`) preservando contrato HTTP.

### [LOW] Callback Hell / Poor Readability
File: src/AppManager.js:37-77
Description: Nested callbacks de 4–5 níveis no checkout.
Impact: Manutenção e propagação de erros frágeis.
Recommendation: Promisificar sqlite3 + async/await.

## Deprecated APIs
| Local | API deprecated | Equivalente moderno |
|---|---|---|
| src/utils.js:17-23 | Base64 truncado como hash de senha (`badCrypto`) | `crypto.scryptSync` com salt |
| src/AppManager.js (callbacks) | Callback-only sqlite3 nesting | Promises / async-await |

## Proposed MVC Target Structure
```
src/
├── config/settings.js
├── models/
│   ├── userModel.js
│   ├── courseModel.js
│   ├── enrollmentModel.js
│   └── paymentModel.js
├── controllers/
│   ├── checkoutController.js
│   ├── reportController.js
│   └── userController.js
├── views/routes.js
├── middlewares/errorHandler.js
├── database.js
└── app.js
```

## Refactoring Plan (Phase 3 preview)
1. Extrair config/secrets para env
2. Criar database factory + models promisificados
3. Controllers async para checkout, report e delete
4. Routes finas + error handler central
5. Corrigir crypto, N+1, cascata no delete, mask de cartão
6. Validar endpoints originais

================================
Total: 10 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y (confirmado pelo usuário na execução do desafio)
