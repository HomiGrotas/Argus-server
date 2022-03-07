from sqlalchemy import Column, Integer, String


from app import db


class BlockedApps(db.Model):
    __tablename__ = "BlockedApps"
    id = Column(Integer, primary_key=True)
    _app = Column(String(253), nullable=False)

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, new_app: str):
        self._app = new_app

    def info(self):
        return {
            'id': self.id,
            'app': self.app,
        }
