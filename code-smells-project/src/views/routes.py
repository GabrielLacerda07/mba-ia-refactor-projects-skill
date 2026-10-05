from flask import request
from src.controllers import produto_controller
from src.controllers import usuario_controller
from src.controllers import pedido_controller
from src.controllers import health_controller


def register_routes(app):
    app.add_url_rule("/", "index", health_controller.index, methods=["GET"])
    app.add_url_rule("/health", "health_check", health_controller.health_check, methods=["GET"])

    app.add_url_rule("/produtos", "listar_produtos", _listar_produtos, methods=["GET"])
    app.add_url_rule("/produtos/busca", "buscar_produtos", _buscar_produtos, methods=["GET"])
    app.add_url_rule("/produtos/<int:id>", "buscar_produto", _buscar_produto, methods=["GET"])
    app.add_url_rule("/produtos", "criar_produto", _criar_produto, methods=["POST"])
    app.add_url_rule("/produtos/<int:id>", "atualizar_produto", _atualizar_produto, methods=["PUT"])
    app.add_url_rule("/produtos/<int:id>", "deletar_produto", _deletar_produto, methods=["DELETE"])

    app.add_url_rule("/usuarios", "listar_usuarios", _listar_usuarios, methods=["GET"])
    app.add_url_rule("/usuarios/<int:id>", "buscar_usuario", _buscar_usuario, methods=["GET"])
    app.add_url_rule("/usuarios", "criar_usuario", _criar_usuario, methods=["POST"])
    app.add_url_rule("/login", "login", _login, methods=["POST"])

    app.add_url_rule("/pedidos", "criar_pedido", _criar_pedido, methods=["POST"])
    app.add_url_rule("/pedidos", "listar_todos_pedidos", _listar_todos_pedidos, methods=["GET"])
    app.add_url_rule(
        "/pedidos/usuario/<int:usuario_id>",
        "listar_pedidos_usuario",
        _listar_pedidos_usuario,
        methods=["GET"],
    )
    app.add_url_rule(
        "/pedidos/<int:pedido_id>/status",
        "atualizar_status_pedido",
        _atualizar_status_pedido,
        methods=["PUT"],
    )
    app.add_url_rule("/relatorios/vendas", "relatorio_vendas", _relatorio_vendas, methods=["GET"])


def _listar_produtos():
    return produto_controller.listar()


def _buscar_produtos():
    return produto_controller.buscar(
        request.args.get("q", ""),
        request.args.get("categoria", None),
        request.args.get("preco_min", None),
        request.args.get("preco_max", None),
    )


def _buscar_produto(id):
    return produto_controller.buscar_por_id(id)


def _criar_produto():
    return produto_controller.criar(request.get_json())


def _atualizar_produto(id):
    return produto_controller.atualizar(id, request.get_json())


def _deletar_produto(id):
    return produto_controller.deletar(id)


def _listar_usuarios():
    return usuario_controller.listar()


def _buscar_usuario(id):
    return usuario_controller.buscar_por_id(id)


def _criar_usuario():
    return usuario_controller.criar(request.get_json())


def _login():
    return usuario_controller.login(request.get_json())


def _criar_pedido():
    return pedido_controller.criar(request.get_json())


def _listar_todos_pedidos():
    return pedido_controller.listar_todos()


def _listar_pedidos_usuario(usuario_id):
    return pedido_controller.listar_por_usuario(usuario_id)


def _atualizar_status_pedido(pedido_id):
    return pedido_controller.atualizar_status(pedido_id, request.get_json())


def _relatorio_vendas():
    return pedido_controller.relatorio_vendas()
