const express = require('express');
const config = require('./config/settings');
const { createDatabase } = require('./database');
const { registerRoutes } = require('./views/routes');
const { errorHandler } = require('./middlewares/errorHandler');

async function bootstrap() {
  const app = express();
  app.use(express.json());

  const db = await createDatabase();
  registerRoutes(app, db);
  app.use(errorHandler);

  app.listen(config.port, () => {
    console.log(`Frankenstein LMS rodando na porta ${config.port}...`);
  });
}

bootstrap().catch((err) => {
  console.error('Falha ao iniciar aplicação:', err);
  process.exit(1);
});
