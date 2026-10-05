from datetime import datetime
import re
import uuid
from config import settings
from utils.datetime_utils import utcnow


def format_date(date_obj):
    return str(date_obj) if date_obj else None


def calculate_percentage(part, total):
    if total == 0:
        return 0
    return round((part / total) * 100, 2)


def validate_email(email):
    return bool(re.match(r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", email))


def sanitize_string(value):
    return value.strip() if value else value


def generate_id():
    return str(uuid.uuid4())


def log_action(action, details=None):
    print(f"[{utcnow()}] ACTION: {action}")
    if details:
        print(f"  DETAILS: {details}")


def parse_date(date_string):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(date_string, fmt)
        except (TypeError, ValueError):
            continue
    return None


def is_valid_color(color):
    return bool(color and len(color) == 7 and color[0] == "#")


def process_task_data(data, existing_task=None):
    result = {}

    if "title" in data:
        title = (data["title"] or "").strip()
        if not title:
            return None, "Título não pode ser vazio"
        if not (settings.MIN_TITLE_LENGTH <= len(title) <= settings.MAX_TITLE_LENGTH):
            return None, "Título deve ter entre 3 e 200 caracteres"
        result["title"] = title

    if "description" in data:
        result["description"] = data["description"]

    if "status" in data:
        if data["status"] not in settings.VALID_STATUSES:
            return None, "Status inválido"
        result["status"] = data["status"]

    if "priority" in data:
        try:
            priority = int(data["priority"])
        except (TypeError, ValueError):
            return None, "Prioridade inválida"
        if not (settings.MIN_PRIORITY <= priority <= settings.MAX_PRIORITY):
            return None, "Prioridade deve ser entre 1 e 5"
        result["priority"] = priority

    if "due_date" in data:
        if data["due_date"]:
            parsed = parse_date(data["due_date"])
            if not parsed:
                return None, "Data inválida"
            result["due_date"] = parsed
        else:
            result["due_date"] = None

    if "tags" in data:
        tags = data["tags"]
        result["tags"] = ",".join(tags) if isinstance(tags, list) else tags

    return result, None


VALID_STATUSES = settings.VALID_STATUSES
VALID_ROLES = settings.VALID_ROLES
MAX_TITLE_LENGTH = settings.MAX_TITLE_LENGTH
MIN_TITLE_LENGTH = settings.MIN_TITLE_LENGTH
MIN_PASSWORD_LENGTH = settings.MIN_PASSWORD_LENGTH
DEFAULT_PRIORITY = settings.DEFAULT_PRIORITY
DEFAULT_COLOR = settings.DEFAULT_COLOR
