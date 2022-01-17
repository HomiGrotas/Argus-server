from sqlalchemy import Column, Integer, String


from app import db


class BlockedWebsites(db.Model):
    __tablename__ = "BlockedWebsites"
    id = Column(Integer, primary_key=True)
    _domain = Column(String(253), nullable=False)

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, set_domain: str):
        self._domain = set_domain

    def info(self):
        return {
            'id': self.id,
            'domain': self.domain,
        }
