# Playbook de Refatoração

Padrões concretos de transformação (antes → depois). Mínimo 8. Adapte a sintaxe à stack do projeto.

---

## 1. SQL concatenado → Parameterized Query

**Antes (Python):**
```python
cursor.execute("SELECT * FROM produtos WHERE id = " + str(id))
cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES ('" + nome + "', '" + email + "', '" + senha + "')")
```

**Depois:**
```python
cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
cursor.execute(
    "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
    (nome, email, senha),
)
```

---

## 2. Secrets hardcoded → Config + Environment

**Antes:**
```python
app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"
```

```javascript
const config = { paymentGatewayKey: "pk_live_1234567890abcdef", port: 3000 };
```

**Depois:**
```python
# config/settings.py
import os
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
DATABASE_PATH = os.environ.get("DATABASE_PATH", "loja.db")
```

```javascript
// config/settings.js
module.exports = {
  port: process.env.PORT || 3000,
  paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || "dev-key",
};
```

---

## 3. God Module → Models + Controllers + Routes

**Antes:** um arquivo com `setupRoutes` + SQL + regras de checkout.

**Depois:**
```
models/courseModel.js      → queries de cursos
models/userModel.js        → users
controllers/checkoutController.js → orquestra checkout
views/routes.js            → app.post('/api/checkout', checkoutController.checkout)
```

```javascript
// views/routes.js
const checkout = require('../controllers/checkoutController');
module.exports = (app) => {
  app.post('/api/checkout', checkout.checkout);
};
```

---

## 4. Fat Route → Thin Route + Controller

**Antes (Flask):**
```python
@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    # 80 linhas de validação + SQLAlchemy + print
    ...
```

**Depois:**
```python
# views/task_routes.py
@task_bp.route('/tasks', methods=['POST'])
def create_task():
    return task_controller.create_task(request.get_json())

# controllers/task_controller.py
def create_task(data):
    errors = validate_task(data)
    if errors:
        return jsonify({'error': errors}), 400
    task = TaskModel.create(data)
    return jsonify(task.to_dict()), 201
```

---

## 5. Weak Crypto / Deprecated Hash → Modern Password Hashing

**Antes:**
```python
self.password = hashlib.md5(pwd.encode()).hexdigest()
```

```javascript
function badCrypto(pwd) {
  return Buffer.from(pwd).toString('base64').substring(0, 10);
}
```

**Depois:**
```python
from werkzeug.security import generate_password_hash, check_password_hash

def set_password(self, pwd):
    self.password = generate_password_hash(pwd)

def check_password(self, pwd):
    return check_password_hash(self.password, pwd)
```

```javascript
const crypto = require('crypto');
function hashPassword(pwd) {
  const salt = crypto.randomBytes(16).toString('hex');
  const hash = crypto.scryptSync(pwd, salt, 64).toString('hex');
  return `${salt}:${hash}`;
}
```

---

## 6. Deprecated datetime.utcnow → timezone-aware

**Antes:**
```python
created_at = db.Column(db.DateTime, default=datetime.utcnow)
if t.due_date < datetime.utcnow():
    ...
```

**Depois:**
```python
from datetime import datetime, timezone

def utcnow():
    return datetime.now(timezone.utc)

created_at = db.Column(db.DateTime, default=utcnow)
if t.due_date.replace(tzinfo=timezone.utc) < utcnow():
    ...
```

---

## 7. N+1 Queries → JOIN / Eager Load / Batch

**Antes:**
```python
for row in pedidos:
    cursor.execute("SELECT * FROM itens_pedido WHERE pedido_id = " + str(row["id"]))
    for item in itens:
        cursor.execute("SELECT nome FROM produtos WHERE id = " + str(item["produto_id"]))
```

**Depois:**
```python
cursor.execute("""
    SELECT p.*, i.produto_id, i.quantidade, i.preco_unitario, pr.nome AS produto_nome
    FROM pedidos p
    LEFT JOIN itens_pedido i ON i.pedido_id = p.id
    LEFT JOIN produtos pr ON pr.id = i.produto_id
    WHERE p.usuario_id = ?
""", (usuario_id,))
# Agrupar rows em memória por pedido_id
```

```python
# SQLAlchemy
tasks = Task.query.options(
    joinedload(Task.user),
    joinedload(Task.category),
).all()
```

---

## 8. Sensitive Leakage → Safe Serializer

**Antes:**
```python
def to_dict(self):
    return {'id': self.id, 'email': self.email, 'password': self.password}
```

**Depois:**
```python
def to_dict(self):
    return {
        'id': self.id,
        'name': self.name,
        'email': self.email,
        'role': self.role,
        'active': self.active,
        'created_at': str(self.created_at),
    }
```

Remover `secret_key` de health checks; mascarar cartões em logs (`****4444`).

---

## 9. Global Mutable DB → Factory / DI

**Antes:**
```python
db_connection = None
def get_db():
    global db_connection
    if db_connection is None:
        db_connection = sqlite3.connect(...)
    return db_connection
```

**Depois:**
```python
def get_connection(db_path):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Em app startup: app.config['DB'] = init_db(settings.DATABASE_PATH)
```

---

## 10. Magic Numbers / Poor Names → Named Constants

**Antes:**
```python
if faturamento > 10000:
    desconto = faturamento * 0.1
```

```javascript
let u = req.body.usr; let e = req.body.eml; let cc = req.body.card;
```

**Depois:**
```python
TIER_HIGH = 10_000
RATE_HIGH = 0.10
if faturamento > TIER_HIGH:
    desconto = faturamento * RATE_HIGH
```

```javascript
const userName = req.body.usr;
const email = req.body.eml;
const cardNumber = req.body.card;
```

---

## 11. Scattered try/except → Central Error Handler

**Antes:** cada handler com `try/except` repetido retornando `jsonify({"erro": str(e)})`.

**Depois (Flask):**
```python
# middlewares/error_handler.py
def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.exception(e)
        return jsonify({"erro": "Erro interno", "sucesso": False}), 500

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"erro": "Não encontrado", "sucesso": False}), 404
```

**Depois (Express):**
```javascript
function errorHandler(err, req, res, next) {
  console.error(err);
  res.status(err.status || 500).json({ erro: err.message || 'Erro interno' });
}
app.use(errorHandler);
```

---

## Ordem sugerida de aplicação na Fase 3

1. Criar `config/` e remover secrets do código
2. Criar estrutura de pastas MVC
3. Extrair Models (com queries parametrizadas)
4. Extrair Controllers
5. Deixar Routes/Views finas
6. Registrar error handler
7. Corrigir crypto, serializers, N+1, deprecated APIs
8. Validar boot + endpoints
