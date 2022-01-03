from sqlalchemy import Table, ForeignKey, Column, Integer

from app import db

# Many To Many between Child and BlockedWebsites tables
child_blocked_websites = Table(
    'child_blocked_websites',
    db.metadata,
    Column('child_id', ForeignKey('Children.id'), primary_key=True),
    Column('website_id', ForeignKey('BlockedWebsites.id'), primary_key=True)
)
