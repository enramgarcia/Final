from app import db


class Settings(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    sunday_start = db.Column(db.Time, nullable=True)
    sunday_end = db.Column(db.Time, nullable=True)
    monday_start = db.Column(db.Time, nullable=True)
    monday_end = db.Column(db.Time, nullable=True)
    tuesday_start = db.Column(db.Time, nullable=True)
    tuesday_end = db.Column(db.Time, nullable=True)
    wednesday_start = db.Column(db.Time, nullable=True)
    wednesday_end = db.Column(db.Time, nullable=True)
    thursday_start = db.Column(db.Time, nullable=True)
    thursday_end = db.Column(db.Time, nullable=True)
    friday_start = db.Column(db.Time, nullable=True)
    friday_end = db.Column(db.Time, nullable=True)
    saturday_start = db.Column(db.Time, nullable=True)
    saturday_end = db.Column(db.Time, nullable=True)
    business_name = db.Column(db.String(length=80))
    system_email = db.Column(db.String(length=255))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
