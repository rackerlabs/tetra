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
from tetra.config import cfg
from tetra.data.database_client import DatabaseClient
from tetra.data.sql import db_connect

conf = cfg.CONF

DATABASE = {
    'drivername': 'postgres',
    'host': conf.sqlalchemy.host,
    'port': conf.sqlalchemy.port,
    'username': conf.sqlalchemy.username,
    'password': conf.sqlalchemy.password,
    'database': conf.sqlalchemy.database
}


class PostgresClient(DatabaseClient):

    def __init__(self):
        self.engine = None

    def connect(self):
        self.engine = db_connect(database_dict=DATABASE)

    def create(self, resource):
        data = resource.to_dict()
        query = resource.TABLE.insert().values(**data)
        result = self.engine.execute(query)
        resource.id = result.inserted_primary_key[0]
        return resource

    def create_many(self, resources):
        if not resources:
            return
        table = resources[0].TABLE
        result = self.engine.execute(table.insert(),
                                     [r.to_dict() for r in resources])
        result.close()

    def update(self, resource_id, resource):
        pass

    def delete(self, resource_id, resource_class):
        table = resource_class.TABLE
        query = table.delete().where(table.c.id == int(resource_id))
        result = self.engine.execute(query)
        result.close()

    def get(self, resource_id, resource_class):
        table = resource_class.TABLE
        query = table.select().where(table.c.id == int(resource_id))
        result = self.engine.execute(query)
        if result.rowcount == 0:
            return
        row = result.fetchone()
        data = {key: value for key, value in zip(result.keys(), row)}
        result.close()
        return resource_class.from_dict(data)

    def get_all(self, resource_class, query=None, limit=None, offset=None):
        if query is None:
            query = resource_class.TABLE.select()

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        result = self.engine.execute(query)
        rows = result.fetchall()
        data = []
        for row in rows:
            resource = {key: value for key, value in zip(result.keys(), row)}
            data.append(resource)
        result.close()
        return data
