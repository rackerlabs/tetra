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
from sqlalchemy import (Table, Column, MetaData, ForeignKey, Index,
                        UniqueConstraint)
from sqlalchemy import Integer, String, Text

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL


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
    Index('build_index', 'project_id', 'id')
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
    Index('result_index', 'project_id', 'build_id', 'result')
)

build_tags_table = Table(
    'build_tags', metadata,
    Column('id', Integer, nullable=False, primary_key=True,
           autoincrement=True),
    Column('build_id', Integer, nullable=False),
    Column('tag_id', Integer, nullable=False),
)

result_tags_table = Table(
    'result_tags', metadata,
    Column('id', Integer, nullable=False, primary_key=True,
           autoincrement=True),
    Column('result_id', Integer, nullable=False),
    Column('tag_id', Integer, nullable=False),
)

tags_table = Table(
    'tags', metadata,
    Column('id', Integer, nullable=False, primary_key=True,
           autoincrement=True),
    Column('key', Text, nullable=False),
    Column('value', Text, nullable=False),
    UniqueConstraint('key', 'value')
)


def db_connect(database_dict):
    engine = create_engine(URL(**database_dict))
    metadata.create_all(engine)
    return engine
