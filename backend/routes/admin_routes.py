from flask import Blueprint
from controllers.AdminController import schedules, get_schedule, update_schedule, delete_schedule, authenticate

admin_blueprint = Blueprint('admin', __name__)

admin_blueprint.route('/login', methods=['POST'])(authenticate)
admin_blueprint.route('/schedules', methods=['GET'])(schedules)
admin_blueprint.route('/schedules/<schedule>', methods=['GET'])(get_schedule)
admin_blueprint.route('/schedules/<schedule>/edit', methods=['POST'])(update_schedule)
admin_blueprint.route('/schedules/<schedule>', methods=['DELETE'])(delete_schedule)

