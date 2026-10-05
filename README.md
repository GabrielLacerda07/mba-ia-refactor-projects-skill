# Criação de Skills — Refatoração Arquitetural Automatizada

Skill **`refactor-arch`** para Cursor: analisa, audita e refatora APIs backend para o padrão MVC, de forma agnóstica de tecnologia.

## Objetivo

Entregar uma Skill capaz de:

- Analisar uma codebase detectando linguagem, framework e arquitetura atual
- Identificar anti-patterns e code smells, classificando por severidade com arquivo e linha exatos
- Gerar um relatório de auditoria estruturado
- Refatorar o projeto para MVC, eliminando os problemas encontrados
- Validar que a aplicação continua funcionando após as mudanças

---

## A) Análise Manual

### 1. code-smells-project (Python/Flask — E-commerce)

| Severidade | Problema | Justificativa |
|---|---|---|
| **CRITICAL** | SQL Injection por concatenação (`models.py`) e endpoint `/admin/query` | Permite leitura/escrita arbitrária no banco |
| **CRITICAL** | `SECRET_KEY` hardcoded e exposta no `/health` | Vazamento de segredo de sessão |
| **CRITICAL** | Senhas em plaintext + retornadas na listagem de usuários | Compromete todas as contas |
| **HIGH** | God module `models.py` com 4 domínios | Impede testes isolados e evolução segura |
| **MEDIUM** | N+1 em listagem de pedidos/itens | Latência cresce com volume |
| **MEDIUM** | `/admin/reset-db` sem autenticação | Destruição de dados por qualquer cliente |
| **LOW** | Magic numbers nos descontos do relatório | Regras de negócio opacas |
| **LOW** | Logs com concatenação de strings | Legibilidade e padronização |

### 2. ecommerce-api-legacy (Node.js/Express — LMS/Checkout)

| Severidade | Problema | Justificativa |
|---|---|---|
| **CRITICAL** | God Class `AppManager` (DB + rotas + regras) | Viola separação de responsabilidades por completo |
| **CRITICAL** | Credenciais/payment key hardcoded em `utils.js` | Segredos de produção no código |
| **HIGH** | `badCrypto` (Base64) como hash de senha | Senhas trivialmente reversíveis |
| **HIGH** | Cartão de crédito logado em plaintext | Vazamento de PII/PCI |
| **MEDIUM** | N+1 no relatório financeiro (callbacks aninhados) | Performance e legibilidade |
| **MEDIUM** | Delete de usuário deixa órfãos no banco | Integridade referencial quebrada |
| **LOW** | Nomes `u`, `e`, `p`, `cid`, `cc` | Manutenção difícil |
| **LOW** | `globalCache` mutável | Estado global compartilhado entre requests |

### 3. task-manager-api (Python/Flask — Task Manager)

| Severidade | Problema | Justificativa |
|---|---|---|
| **CRITICAL** | `to_dict()` expõe `password` | Hash vaza pela API |
| **HIGH** | MD5 para senhas | Cripto fraca / API inadequada |
| **HIGH** | SECRET_KEY e SMTP hardcoded | Segredos no repositório |
| **HIGH** | Routes gordas sem Controllers | Camadas parciais; lógica presa ao HTTP |
| **MEDIUM** | N+1 em `GET /tasks` (user/category por item) | Performance na listagem |
| **MEDIUM** | `datetime.utcnow()` e `Query.get()` deprecated | Quebra futura em Python/SQLAlchemy novos |
| **LOW** | Imports mortos / helper não usado nas routes | Ruído e dead code |
| **LOW** | Constantes duplicadas vs literais mágicos | Drift de validação |

---

## B) Construção da Skill

### Decisões de design

A skill vive em `.cursor/skills/refactor-arch/` (convenção do Cursor) e foi **copiada para os 3 projetos**.

