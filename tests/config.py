from oslo_config import cfg
import os

_LOCATIONS = (
    os.path.realpath('tetra-test.conf'),
    os.path.realpath('etc/tetra/tetra-test.conf'),
    '/etc/tetra/tetra-test.conf',
)

cfg.CONF.register_group(cfg.OptGroup('api'))

cfg.CONF.register_opts([
    cfg.StrOpt('base_url'),
], group='api')


def _find_config_file(locations):
    for path in locations:
        if os.path.exists(path):
            return path
    raise Exception("Failed to find config at any of these paths: {0}"
                    .format(locations))


_CONFIG_FILE = _find_config_file(_LOCATIONS)

cfg.CONF(args=[], default_config_files=[_CONFIG_FILE])
