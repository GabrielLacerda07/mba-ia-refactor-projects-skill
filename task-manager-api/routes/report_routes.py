from flask import Blueprint, request
from controllers import report_controller

report_bp = Blueprint("reports", __name__)


@report_bp.route("/reports/summary", methods=["GET"])
def summary_report():
    return report_controller.summary_report()


@report_bp.route("/reports/user/<int:user_id>", methods=["GET"])
def user_report(user_id):
    return report_controller.user_report(user_id)


@report_bp.route("/categories", methods=["GET"])
def get_categories():
    return report_controller.list_categories()


@report_bp.route("/categories", methods=["POST"])
def create_category():
    return report_controller.create_category(request.get_json())


@report_bp.route("/categories/<int:cat_id>", methods=["PUT"])
def update_category(cat_id):
    return report_controller.update_category(cat_id, request.get_json())


@report_bp.route("/categories/<int:cat_id>", methods=["DELETE"])
def delete_category(cat_id):
    return report_controller.delete_category(cat_id)
