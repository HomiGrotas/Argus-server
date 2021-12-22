from sqlalchemy import Column, Integer, String

from app import db


class BlockedWebsites(db.Model):
    id = Column(Integer, primary_key=True)
    domain = Column(String(253), nullable=False)
