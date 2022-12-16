from app import db


class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    schedule_date = db.Column(db.Date)
    schedule_time = db.Column(db.Time)
    is_active = db.Column(db.Boolean, default=True)
    reason = db.Column(db.String(length=255))
    email = db.Column(db.String(length=255))
    name = db.Column(db.String(length=255))
    last_name = db.Column(db.String(length=255))
    phone = db.Column(db.String(length=20))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
