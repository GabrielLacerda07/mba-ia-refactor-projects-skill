from werkzeug.security import generate_password_hash, check_password_hash
from src.database import get_db


def _row_to_usuario(row, include_senha=False):
    data = {
        "id": row["id"],
        "nome": row["nome"],
        "email": row["email"],
        "tipo": row["tipo"],
        "criado_em": row["criado_em"],
    }
    if include_senha:
        data["senha"] = row["senha"]
    return data


def get_todos():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM usuarios")
    return [_row_to_usuario(row) for row in cursor.fetchall()]


def get_por_id(usuario_id):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
    row = cursor.fetchone()
    return _row_to_usuario(row) if row else None


def criar(nome, email, senha, tipo="cliente"):
    db = get_db()
    cursor = db.cursor()
    senha_hash = generate_password_hash(senha)
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
        (nome, email, senha_hash, tipo),
    )
    db.commit()
    return cursor.lastrowid


def autenticar(email, senha):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    row = cursor.fetchone()
    if not row:
        return None
    if not check_password_hash(row["senha"], senha):
        # Compatibilidade com seeds antigos em plaintext
        if row["senha"] != senha:
            return None
    return {
        "id": row["id"],
        "nome": row["nome"],
        "email": row["email"],
        "tipo": row["tipo"],
    }
