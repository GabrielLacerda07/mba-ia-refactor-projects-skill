# Template de Relatório de Auditoria (Fase 2)

Use **exatamente** esta estrutura ao gerar o relatório. Preencha todos os campos. Ordene findings por severidade: CRITICAL → HIGH → MEDIUM → LOW.

```markdown
================================
ARCHITECTURE AUDIT REPORT
================================
Project: <nome-do-projeto>
Stack:   <linguagem> + <framework>
Files:   <N> analyzed | ~<LOC> lines of code
Domain:  <domínio>

## Summary
CRITICAL: <n> | HIGH: <n> | MEDIUM: <n> | LOW: <n>

## Findings

### [CRITICAL] <Nome do Anti-Pattern>
File: <path>:<start>-<end>   # ou path:linha única
Description: <o que foi encontrado, com evidência>
Impact: <por que é grave>
Recommendation: <ação concreta alinhada ao playbook>

### [HIGH] <Nome do Anti-Pattern>
File: <path>:<linhas>
Description: ...
Impact: ...
Recommendation: ...

### [MEDIUM] <Nome do Anti-Pattern>
File: <path>:<linhas>
Description: ...
Impact: ...
Recommendation: ...

### [LOW] <Nome do Anti-Pattern>
File: <path>:<linhas>
Description: ...
Impact: ...
Recommendation: ...

## Deprecated APIs
| Local | API deprecated | Equivalente moderno |
|---|---|---|
| <file:line> | <api> | <replacement> |

(Se nenhuma API deprecated for encontrada, escrever: "Nenhuma API deprecated detectada.")

## Proposed MVC Target Structure
```
<tree proposto>
```

## Refactoring Plan (Phase 3 preview)
1. ...
2. ...
3. ...

================================
Total: <N> findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

## Regras do template

1. Cada finding **deve** ter arquivo e linhas exatos verificáveis.
2. Mínimo **5 findings**; pelo menos **1 CRITICAL ou HIGH**.
3. Incluir seção **Deprecated APIs** mesmo que vazia.
4. Após imprimir o relatório, **parar e aguardar confirmação** antes de qualquer escrita em arquivos de código.
5. Ao salvar em `reports/audit-project-N.md`, manter o mesmo conteúdo (pode omitir o prompt `[y/n]` no arquivo salvo, mas registre que a confirmação foi solicitada).
