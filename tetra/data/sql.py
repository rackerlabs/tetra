"""
Copyright 2016 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from sqlalchemy import (
    Table, Column, MetaData, ForeignKey, Index, Integer, String, Text
)

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

# plain JSON is inferior to JSONB in postgres.
# JSONB supports indexing and is stored as binary.
# TODO: other database support?
from sqlalchemy.dialects.postgresql import JSONB


metadata = MetaData()


projects_table = Table(
    'projects', metadata,
    Column('id', Integer, nullable=False, primary_key=True,
           autoincrement=True),
    Column('name', String(256), nullable=False)
)

builds_table = Table(
    'builds', metadata,
    Column('id', Integer, nullable=False, primary_key=True,
           autoincrement=True),
    Column('project_id', ForeignKey(projects_table.c.id, ondelete='CASCADE'),
           nullable=False),
    Column('name', String(256), nullable=False),
    Column('build_url', String(256), nullable=True),
    Column('region', String(256), nullable=True),
    Column('environment', String(256), nullable=True),
    Column('status', String(256), nullable=True),
    Column('tags', JSONB, nullable=False),
    Index('build_index', 'project_id', 'id'),
    Index('build_tags_index', 'tags', postgresql_using='gin'),
)

results_table = Table(
    'results', metadata,
    Column('id', Integer, nullable=False, primary_key=True,
           autoincrement=True),
    Column('project_id', ForeignKey(projects_table.c.id, ondelete='CASCADE'),
           nullable=False),
    Column('build_id', ForeignKey(builds_table.c.id, ondelete='CASCADE'),
           nullable=False),
    Column('test_name', String(256), nullable=False),
    Column('timestamp', Integer, nullable=False),
    Column('result', String(256), nullable=False),
    Column('result_message', Text, nullable=True),
    Column('tags', JSONB, nullable=False),
    Index('result_index', 'project_id', 'build_id', 'result'),
    Index('result_tags_index', 'tags', postgresql_using='gin'),
)


def db_connect(database_dict):
    engine = create_engine(URL(**database_dict))
    metadata.create_all(engine)
    return engine
