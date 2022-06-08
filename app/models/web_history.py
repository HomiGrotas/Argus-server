from sqlalchemy import Column, Integer, ForeignKey, String, BOOLEAN, DateTime

from app import db


class WebHistory(db.Model):
    __tablename__ = 'WebHistory'

    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('Children.id'),  nullable=False)
    _url = Column(String(2048), nullable=False)
    _title = Column(String(2048), nullable=True)
    _date = Column(DateTime, nullable=False)
    _blocked = Column(BOOLEAN, nullable=False, default=False)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, new_url: str):
        self._url = new_url

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title: str):
        self._title = new_title

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, new_date):
        self._date = new_date

    @property
    def blocked(self):
        return self._blocked

    @blocked.setter
    def blocked(self, was_blocked: bool):
        self._blocked = was_blocked

    def info(self):
        return {
            'url': self.url,
            'title': self.title,
            'date': self.date.strftime("%Y-%m-%d %H:%M:%S"),
            'blocked': self.blocked,
        }
