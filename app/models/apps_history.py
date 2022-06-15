from sqlalchemy import Column, Integer, ForeignKey, String, BOOLEAN
from datetime import datetime

from .utils.types import CreatedAt
from app import db


class AppsHistory(db.Model, CreatedAt):
    __tablename__ = 'AppsHistory'

    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('Children.id'),  nullable=False)
    _opened = Column(BOOLEAN, nullable=False)  # opened/ closed
    _name = Column(String(2048), nullable=False)
    _blocked = Column(BOOLEAN, nullable=False)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    @property
    def blocked(self) -> bool:
        return self._blocked

    @blocked.setter
    def blocked(self, was_blocked: bool):
        self._blocked = was_blocked

    @property
    def state(self):
        return 'opened' if self._opened else 'closed'

    @state.setter
    def state(self, state: str):
        assert state in ['closed', 'opened'], "Unknown state!"
        self._opened = state == 'opened'

    def info(self) -> dict:
        return {
            "child_id": self.child_id,
            "state": self.state,
            "app_name": self._name,
            "blocked": self._blocked,
            'date': self.created_at.strftime("%d/%m/%y %H:%M:%S"),
        }
