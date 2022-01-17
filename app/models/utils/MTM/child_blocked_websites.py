from sqlalchemy import Table, Column, Integer, ForeignKey

from app import db

# Many To Many of Child and BlockedWebsites tables
child_blocked_websites = Table(
    'child_blocked_websites',
    db.metadata,
    Column('child_id', Integer, ForeignKey('Children.id')),
    Column('website_id', Integer, ForeignKey('BlockedWebsites.id'))
)
