from datetime import datetime, timedelta

import jwt
from flask import request, jsonify
from flask_jwt import jwt_required, JWT

from app import db, app
from models.schedule import Schedule
from models.settings import Settings
from models.user import User
from werkzeug.security import check_password_hash


def authenticate():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if username == '' or password == '':
        return {'error': 'Usuario o password incorrecto.'}, 401

    user = User.query.filter_by(username=username).first()

    if user is not None and check_password_hash(user.password, password):
        issued_at = datetime.utcnow() + timedelta(seconds=0)
        token = jwt.encode({
            'exp': datetime.utcnow() + timedelta(days=30),
            'iat': issued_at,
            'nbf': issued_at,
            'sub': user.id,
        }, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf-8')})

    return {'error': 'Usuario o password incorrecto.'}, 401


def identity(payload):
    user_id = payload['sub']
    return User.query.filter_by(id=user_id).first()


jwt_handler = JWT(app, authenticate, identity)


@jwt_required()
def schedules():
    data = []
    schedule_list = Schedule.query.all()

    for schedule in schedule_list:
        data.append({
            'id': schedule.id,
            'title': f'{schedule.name} {schedule.last_name}',
            'date': f'{schedule.schedule_date} {schedule.schedule_time}'
        })

    return data


@jwt_required()
def get_schedule(schedule):
    result = Schedule.query.filter_by(id=schedule).first()

    if result is None:
        return {'error': 'No se pudó encontrar el evento.'}, 404

    return {'schedule': result.as_dict()}


def get_schedule_time(date, settings_info):
    weekday = datetime.strptime(date, '%Y-%m-%d').weekday()

    # Lunes
    if weekday == 0:
        start_time = settings_info.monday_start
        end_time = settings_info.monday_end
    elif weekday == 1:
        start_time = settings_info.tuesday_start
        end_time = settings_info.tuesday_end
    elif weekday == 2:
        start_time = settings_info.wednesday_start
        end_time = settings_info.wednesday_end
    elif weekday == 3:
        start_time = settings_info.thursday_start
        end_time = settings_info.thursday_end
    elif weekday == 4:
        start_time = settings_info.friday_start
        end_time = settings_info.friday_end
    elif weekday == 5:
        start_time = settings_info.saturday_start
        end_time = settings_info.saturday_end
    else:
        start_time = settings_info.sunday_start
        end_time = settings_info.sunday_end

    return start_time, end_time


@jwt_required()
def update_schedule(schedule):
    try:
        result = Schedule.query.filter_by(id=schedule).first()

        if result is None:
            return {'error': 'No se pudó encontrar el evento.'}, 404

        data = request.get_json()

        schedule_time = data.get('schedule_time')
        schedule_date = data.get('schedule_date')

        if schedule_time == '' or schedule_date == '':
            return {'error': 'Todos los campos son requeridos.'}, 500

        setting = Settings.query.first()

        if setting is None:
            return {'error': 'No se ha configurado el sistema correctamente.'}, 500

        start_time, end_time = get_schedule_time(schedule_date, setting)

        if start_time is None or end_time is None:
            return {'success': False, 'error': 'No hay horario disponible.'}, 500

        exists = Schedule \
            .query \
            .filter_by(schedule_date=schedule_date, schedule_time=schedule_time) \
            .first()

        if exists is not None:
            return {'error': 'Ya existe un cita en esa fecha y hora.'}, 500

        result.schedule_time = schedule_time
        result.schedule_date = schedule_date

        db.session.commit()

        return {'success': True}, 202
    except Exception as e:
        return {'error': e}, 500


@jwt_required()
def delete_schedule(schedule):
    result = Schedule.query.filter_by(id=schedule).first()

    if result is None:
        return {'error': 'No se pudó encontrar el evento.'}, 404

    db.session.delete(result)
    db.session.commit()

    return {'success': True}, 202
