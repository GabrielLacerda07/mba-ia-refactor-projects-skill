from flask import jsonify
from src.models import produto_model
from src.config import settings


def _validar_produto(dados, partial=False):
    if not dados:
        return "Dados inválidos"
    if not partial or "nome" in dados:
        if "nome" not in dados:
            return "Nome é obrigatório"
        nome = dados["nome"]
        if len(nome) < settings.NOME_MIN_LEN:
            return "Nome muito curto"
        if len(nome) > settings.NOME_MAX_LEN:
            return "Nome muito longo"
    if not partial or "preco" in dados:
        if "preco" not in dados:
            return "Preço é obrigatório"
        if dados["preco"] < 0:
            return "Preço não pode ser negativo"
    if not partial or "estoque" in dados:
        if "estoque" not in dados:
            return "Estoque é obrigatório"
        if dados["estoque"] < 0:
            return "Estoque não pode ser negativo"
    categoria = dados.get("categoria", "geral")
    if categoria not in settings.CATEGORIAS_VALIDAS:
        return f"Categoria inválida. Válidas: {settings.CATEGORIAS_VALIDAS}"
    return None


def listar(db):
    produtos = produto_model.get_todos(db)
    return jsonify({"dados": produtos, "sucesso": True}), 200


def buscar_por_id(db, produto_id):
    produto = produto_model.get_por_id(db, produto_id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404
    return jsonify({"dados": produto, "sucesso": True}), 200


def criar(db, dados):
    erro = _validar_produto(dados)
    if erro:
        return jsonify({"erro": erro}), 400

    produto_id = produto_model.criar(
        db,
        dados["nome"],
        dados.get("descricao", ""),
        dados["preco"],
        dados["estoque"],
        dados.get("categoria", "geral"),
    )
    return jsonify({
        "dados": {"id": produto_id},
        "sucesso": True,
        "mensagem": "Produto criado",
    }), 201


def atualizar(db, produto_id, dados):
    if not produto_model.get_por_id(db, produto_id):
        return jsonify({"erro": "Produto não encontrado"}), 404
    erro = _validar_produto(dados)
    if erro:
        return jsonify({"erro": erro}), 400

    produto_model.atualizar(
        db,
        produto_id,
        dados["nome"],
        dados.get("descricao", ""),
        dados["preco"],
        dados["estoque"],
        dados.get("categoria", "geral"),
    )
    return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200


def deletar(db, produto_id):
    if not produto_model.get_por_id(db, produto_id):
        return jsonify({"erro": "Produto não encontrado"}), 404
    produto_model.deletar(db, produto_id)
    return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200


def buscar(db, termo, categoria, preco_min, preco_max):
    if preco_min is not None and preco_min != "":
        preco_min = float(preco_min)
    else:
        preco_min = None
    if preco_max is not None and preco_max != "":
        preco_max = float(preco_max)
    else:
        preco_max = None

    resultados = produto_model.buscar(db, termo, categoria, preco_min, preco_max)
    return jsonify({"dados": resultados, "total": len(resultados), "sucesso": True}), 200
