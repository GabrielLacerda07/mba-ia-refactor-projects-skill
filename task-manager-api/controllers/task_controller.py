from flask import jsonify
from sqlalchemy.orm import joinedload
from database import db
from models.task import Task
from models.user import User
from models.category import Category
from utils.datetime_utils import utcnow
from config import settings


def _parse_due_date(value):
    from datetime import datetime

    return datetime.strptime(value, "%Y-%m-%d")


def list_tasks():
    tasks = Task.query.options(
        joinedload(Task.user),
        joinedload(Task.category),
    ).all()
    result = []
    for task in tasks:
        data = task.to_dict()
        data["user_name"] = task.user.name if task.user else None
        data["category_name"] = task.category.name if task.category else None
        result.append(data)
    return jsonify(result), 200


def get_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({"error": "Task não encontrada"}), 404
    return jsonify(task.to_dict()), 200


def create_task(data):
    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    title = data.get("title")
    if not title:
        return jsonify({"error": "Título é obrigatório"}), 400
    if len(title) < settings.MIN_TITLE_LENGTH:
        return jsonify({"error": "Título muito curto"}), 400
    if len(title) > settings.MAX_TITLE_LENGTH:
        return jsonify({"error": "Título muito longo"}), 400

    status = data.get("status", "pending")
    priority = data.get("priority", settings.DEFAULT_PRIORITY)
    user_id = data.get("user_id")
    category_id = data.get("category_id")

    if status not in settings.VALID_STATUSES:
        return jsonify({"error": "Status inválido"}), 400
    if priority < settings.MIN_PRIORITY or priority > settings.MAX_PRIORITY:
        return jsonify({"error": "Prioridade deve ser entre 1 e 5"}), 400

    if user_id and not db.session.get(User, user_id):
        return jsonify({"error": "Usuário não encontrado"}), 404
    if category_id and not db.session.get(Category, category_id):
        return jsonify({"error": "Categoria não encontrada"}), 404

    task = Task(
        title=title,
        description=data.get("description", ""),
        status=status,
        priority=priority,
        user_id=user_id,
        category_id=category_id,
    )

    due_date = data.get("due_date")
    if due_date:
        try:
            task.due_date = _parse_due_date(due_date)
        except ValueError:
            return jsonify({"error": "Formato de data inválido. Use YYYY-MM-DD"}), 400

    tags = data.get("tags")
    if tags:
        task.tags = ",".join(tags) if isinstance(tags, list) else tags

    try:
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Erro ao criar task"}), 500


def update_task(task_id, data):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({"error": "Task não encontrada"}), 404
    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    if "title" in data:
        if len(data["title"]) < settings.MIN_TITLE_LENGTH:
            return jsonify({"error": "Título muito curto"}), 400
        if len(data["title"]) > settings.MAX_TITLE_LENGTH:
            return jsonify({"error": "Título muito longo"}), 400
        task.title = data["title"]

    if "description" in data:
        task.description = data["description"]

    if "status" in data:
        if data["status"] not in settings.VALID_STATUSES:
            return jsonify({"error": "Status inválido"}), 400
        task.status = data["status"]

    if "priority" in data:
        if data["priority"] < settings.MIN_PRIORITY or data["priority"] > settings.MAX_PRIORITY:
            return jsonify({"error": "Prioridade deve ser entre 1 e 5"}), 400
        task.priority = data["priority"]

    if "user_id" in data:
        if data["user_id"] and not db.session.get(User, data["user_id"]):
            return jsonify({"error": "Usuário não encontrado"}), 404
        task.user_id = data["user_id"]

    if "category_id" in data:
        if data["category_id"] and not db.session.get(Category, data["category_id"]):
            return jsonify({"error": "Categoria não encontrada"}), 404
        task.category_id = data["category_id"]

    if "due_date" in data:
        if data["due_date"]:
            try:
                task.due_date = _parse_due_date(data["due_date"])
            except ValueError:
                return jsonify({"error": "Formato de data inválido"}), 400
        else:
            task.due_date = None

    if "tags" in data:
        tags = data["tags"]
        task.tags = ",".join(tags) if isinstance(tags, list) else tags

    task.updated_at = utcnow()

    try:
        db.session.commit()
        return jsonify(task.to_dict()), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Erro ao atualizar"}), 500


def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({"error": "Task não encontrada"}), 404
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deletada com sucesso"}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Erro ao deletar"}), 500


def search_tasks(query, status, priority, user_id):
    tasks_query = Task.query

    if query:
        tasks_query = tasks_query.filter(
            db.or_(
                Task.title.like(f"%{query}%"),
                Task.description.like(f"%{query}%"),
            )
        )
    if status:
        tasks_query = tasks_query.filter(Task.status == status)
    if priority:
        tasks_query = tasks_query.filter(Task.priority == int(priority))
    if user_id:
        tasks_query = tasks_query.filter(Task.user_id == int(user_id))

    return jsonify([t.to_dict() for t in tasks_query.all()]), 200


def task_stats():
    total = Task.query.count()
    pending = Task.query.filter_by(status="pending").count()
    in_progress = Task.query.filter_by(status="in_progress").count()
    done = Task.query.filter_by(status="done").count()
    cancelled = Task.query.filter_by(status="cancelled").count()
    overdue_count = sum(1 for t in Task.query.all() if t.is_overdue())

    return jsonify({
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "done": done,
        "cancelled": cancelled,
        "overdue": overdue_count,
        "completion_rate": round((done / total) * 100, 2) if total > 0 else 0,
    }), 200
