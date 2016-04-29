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
from oslo_config import cfg
import os.path

_LOCATIONS = (
    os.path.realpath('tetra.conf'),
    os.path.realpath('etc/tetra/tetra.conf'),
    '/etc/tetra/tetra.conf',
)

cfg.CONF.register_group(cfg.OptGroup('sqlalchemy'))

cfg.CONF.register_opts([
    cfg.StrOpt('engine', default='postgres'),
    cfg.StrOpt('host', default='localhost'),
    cfg.IntOpt('port', default=5432),
    cfg.StrOpt('username', default='postgres'),
    cfg.StrOpt('password'),
    cfg.StrOpt('database', default='tetra-ab'),
], group='sqlalchemy')


def _find_config_file(locations):
    for path in locations:
        if os.path.exists(path):
            return path
    raise Exception("Failed to find config at any of these paths: {0}"
                    .format(locations))

_CONFIG_FILE = _find_config_file(_LOCATIONS)

cfg.CONF(args=[], default_config_files=[_CONFIG_FILE])
