from setuptools import setup, find_packages

requires = [
    'clld>=3.2.0',
    'clldmpg>=2.0.0',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'mock==1.0',
]

setup(
    name='ewave',
    version='0.0',
    description='ewave',
    long_description='',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'clld~=4.2',
        'clldmpg~=3.1',
        'sqlalchemy',
        'waitress',
    ],
    extras_require={
        'dev': [
            'flake8',
            'psycopg2',
            'tox'
        ],
        'test': [
            'mock',
            'pytest>=3.1',
            'pytest-clld',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
            'selenium',
            'zope.component>=3.11.0',
        ],
    },
    test_suite="ewave",
    entry_points="""\
    [paste.app_factory]
    main = ewave:main
    """)
