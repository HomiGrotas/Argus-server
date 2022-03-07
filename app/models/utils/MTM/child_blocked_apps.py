from sqlalchemy import Table, Column, Integer, ForeignKey

from app import db

# Many To Many of Child and BlockedWebsites tables
child_blocked_apps = Table(
    'child_blocked_apps',
    db.metadata,
    Column('child_id', Integer, ForeignKey('Children.id')),
    Column('app_id', Integer, ForeignKey('BlockedApps.id'))
)
