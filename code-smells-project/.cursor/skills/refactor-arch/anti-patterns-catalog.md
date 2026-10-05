# Catálogo de Anti-Patterns

Mínimo de 8 anti-patterns com severidade distribuída. Use sinais concretos (não "código ruim").

Classificação: **CRITICAL** → **HIGH** → **MEDIUM** → **LOW** (ver README do desafio).

---

## 1. SQL Injection / Query String Concatenation
**Severidade:** CRITICAL

**Sinais de detecção:**
- Concatenação de strings em SQL: `"WHERE id = " + str(id)`, `` `WHERE email = '${email}'` ``
- `cursor.execute(query)` onde `query` foi montada com input do usuário
- Endpoint que executa SQL arbitrário (`/admin/query`, body com campo `sql`)

**Impacto:** Leitura/escrita arbitrária no banco; comprometimento total dos dados.

**Correção:** Parameterized queries (`?`, `%s`) ou ORM; remover endpoints de SQL livre.

---

## 2. Hardcoded Secrets / Credentials
**Severidade:** CRITICAL

**Sinais de detecção:**
- `SECRET_KEY = "..."`, `password = "senha..."`, `paymentGatewayKey: "pk_live_..."`
- Credenciais SMTP, DB user/pass em código-fonte
- Secrets expostos em responses (`health` retornando `secret_key`)

**Impacto:** Exposição de credenciais; acesso indevido a sistemas e dados.

**Correção:** Extrair para `config` + variáveis de ambiente; nunca retornar secrets em APIs.

---

## 3. God Class / God Module
**Severidade:** CRITICAL

**Sinais de detecção:**
- Um arquivo/classe com DB init + rotas HTTP + regras de negócio + notificações
- Módulo único cobrindo múltiplos domínios (produtos, usuários, pedidos, relatórios)
- Arquivo com centenas de linhas misturando responsabilidades

**Impacto:** Impossível testar/isolar; qualquer mudança tem efeito colateral amplo.

**Correção:** Separar em Models (dados), Controllers (fluxo), Views/Routes (HTTP).

---

## 4. Fat Controller / Business Logic in Routes
**Severidade:** HIGH

**Sinais de detecção:**
- Handlers de rota com validação pesada, cálculo de totais, loops de persistência
- Rotas Flask/Express com SQL direto ou orquestração de checkout completa
- Ausência de camada Controller quando `routes/` só deveria rotear

**Impacto:** Difícil reutilizar e testar regras; acoplamento ao framework HTTP.

**Correção:** Mover orquestração para Controllers; routes só binding HTTP ↔ controller.

---

## 5. Weak / Deprecated Cryptography
**Severidade:** HIGH (CRITICAL se senhas em plaintext)

**Sinais de detecção:**
- `hashlib.md5` / `sha1` para senhas
- Senhas armazenadas em plaintext
- Funções custom tipo `badCrypto` / Base64 como "hash"
- Comparação direta `senha == senha_banco` sem hash

**APIs deprecated / inseguras (detecção obrigatória):**

| Deprecated / inseguro | Equivalente moderno |
|---|---|
| `hashlib.md5` / `sha1` para senhas | `werkzeug.security` / `bcrypt` / `argon2` |
| `datetime.utcnow()` (Python 3.12+) | `datetime.now(timezone.utc)` |
| `Model.query.get()` (SQLAlchemy 2.x) | `db.session.get(Model, id)` |
| Plaintext / Base64 "crypto" | Algoritmo de hashing de senha adequado |
| `sqlite3` string concat | Placeholders `?` |

**Impacto:** Credenciais quebráveis; APIs obsoletas quebram em versões novas.

**Correção:** Migrar para API moderna recomendada na tabela acima.

---

## 6. Mutable Global State
**Severidade:** HIGH

**Sinais de detecção:**
- `global db_connection`, `let globalCache = {}`, singleton mutável compartilhado
- Variáveis de módulo alteradas por requests concorrentes

**Impacto:** Race conditions; comportamento imprevisível sob carga; testes flaky.

**Correção:** Connection factory / DI; cache com escopo explícito; evitar globais mutáveis.

---

## 7. N+1 Query Pattern
**Severidade:** MEDIUM

**Sinais de detecção:**
- `for` / `forEach` com query dentro do loop (`SELECT` por item)
- Nested callbacks com `db.get`/`db.all` por enrollment/pedido
- `User.query.get(t.user_id)` dentro de loop de tasks

**Impacto:** Latência cresce linearmente com volume de dados.

**Correção:** JOINs, `joinedload`/`selectinload`, batch fetch, queries agregadas.

---

## 8. Missing Validation / Insecure Endpoints
**Severidade:** MEDIUM

**Sinais de detecção:**
- Rotas admin sem autenticação (`/admin/reset-db`, delete user aberto)
- Delete que deixa órfãos (matrículas/pagamentos sujos)
- Campos obrigatórios não validados; tipagem fraca

**Impacto:** Abuso de API; inconsistência de dados; operações destrutivas públicas.

**Correção:** Validação de input; auth em rotas sensíveis; cascata ou transação no delete.

---

## 9. Code Duplication / Dead Code
**Severidade:** MEDIUM

**Sinais de detecção:**
- Mesmo bloco de validação copiado em create/update
- Lógica `is_overdue` repetida em 4+ lugares
- Helpers definidos e nunca importados (`process_task_data`)
- Imports não usados (`os, sys, json` sem uso)

**Impacto:** Drift de comportamento; manutenção cara.

**Correção:** Extrair funções/helpers únicos; remover dead code.

---

## 10. Magic Numbers / Poor Naming
**Severidade:** LOW

**Sinais de detecção:**
- Literais `0.1`, `10000`, `10000` loops sem constante nomeada
- Variáveis `u`, `e`, `p`, `cid`, `cc`
- Concatenação de log `"Listando " + str(n)` em vez de f-string

**Impacto:** Legibilidade baixa; risco de alterar o literal errado.

**Correção:** Constantes nomeadas; nomes descritivos; logging idiomático.

---

## 11. Sensitive Data Leakage in Responses
**Severidade:** CRITICAL (quando inclui senhas/secrets) / HIGH

**Sinais de detecção:**
- `to_dict()` inclui `password` / `senha`
- Health endpoint retorna `secret_key`, path de DB, debug flags
- Logs com número de cartão completo

**Impacto:** Vazamento de PII e segredos via API ou logs.

**Correção:** Serializers sem campos sensíveis; mascarar cartões; health mínimo.

---

## Como usar na Fase 2

1. Percorra cada item do catálogo.
2. Busque os sinais no código (grep + leitura).
3. Registre finding só com evidência (arquivo:linhas).
4. Inclua pelo menos uma detecção de API deprecated quando existir no projeto.
5. Ordene por severidade no relatório.
