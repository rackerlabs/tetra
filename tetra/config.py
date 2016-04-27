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
from six.moves.configparser import ConfigParser
import os.path

_CONFIG_FILE_LOCATIONS = (
    os.path.realpath('tetra.conf'),
    os.path.realpath('etc/tetra/tetra.conf'),
    '/etc/tetra/tetra.conf',
)


def _find_config_file(locations):
    for path in locations:
        if os.path.exists(path):
            return path
    raise Exception("Failed to find config at any of these paths: {0}"
                    .format(locations))

_CONFIG_FILE = _find_config_file(_CONFIG_FILE_LOCATIONS)

_CFG_DEFAULTS = {
    'sqlalchemy': {
        'engine': 'postgres',
        'host': 'localhost',
        'port': '5432',
        'username': 'postgres',
        'password': '',
        'database': 'tetra-db',
    }
}


class ConfigSection(object):
    def add_option(self, option, value):
        self.__setattr__(option, value)


class TetraConfiguration(object):

    def __init__(self, default_cfg):
        self.load_defaults(default_cfg)

    def load_defaults(self, default_cfg):
        for section_name in default_cfg:
            section = ConfigSection()
            for option in default_cfg[section_name]:
                section.add_option(option, default_cfg[section_name][option])
            self.__setattr__(section_name, section)

    def load_config(self, cfg_parser):
        for section_name in cfg_parser.sections():
            section = ConfigSection()
            for option in cfg_parser.options(section_name):
                section.add_option(option, cfg_parser.get(section_name,
                                                          option))
            self.__setattr__(section_name, section)


_cfg = TetraConfiguration(_CFG_DEFAULTS)


def load_config(config_file=_CONFIG_FILE):
    cfg_parser = ConfigParser()
    if not os.path.isfile(config_file):
        raise Exception(
            'configuration file not found: {0}'.format(config_file))
    cfg_parser.read(config_file)
    _cfg.load_config(cfg_parser)


def get_config():
    config = _CONFIG_FILE
    local_path = '.{0}'.format(_CONFIG_FILE)
    if os.path.exists(local_path):
        config = os.path.abspath(local_path)

    load_config(config_file=config)
    return _cfg
