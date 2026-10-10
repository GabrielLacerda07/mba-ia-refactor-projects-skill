def _row_to_produto(row):
    return {
        "id": row["id"],
        "nome": row["nome"],
        "descricao": row["descricao"],
        "preco": row["preco"],
        "estoque": row["estoque"],
        "categoria": row["categoria"],
        "ativo": row["ativo"],
        "criado_em": row["criado_em"],
    }


def get_todos(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produtos")
    return [_row_to_produto(row) for row in cursor.fetchall()]


def get_por_id(db, produto_id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
    row = cursor.fetchone()
    return _row_to_produto(row) if row else None


def criar(db, nome, descricao, preco, estoque, categoria):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES (?, ?, ?, ?, ?)",
        (nome, descricao, preco, estoque, categoria),
    )
    db.commit()
    return cursor.lastrowid


def atualizar(db, produto_id, nome, descricao, preco, estoque, categoria):
    cursor = db.cursor()
    cursor.execute(
        """
        UPDATE produtos
        SET nome = ?, descricao = ?, preco = ?, estoque = ?, categoria = ?
        WHERE id = ?
        """,
        (nome, descricao, preco, estoque, categoria, produto_id),
    )
    db.commit()
    return True


def deletar(db, produto_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    db.commit()
    return True


def buscar(db, termo, categoria=None, preco_min=None, preco_max=None):
    cursor = db.cursor()
    query = "SELECT * FROM produtos WHERE 1=1"
    params = []

    if termo:
        query += " AND (nome LIKE ? OR descricao LIKE ?)"
        like = f"%{termo}%"
        params.extend([like, like])
    if categoria:
        query += " AND categoria = ?"
        params.append(categoria)
    if preco_min is not None:
        query += " AND preco >= ?"
        params.append(preco_min)
    if preco_max is not None:
        query += " AND preco <= ?"
        params.append(preco_max)

    cursor.execute(query, params)
    return [_row_to_produto(row) for row in cursor.fetchall()]
