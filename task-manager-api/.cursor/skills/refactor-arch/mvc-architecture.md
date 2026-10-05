# Guidelines de Arquitetura MVC

Padrão-alvo da Fase 3. Independente de linguagem: preserve contratos HTTP; reorganize responsabilidades.

## Camadas

### Models
**Responsabilidade:** persistência, entidades, queries, mapeamento de dados.

- Acesso ao banco (SQL parametrizado ou ORM)
- Regras de integridade de dados do domínio (estoque suficiente, email único)
- Serialização segura (`to_dict` **sem** senhas/secrets)
- **Não** conhecem HTTP (`request`, `response`, status codes)

### Views / Routes
**Responsabilidade:** binding HTTP — paths, métodos, parsing de request, status codes.

- Registrar rotas / blueprints / routers
- Extrair params/body/query e delegar ao Controller
- Retornar JSON/HTML a partir do resultado do Controller
- **Não** contêm SQL nem regras de negócio complexas

### Controllers
**Responsabilidade:** orquestrar o fluxo da aplicação.

- Validar input (ou chamar validator)
- Chamar Models / services na ordem correta
- Coordenar efeitos colaterais (notificações) via abstrações
- Traduzir erros de domínio em respostas apropriadas
- **Não** montam SQL cru nem leem config secreta diretamente demais — preferem Models/config

### Config
- Centralizar settings (`PORT`, `SECRET_KEY`, `DATABASE_URL`)
- Ler de variáveis de ambiente com defaults seguros para dev
- Zero secrets hardcoded no restante do código

### Middlewares / Error handling
- Handler global de exceções
- Respostas de erro consistentes (`{ "erro": "..." }` ou shape do projeto)
- Logging centralizado (sem dados sensíveis)

### Entry point (Composition Root)
- Cria app, carrega config, registra routes/blueprints, sobe servidor
- Fino: sem lógica de negócio

## Estrutura de diretórios alvo

### Python / Flask
```
src/
├── config/
│   └── settings.py
├── models/
│   ├── __init__.py
│   ├── produto_model.py
│   └── ...
├── controllers/
│   ├── produto_controller.py
│   └── ...
├── views/
│   └── routes.py          # ou blueprints em views/
├── middlewares/
│   └── error_handler.py
├── database.py
└── app.py
```

Entry na raiz pode reexportar: `app.py` → `from src.app import app`.

### Node.js / Express
```
src/
├── config/
│   └── settings.js
├── models/
│   ├── userModel.js
│   └── ...
├── controllers/
│   ├── checkoutController.js
│   └── ...
├── views/   # ou routes/
│   └── routes.js
├── middlewares/
│   └── errorHandler.js
├── database.js
└── app.js
```

## Adaptação por contexto

| Situação atual | Estratégia |
|---|---|
| Monólito plano (4 arquivos) | Criar árvore MVC completa; mover código por domínio |
| God Class única | Extrair models por entidade; routes finas; controllers por caso de uso |
| Já tem models/ + routes/ | Introduzir `controllers/`, `config/`, `middlewares/`; emagrecer routes |
| Já próximo de MVC | Corrigir smells (SQL, secrets, N+1) sem reescrever tudo |

## Princípios SOLID aplicados

- **S:** um controller por domínio/caso de uso coerente
- **O:** novos endpoints via novos handlers, sem inflar God Class
- **D:** Controllers dependem de Models/abstrações, não de SQL embutido

## Checklist MVC (validação Fase 3)

- [ ] Config sem secrets hardcoded no código de negócio
- [ ] Models abstraem dados
- [ ] Views/Routes só roteiam
- [ ] Controllers orquestram
- [ ] Error handling centralizado
- [ ] Entry point claro
- [ ] App sobe e endpoints respondem
