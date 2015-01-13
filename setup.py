from setuptools import setup, find_packages

requires = [
    'clld>=0.28',
    'clldmpg>=0.2',
]

tests_require = [
    'WebTest >= 1.3.1', # py3 compat
    'mock',
]

setup(name='ewave',
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
      install_requires=requires,
      tests_require=tests_require,
      test_suite="ewave",
      entry_points="""\
      [paste.app_factory]
      main = ewave:main
      """,
      )
