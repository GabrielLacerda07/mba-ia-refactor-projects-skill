# ecommerce-api-legacy

LMS API (checkout) em Node.js/Express refatorada para MVC via skill `refactor-arch`.

## Como rodar

```bash
npm install
npm start
```

A aplicação sobe em `http://localhost:3000`. O banco SQLite é em memória e carrega seeds no boot.

Exemplos de requisições em `api.http`.

## Estrutura (MVC)

```
src/
├── config/settings.js
├── models/
├── controllers/
├── views/routes.js
├── middlewares/errorHandler.js
├── database.js
└── app.js
```
