from setuptools import setup

setup_params = dict(
    name='tetra',
    version='0.0.1',
    url='https://github.com/rackerlabs/tetra',
    packages=['tetra'],
    install_requires=[
        'celery',
        'falcon',
        'oslo.config',
        'psycopg2',
        'sqlalchemy',
        'xunitparser',
    ],
)

if __name__ == '__main__':
    setup(**setup_params)
