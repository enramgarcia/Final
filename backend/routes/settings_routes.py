from flask import Blueprint
from controllers.SettingsController import edit, update

settings_blueprint = Blueprint('settings_blueprint', __name__)

settings_blueprint.route('/', methods=['GET'])(edit)
settings_blueprint.route('/create', methods=['POST'])(update)