| Arquivo | Área de conhecimento |
|---|---|
| `SKILL.md` | Orquestra as 3 fases (prompt operacional) |
| `project-analysis.md` | Heurísticas de linguagem, framework, DB, domínio, arquitetura |
| `anti-patterns-catalog.md` | 11 anti-patterns + tabela de APIs deprecated |
| `report-template.md` | Formato padronizado do relatório (Fase 2) |
| `mvc-architecture.md` | Responsabilidades Models / Views / Controllers / Config / Middleware |
| `refactoring-playbook.md` | 11 padrões de transformação com antes/depois |

O `SKILL.md` permanece enxuto (~150 linhas): instrui o agente a **ler** os arquivos de referência sob demanda (progressive disclosure).

### Anti-patterns do catálogo (e por quê)

1. SQL Injection — presente nos projetos Flask legados  
2. Hardcoded Secrets — comum aos 3  
3. God Class/Module — AppManager e models monolíticos  
4. Fat Controller/Routes — routes sem controllers  
5. Weak/Deprecated Crypto — MD5, badCrypto, plaintext  
6. Mutable Global State — db global, globalCache  
7. N+1 Queries — pedidos, relatório LMS, tasks  
8. Missing Validation / Insecure Endpoints — admin abertos, deletes sujos  
9. Duplication / Dead Code — overdue repetido  
10. Magic Numbers / Poor Naming — descontos, variáveis curtas  
11. Sensitive Data Leakage — senhas/secrets em responses  

Inclui detecção explícita de APIs deprecated (`datetime.utcnow`, `Query.get`, MD5, Base64-as-hash).

### Agnosticismo de tecnologia

- Heurísticas por manifesto (`requirements.txt` / `package.json`) e imports  
- Playbook com exemplos Python **e** Node  
- MVC alvo descrito em termos de responsabilidade, não de pasta fixa única  
- Fase 3 adapta: monólito plano → MVC completo; parcialmente organizado → controllers + config sem destruir o que já funciona  

### Desafios e soluções

| Desafio | Solução |
|---|---|
| Projeto 3 já tinha layers | Introduzir Controllers/Config sem reescrever models ORM |
| Contratos HTTP diferentes (PT/EN) | Preservar paths e shapes originais |
| Senhas legadas plaintext/MD5 | Hash moderno + fallback de verificação na migração |
| Confirmação obrigatória na Fase 2 | Prompt explícito `[y/n]` antes de qualquer escrita |

---

## C) Resultados

### Resumo dos findings (Fase 2)

| Projeto | CRITICAL | HIGH | MEDIUM | LOW | Total |
|---|---|---|---|---|---|
| code-smells-project | 5 | 2 | 2 | 2 | **11** |
| ecommerce-api-legacy | 3 | 3 | 2 | 2 | **10** |
| task-manager-api | 2 | 3 | 3 | 2 | **10** |

Relatórios completos em [`reports/`](reports/).

### Comparação antes / depois

**Projeto 1 — code-smells-project**

```
Antes: app.py, controllers.py, models.py, database.py
Depois:
src/config/  models/  controllers/  views/  middlewares/  database.py  app.py
+ app.py (entry)
```

**Projeto 2 — ecommerce-api-legacy**

```
Antes: app.js, AppManager.js, utils.js
Depois:
src/config/  models/  controllers/  views/  middlewares/  database.js  app.js
```

**Projeto 3 — task-manager-api**

```
Antes: models/ + routes/ + services/ (sem controllers/config)
Depois: + config/ + controllers/ + middlewares/ ; routes emagrecidas
```

### Logs de validação (pós-refatoração)

**Projeto 1**
```
health 200 {... 'status': 'ok' ...}
produtos 200 10
login 200 {... 'sucesso': True}
pedido 201 {... 'pedido_id': 1 ...}
usuarios 200 senha_leak= False
relatorio 200
```

**Projeto 2**
```
checkout 200 { msg: 'Sucesso', enrollment_id: 2 }
denied 400 {"erro":"Pagamento recusado"}
report 200 [{"course":"Clean Architecture","revenue":997,...}, ...]
```

**Projeto 3**
```
Seed: 3 usuários, 4 categorias, 10 tasks
tasks 200 10 | users 200 | login 200 | password_leak False
stats/summary/categories/search/create_task OK
```

