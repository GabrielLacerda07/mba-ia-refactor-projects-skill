from flask import jsonify
from src.models import pedido_model
from src.config import settings


def criar(db, dados):
    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    usuario_id = dados.get("usuario_id")
    itens = dados.get("itens", [])

    if not usuario_id:
        return jsonify({"erro": "Usuario ID é obrigatório"}), 400
    if not itens:
        return jsonify({"erro": "Pedido deve ter pelo menos 1 item"}), 400

    resultado = pedido_model.criar(db, usuario_id, itens)
    if "erro" in resultado:
        return jsonify({"erro": resultado["erro"], "sucesso": False}), 400

    return jsonify({
        "dados": resultado,
        "sucesso": True,
        "mensagem": "Pedido criado com sucesso",
    }), 201


def listar_por_usuario(db, usuario_id):
    pedidos = pedido_model.get_por_usuario(db, usuario_id)
    return jsonify({"dados": pedidos, "sucesso": True}), 200


def listar_todos(db):
    pedidos = pedido_model.get_todos(db)
    return jsonify({"dados": pedidos, "sucesso": True}), 200


def atualizar_status(db, pedido_id, dados):
    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    novo_status = dados.get("status", "")
    if novo_status not in settings.STATUS_PEDIDO_VALIDOS:
        return jsonify({"erro": "Status inválido"}), 400

    pedido_model.atualizar_status(db, pedido_id, novo_status)
    return jsonify({"sucesso": True, "mensagem": "Status atualizado"}), 200


def relatorio_vendas(db):
    relatorio = pedido_model.relatorio_vendas(db)
    return jsonify({"dados": relatorio, "sucesso": True}), 200
