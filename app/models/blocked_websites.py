from sqlalchemy import Column, Integer, String

from app import db


class BlockedWebsites(db.Model):
    __tablename__ = "BlockedWebsites"
    id = Column(Integer, primary_key=True)
    domain = Column(String(253), nullable=False)

    def info(self):
        return {
            'id': self.id,
            'domain': self.domain,
        }
