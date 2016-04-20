from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
sensor = Table('sensor', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('Serial', String(length=64)),
    Column('Type', String(length=64)),
    Column('Location', String(length=64)),
    Column('LastReading', DateTime),
    Column('Interval', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['sensor'].columns['Location'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['sensor'].columns['Location'].drop()
