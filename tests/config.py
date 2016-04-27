from oslo_config import cfg

cfg.CONF.register_group(cfg.OptGroup('api'))

cfg.CONF.register_opts([
    cfg.StrOpt('base_url'),
], group='api')

cfg.CONF(args=[], default_config_files=['tetra-test.conf'])
