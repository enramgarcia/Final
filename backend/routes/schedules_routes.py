from flask import Blueprint
from controllers.SchedulesController import index, create, store

schedules_blueprint = Blueprint('schedules_blueprint', __name__)

schedules_blueprint.route('/')(index)
schedules_blueprint.route('/create', methods=['GET'])(create)
schedules_blueprint.route('/create', methods=['POST'])(store)
