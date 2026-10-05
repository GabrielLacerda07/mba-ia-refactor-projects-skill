# code-smells-project

API de E-commerce em Python/Flask refatorada para MVC via skill `refactor-arch`.

## Como rodar

```bash
pip install -r requirements.txt
python app.py
```

A aplicação sobe em `http://localhost:5000`. O banco SQLite (`loja.db`) é criado automaticamente no primeiro boot.

## Estrutura (MVC)

```
src/
├── config/settings.py
├── models/
├── controllers/
├── views/routes.py
├── middlewares/error_handler.py
├── database.py
└── app.py
```
