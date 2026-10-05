# Análise de Projeto — Heurísticas

Use estas heurísticas na **Fase 1** para detectar stack e mapear arquitetura. São agnósticas: aplique na ordem e registre evidências.

## 1. Detecção de linguagem

| Sinal | Linguagem |
|---|---|
| `*.py`, `requirements.txt`, `pyproject.toml`, `Pipfile` | Python |
| `*.js` / `*.ts`, `package.json`, `package-lock.json` | JavaScript / TypeScript |
| `*.go`, `go.mod` | Go |
| `*.java`, `pom.xml`, `build.gradle` | Java |
| `*.rb`, `Gemfile` | Ruby |
| `*.cs`, `*.csproj` | C# |

Priorize o manifesto (`requirements.txt`, `package.json`) sobre extensões isoladas.

## 2. Detecção de framework

### Python
| Dependência / import | Framework |
|---|---|
| `flask`, `from flask import` | Flask |
| `fastapi`, `from fastapi import` | FastAPI |
| `django`, `DJANGO_SETTINGS_MODULE` | Django |
| `flask_sqlalchemy`, `SQLAlchemy` | ORM SQLAlchemy (complementar) |

### Node.js
| Dependência / require | Framework |
|---|---|
| `express` | Express |
| `fastify` | Fastify |
| `koa` | Koa |
| `nest` / `@nestjs/*` | NestJS |

Extraia versão de `requirements.txt` (`flask==3.1.1`) ou `package.json` (`"express": "^4.18.2"`).

## 3. Detecção de banco de dados

| Sinal | Banco |
|---|---|
| `sqlite3`, `*.db`, `:memory:`, `sqlite:///` | SQLite |
| `psycopg`, `postgresql://`, `pg` | PostgreSQL |
| `mysql`, `pymysql`, `mysql://` | MySQL |
| `mongodb`, `mongoose` | MongoDB |
| `CREATE TABLE`, models ORM | Relacional (inferir tabelas) |

Liste tabelas encontradas em `CREATE TABLE`, models ou seeds.

## 4. Detecção de domínio

Analise nomes de rotas, models e seeds:

| Palavras-chave | Domínio provável |
|---|---|
| produto, pedido, carrinho, estoque, checkout | E-commerce |
| course, enrollment, payment, lms | LMS / Educação |
| task, todo, category, assignee | Task Manager |
| user, auth, login | Identidade (transversal) |

Descreva o domínio em 1 linha: entidades principais + propósito da API.

## 5. Mapeamento de arquitetura atual

Classifique o estilo predominante:

| Estilo | Sinais |
|---|---|
| **Monólito plano** | Poucos arquivos na raiz; rotas + SQL + regras no mesmo módulo |
| **God Class** | Uma classe/arquivo concentra DB init, rotas e regras de negócio |
| **Camadas parciais** | Existem pastas `models/`, `routes/`, `services/` mas lógica vaza entre elas |
| **MVC incompleto** | Models e Views/Routes existem; Controllers ausentes ou vazios |
| **MVC adequado** | Models / Views / Controllers com responsabilidades claras + config + error handler |

Conte arquivos-fonte (código da aplicação), excluindo:

- `node_modules/`, `.venv/`, `venv/`, `__pycache__/`
- `*.db`, `package-lock.json`, `.git/`
- Arquivos da skill (`.cursor/`)

## 6. Entry point e composição

| Stack | Entry típico |
|---|---|
| Flask | `app.py`, `wsgi.py`, `if __name__ == "__main__"` |
| Express | `src/app.js`, `server.js`, `bin/www`, script `start` no package.json |

Identifique onde rotas são registradas e onde o servidor sobe (`app.run`, `app.listen`).

## 7. Template de saída (obrigatório)

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      <...>
Framework:     <...>
Dependencies:  <...>
Domain:        <...>
Architecture:  <...>
Source files:  <N> files analyzed
DB:            <...>
================================
```
