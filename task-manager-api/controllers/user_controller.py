from flask import jsonify
from database import db
from models.user import User
from models.task import Task
from config import settings
import re


def list_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "active": user.active,
            "created_at": str(user.created_at),
            "task_count": len(user.tasks),
        })
    return jsonify(result), 200


def get_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    data = user.to_dict()
    data["tasks"] = [t.to_dict() for t in Task.query.filter_by(user_id=user_id).all()]
    return jsonify(data), 200


def create_user(data):
    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    if not name:
        return jsonify({"error": "Nome é obrigatório"}), 400
    if not email:
        return jsonify({"error": "Email é obrigatório"}), 400
    if not password:
        return jsonify({"error": "Senha é obrigatória"}), 400
    if not re.match(r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", email):
        return jsonify({"error": "Email inválido"}), 400
    if len(password) < settings.MIN_PASSWORD_LENGTH:
        return jsonify({"error": "Senha deve ter no mínimo 4 caracteres"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email já cadastrado"}), 409
    if role not in settings.VALID_ROLES:
        return jsonify({"error": "Role inválido"}), 400

    user = User(name=name, email=email, role=role)
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Erro ao criar usuário"}), 500


def update_user(user_id, data):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        if not re.match(r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", data["email"]):
            return jsonify({"error": "Email inválido"}), 400
        existing = User.query.filter_by(email=data["email"]).first()
        if existing and existing.id != user_id:
            return jsonify({"error": "Email já cadastrado"}), 409
        user.email = data["email"]
    if "password" in data:
        if len(data["password"]) < settings.MIN_PASSWORD_LENGTH:
            return jsonify({"error": "Senha muito curta"}), 400
        user.set_password(data["password"])
    if "role" in data:
        if data["role"] not in settings.VALID_ROLES:
            return jsonify({"error": "Role inválido"}), 400
        user.role = data["role"]
    if "active" in data:
        user.active = data["active"]

    try:
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Erro ao atualizar"}), 500


def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    for task in Task.query.filter_by(user_id=user_id).all():
        db.session.delete(task)

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuário deletado com sucesso"}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Erro ao deletar"}), 500


def get_user_tasks(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    return jsonify([t.to_dict() for t in Task.query.filter_by(user_id=user_id).all()]), 200


def login(data):
    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Credenciais inválidas"}), 401
    if not user.active:
        return jsonify({"error": "Usuário inativo"}), 403

    return jsonify({
        "message": "Login realizado com sucesso",
        "user": user.to_dict(),
        "token": f"fake-jwt-token-{user.id}",
    }), 200
