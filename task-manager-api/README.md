# task-manager-api

API de Task Manager em Python/Flask refatorada para MVC via skill `refactor-arch`. Mantém models/routes existentes, com controllers, config e middlewares adicionados.

## Como rodar

```bash
pip install -r requirements.txt
python seed.py
python app.py
```

A aplicação sobe em `http://localhost:5000`.

## Estrutura (MVC)

```
config/settings.py
models/
controllers/
routes/          # views HTTP
middlewares/
services/
utils/
database.py
app.py
```
