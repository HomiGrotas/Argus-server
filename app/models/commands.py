from app import db
from app.models.utils import CreatedAt


class Command(CreatedAt, db.Model):
    __tablename__ = 'Commands'

    command_id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String, nullable=False)
