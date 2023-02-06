from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = [
    # For DB management
    'sqlalchemy[asyncio]          >= 1, < 2',
    'databases[asyncpg,aiosqlite] >= 0.6, < 2',
    'python-dateutil              >= 2, < 4',
    'sqlalchemy-utils             >= 0, < 1',
    'psycopg2-binary              >= 2, < 3',
    'python-slugify               >= 7',

    # For server
    'starlette                    >= 0, < 1',
    'fastapi[all]                 >= 0, < 1',
]

dev_requires = [
    'pytest         >= 7, < 8',
    'pytest-cov     >= 4, < 5',
    'pytest-asyncio >= 0.17, < 1',
    'mypy           >= 0.812',
    'uvicorn[standard] >= 0, < 1',
    'requests          >= 2, < 3', # for starlette testing
    'types-python-dateutil >= 2, < 3', # Types for dateutil (for mypy)
]

setup(
    name='sl-dbserver',
    version='0.0.0',
    license='MIT',
    description='Springless Database Server',
    long_description=README,
    author='cogs',
    author_email='cogs@springless.com',
    url='https://github.com/Springless/sl-dbserver',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['sl'],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require={
        'dev': dev_requires,
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Toptic :: Internet :: WWW/HTTP',
    ],
    entry_pointts={
        'console_scripts': [
            'sl-dbserver=sl.dbserver.cli:main',
        ],
    },
    keywords='sl springless database server testing postgresql',
)
