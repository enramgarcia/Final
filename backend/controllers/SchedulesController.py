import datetime

from flask import request

from app import db, send_email
from models.schedule import Schedule
from models.settings import Settings


def index():
    return [i.as_dict() for i in Schedule.query.all()]


def get_time(t):
    return datetime.datetime.combine(datetime.date.today(), t)


def generate_time(start, end, schedules_list):
    times = []
    start_time = get_time(start)
    difference = int((get_time(end) - get_time(start)).seconds / 3600)

    for i in range(difference):
        found = False
        temp_time = (start_time + datetime.timedelta(hours=i)).time()

        for x in schedules_list:
            if temp_time == x.schedule_time:
                found = True
                break

        if found is False:
            times.append(temp_time)

    return times


def create():
    try:
        settings_info = Settings.query.first()

        if settings_info is None:
            return {'error': 'No se encuentra la configuración de sistema.'}, 500

        qs = request.args
        date = qs.get('date')

        weekday = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()

        schedules_list = Schedule.query.filter_by(schedule_date=date).all()

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

        if start_time is None or end_time is None:
            return {'success': False, 'error': 'No hay horario disponible.'}, 500

        times = generate_time(start_time, end_time, schedules_list)

        return {'times': times}, 202
    except Exception as e:
        return {'success': False, 'error': str(e)}, 500


def store():
    try:
        data = request.get_json()

        setting_info = Settings.query.first()

        if setting_info is None:
            return {'message': 'No se encontró la configuración de sistema.'}, 500

        name = data.get('name')
        last_name = data.get('lastName')
        email = data.get('email')
        phone = data.get('phone')
        reason = data.get('reason')
        selected_date = data.get('selectedDate')
        selected_time = data.get('selectedTime')

        meeting = Schedule(
            name=name,
            last_name=last_name,
            email=email,
            phone=phone,
            reason=reason,
            schedule_date=selected_date,
            schedule_time=selected_time)

        db.session.add(meeting)

        send_email.delay({
            'system': {
                'email': setting_info.system_email,
                'business_name': setting_info.business_name,
            },
            'meeting': {
                'email': meeting.email,
                'name': f'{meeting.name} {meeting.last_name}',
                'date': f'{meeting.schedule_date}',
                'time': f'{meeting.schedule_time}',
            }
        })

        db.session.commit()

        return {'success': True}, 201
    except Exception as e:
        return {'success': False, 'error': e}, 500
