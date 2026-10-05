---
name: refactor-arch
description: >
  Analisa, audita e refatora codebases backend para o padrão MVC.
  Detecta stack (linguagem, framework, banco), identifica anti-patterns
  com severidade CRITICAL/HIGH/MEDIUM/LOW, gera relatório de auditoria
  e reestrutura o projeto eliminando os problemas encontrados.
  Use quando o usuário invocar /refactor-arch, pedir auditoria arquitetural,
  refatoração MVC, detecção de code smells ou análise de anti-patterns.
---

# refactor-arch

Skill agnóstica de tecnologia para análise, auditoria e refatoração MVC de APIs backend.

## Workflow obrigatório (3 fases sequenciais)

Execute **exatamente** nesta ordem. Não pule fases. Não modifique arquivos antes da confirmação na Fase 2.

### Checklist de progresso

```
- [ ] Fase 1 — Análise
- [ ] Fase 2 — Auditoria + confirmação humana
- [ ] Fase 3 — Refatoração MVC + validação
```

---

## Fase 1 — Análise

**Objetivo:** Detectar stack, mapear arquitetura atual e imprimir resumo.

1. Ler [project-analysis.md](project-analysis.md) para heurísticas de detecção.
2. Explorar a raiz do projeto (manifests, pastas, entry points).
3. Identificar: linguagem, framework, banco de dados, domínio, estilo arquitetural, arquivos-fonte.
4. Contar arquivos de código relevantes (excluir `node_modules`, `.venv`, `__pycache__`, `*.db`, locks).
5. Imprimir o resumo no formato abaixo e **só então** avançar para a Fase 2.

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      <linguagem>
Framework:     <framework + versão se disponível>
Dependencies:  <deps relevantes>
Domain:        <domínio da aplicação>
Architecture:  <estilo atual>
Source files:  <N> files analyzed
DB:            <tecnologia / tabelas se detectáveis>
================================
```

---

## Fase 2 — Auditoria

**Objetivo:** Cruzar o código contra o catálogo, gerar relatório e **pausar**.

1. Ler [anti-patterns-catalog.md](anti-patterns-catalog.md).
2. Ler [report-template.md](report-template.md).
3. Percorrer **todos** os arquivos-fonte identificados na Fase 1.
4. Para cada anti-pattern do catálogo, registrar findings com:
   - Severidade (`CRITICAL` | `HIGH` | `MEDIUM` | `LOW`)
   - Nome do anti-pattern
   - Arquivo e linhas **exatos**
   - Descrição, impacto e recomendação
5. Incluir detecção de **APIs deprecated** quando aplicável (ver catálogo).
6. Ordenar findings: CRITICAL → HIGH → MEDIUM → LOW.
7. Exigir mínimo de **5 findings**, sendo pelo menos **1 CRITICAL ou HIGH**.
8. Imprimir o relatório seguindo [report-template.md](report-template.md).
9. **PARAR** e perguntar exatamente:

```
Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

10. **Não modificar nenhum arquivo** até receber confirmação afirmativa (`y`, `yes`, `sim`).
11. Se a resposta for negativa, encerrar sem alterações.

Salvar o relatório da Fase 2 em `../reports/audit-project-N.md` (N conforme o projeto) quando solicitado, ou no path indicado pelo usuário.

---

## Fase 3 — Refatoração MVC + Validação

**Objetivo:** Eliminar os findings, estruturar em MVC e validar que a API funciona.

1. Ler [mvc-architecture.md](mvc-architecture.md) e [refactoring-playbook.md](refactoring-playbook.md).
2. Adaptar a transformação ao nível atual de organização:
   - **Monólito plano** → criar estrutura MVC completa.
   - **Parcialmente organizado** → introduzir controllers, config, error handling; não destruir o que já funciona.
3. Aplicar os padrões do playbook para cada finding confirmado.
4. Estrutura-alvo mínima (nomes podem variar por linguagem):

```
src/  (ou equivalente na raiz)
├── config/          # settings sem hardcoded secrets
├── models/          # acesso a dados / entidades
├── views/ ou routes/# roteamento HTTP apenas
├── controllers/     # orquestração do fluxo
├── middlewares/     # error handling centralizado
└── app.<ext>        # composition root / entry point
```

5. Preservar endpoints e contratos HTTP originais (mesmos paths, métodos e shapes de resposta quando possível).
6. Remover ou isolar endpoints perigosos (SQL arbitrário, reset sem auth) — preferir remoção ou proteção.
7. Validar:
   - Instalar dependências se necessário.
   - Boot da aplicação sem erros.
   - Exercitar endpoints principais (GET health/index, CRUD básico, fluxos críticos).
8. Imprimir resumo final:

```
================================
PHASE 3: REFACTORING COMPLETE
================================
## New Project Structure
<tree>

## Validation
  ✓ Application boots without errors
  ✓ Endpoints respond correctly
================================
```

---

## Regras gerais

- **Agnóstico de stack:** Python/Flask, Node/Express e outras stacks usam as mesmas fases; apenas adapte sintaxe e tooling (pip/npm, app.run/listen).
- **Não invente findings:** cada finding precisa de arquivo + linha verificáveis.
- **Não quebre contratos:** clientes existentes devem continuar funcionando.
- **Secrets:** mover para config/env; nunca deixar credenciais hardcoded em produção.
- **SQL:** sempre parameterized queries / ORM seguro.
- Leia os arquivos de referência sob demanda; não assuma o conteúdo de memória.
