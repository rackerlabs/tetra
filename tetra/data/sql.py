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
from sqlalchemy import Table, Column, MetaData
from sqlalchemy import Integer, String

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL


metadata = MetaData()
results_table = Table(
    'results', metadata,
    Column('id', Integer, nullable=False, primary_key=True,
           autoincrement=True),
    Column('test_name', String(256), nullable=False),
    Column('test_suite', String(256), nullable=True),
    Column('test_suite_id', String(256), nullable=True),
    Column('timestamp', Integer, nullable=False),
    Column('result', String(256), nullable=False),
    Column('result_message', String(2048), nullable=True),
    Column('region', String(256), nullable=True),
    Column('environment', String(256), nullable=True),
    Column('extra_data', String(512), nullable=True)
)


def db_connect(database_dict):
    engine = create_engine(URL(**database_dict))
    metadata.create_all(engine)
    return engine
