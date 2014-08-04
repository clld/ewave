import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'clld>=0.16',
    'clldmpg>=0.2',
    'pyramid>=1.5',
    'SQLAlchemy>=0.9',
    'transaction',
    'pyramid_tm',
    'zope.sqlalchemy',
    'waitress',
    ]

setup(name='ewave',
      version='0.0',
      description='ewave',
      long_description=README + '\n\n' + CHANGES,
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
      install_requires=requires,
      tests_require=requires,
      test_suite="ewave",
      entry_points="""\
      [paste.app_factory]
      main = ewave:main
      """,
      )