### Checklist de Validação

#### Projeto 1 — code-smells-project

**Fase 1**
- [x] Linguagem detectada (Python)
- [x] Framework detectado (Flask)
- [x] Domínio descrito (E-commerce)
- [x] Arquivos analisados coerentes (4)

**Fase 2**
- [x] Relatório no template
- [x] Findings com arquivo/linhas
- [x] Ordenados por severidade
- [x] ≥ 5 findings (11)
- [x] APIs deprecated cobertas
- [x] Pausa com confirmação antes da Fase 3

**Fase 3**
- [x] Estrutura MVC
- [x] Config sem hardcoded de produção
- [x] Models / Views / Controllers
- [x] Error handling centralizado
- [x] Entry point claro
- [x] App inicia e endpoints respondem

#### Projeto 2 — ecommerce-api-legacy

**Fase 1**
- [x] JavaScript detectado
- [x] Express detectado
- [x] Domínio LMS/Checkout
- [x] 3 source files analisados

**Fase 2**
- [x] Template + linhas exatas
- [x] ≥ 5 findings (10) com CRITICAL/HIGH
- [x] Deprecated crypto detectada
- [x] Confirmação antes da Fase 3

**Fase 3**
- [x] MVC criado
- [x] Config via env
- [x] Models/Controllers/Views/Middleware
- [x] Boot + checkout/report/delete OK

#### Projeto 3 — task-manager-api

**Fase 1**
- [x] Python/Flask
- [x] Domínio Task Manager
- [x] Contagem de arquivos coerente (~14)

**Fase 2**
- [x] ≥ 5 findings (10) com CRITICAL/HIGH
- [x] Deprecated APIs (MD5, utcnow, Query.get)
- [x] Confirmação antes da Fase 3

**Fase 3**
- [x] Controllers + config + middleware sem quebrar layers existentes
- [x] Todos os endpoints testados respondendo
- [x] Senha removida do serializer; hash moderno

### Observações entre stacks

A mesma skill funcionou em Flask monolítico, Express God Class e Flask parcialmente organizado. A Fase 3 não aplicou o mesmo “big bang”: no projeto 3 preservou SQLAlchemy models e apenas introduziu a camada que faltava (Controllers) + hardening.

---

## D) Como Executar

### Pré-requisitos

- [Cursor](https://cursor.com) com Agent Skills habilitado
- Python 3.12+ (projetos 1 e 3) / Node.js 18+ (projeto 2)
- Skill presente em `.cursor/skills/refactor-arch/` de cada projeto

### Invocar a skill

No chat do Agent do Cursor, a partir da pasta do projeto (ou mencionando o path):

```
/refactor-arch
```

Ou peça explicitamente, por exemplo:

```
Execute a skill refactor-arch neste projeto
```

Na Fase 2, revise o relatório e responda `y` para autorizar a Fase 3.

Os relatórios desta execução estão em:

- `reports/audit-project-1.md`
- `reports/audit-project-2.md`
- `reports/audit-project-3.md`

### Validar manualmente após refatoração

```bash
# Projeto 1
cd code-smells-project && pip install -r requirements.txt && python app.py
# curl http://localhost:5000/health

# Projeto 2
cd ecommerce-api-legacy && npm install && npm start
# ver api.http

# Projeto 3
cd task-manager-api && pip install -r requirements.txt && python seed.py && python app.py
# curl http://localhost:5000/tasks
```

---

## Critérios de Aceite

| Critério | P1 | P2 | P3 |
|---|---|---|---|
| Fase 1 detecta stack | ✅ | ✅ | ✅ |
| Fase 2 ≥ 5 findings | ✅ 11 | ✅ 10 | ✅ 10 |
| ≥ 1 CRITICAL ou HIGH | ✅ | ✅ | ✅ |
| Fase 3 app funciona | ✅ | ✅ | ✅ |

## Referências

- Skills de projeto no Cursor: `.cursor/skills/<nome>/SKILL.md`
- [Cursor Docs](https://docs.cursor.com) — Agent Skills / regras de projeto
