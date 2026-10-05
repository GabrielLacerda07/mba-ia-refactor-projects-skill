from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"erro": "Não encontrado", "sucesso": False}), 404

    @app.errorhandler(Exception)
    def handle_exception(error):
        if isinstance(error, HTTPException):
            return error
        app.logger.exception(error)
        return jsonify({"erro": "Erro interno", "sucesso": False}), 500
