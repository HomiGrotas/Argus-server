from app import db


class WebHistory(db.Model):
    __tablename__ = 'WebHistory'

    record_id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('Children.id'),  nullable=False)
    url = db.Column(db.String, nullable=False)
    date = db.Column(db.DATETIME, nullable=False)
