from flask import request

from app import db
from models.settings import Settings
from models.user import User

from werkzeug.security import generate_password_hash


def edit():
    try:
        setting = Settings.query.first()

        return setting.as_dict(), 202
    except Exception as e:
        return {'success': False, 'error': e}, 500


def update():
    try:
        setting = Settings.query.first()
        data = request.get_json()

        sunday_start = data.get('sundayStart')
        sunday_end = data.get('sundayEnd')
        monday_start = data.get('mondayStart')
        monday_end = data.get('mondayEnd')
        tuesday_start = data.get('tuesdayStart')
        tuesday_end = data.get('tuesdayEnd')
        wednesday_start = data.get('wednesdayStart')
        wednesday_end = data.get('wednesdayEnd')
        thursday_start = data.get('thursdayStart')
        thursday_end = data.get('thursdayEnd')
        friday_start = data.get('fridayStart')
        friday_end = data.get('fridayEnd')
        saturday_start = data.get('saturdayStart')
        saturday_end = data.get('saturdayEnd')
        business_name = data.get('businessName')
        system_email = data.get('systemEmail')

        if setting is None:
            new_setting = Settings(
                sunday_start=sunday_start,
                sunday_end=sunday_end,
                monday_start=monday_start,
                monday_end=monday_end,
                tuesday_start=tuesday_start,
                tuesday_end=tuesday_end,
                wednesday_start=wednesday_start,
                wednesday_end=wednesday_end,
                thursday_start=thursday_start,
                thursday_end=thursday_end,
                friday_start=friday_start,
                friday_end=friday_end,
                saturday_start=saturday_start,
                saturday_end=saturday_end,
                business_name=business_name,
                system_email=system_email
            )

            user = User.query.filter_by(username='admin').first()

            if user is None:
                db.session.add(User(username='admin', password=generate_password_hash('123456')))
                db.session.commit()

            db.session.add(new_setting)
        else:
            setting.sunday_start = sunday_start
            setting.sunday_end = sunday_end
            setting.monday_start = monday_start
            setting.monday_end = monday_end
            setting.tuesday_start = tuesday_start
            setting.tuesday_end = tuesday_end
            setting.wednesday_start = wednesday_start
            setting.wednesday_end = wednesday_end
            setting.thursday_start = thursday_start
            setting.thursday_end = thursday_end
            setting.friday_start = friday_start
            setting.friday_end = friday_end
            setting.saturday_start = saturday_start
            setting.saturday_end = saturday_end
            setting.business_name = business_name
            setting.system_email = system_email

        db.session.commit()

        return {'success': True}, 202
    except Exception as e:
        return {'success': False, 'error': e}, 500

