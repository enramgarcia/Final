from datetime import date, time
from json import JSONEncoder

from celery import Celery
from flask_mail import Mail, Message
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            elif isinstance(obj, time):
                if time is None:
                    return None

                return f'{obj.isoformat("minutes")}'
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app = Flask(__name__)
app.config.from_object('config')
app.json_encoder = CustomJSONEncoder
CORS(app, resources={r'/*': {'origins': '*'}})

db = SQLAlchemy(app)
mail = Mail(app)

celery = Celery(__name__)
celery.conf.broker_url = app.config.get('REDIS_SERVER')
celery.conf.result_backend = app.config.get('REDIS_SERVER')


@celery.task(name='send_email')
def send_email(info):
    msg = Message(
        'Se ha agendado su cita.',
        sender=info.system.email,
        recipients=[info.meeting.email])

    msg.html = f"Estimado(a) {info.meeting.name},<br><br>" \
               f"Se ha agendado su cita para el {info.meeting.date} a las {info.meeting.time}.<br><br>" \
               f"Atentamente,<br>" \
               f"{info.system.business_name}"
    mail.send(msg)


from routes.settings_routes import settings_blueprint
app.register_blueprint(settings_blueprint, url_prefix='/settings')

from routes.schedules_routes import schedules_blueprint
app.register_blueprint(schedules_blueprint, url_prefix='/schedules')

from routes.auth_routes import auth_blueprint
app.register_blueprint(auth_blueprint)

from routes.admin_routes import admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()


