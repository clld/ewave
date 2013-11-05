from path import path

from clld.tests.util import TestWithApp

import ewave


class Tests(TestWithApp):
    __cfg__ = path(ewave.__file__).dirname().joinpath('..', 'development.ini').abspath()
    __setup_db__ = False

    def test_home(self):
        self.app.get('/', status=200)
        self.app.get('/changes', status=200)

    def test_contributions(self):
        self.app.get('/languages', status=200)
        self.app.get('/languages?sEcho=1', xhr=True, status=200)
        self.app.get('/languages/1', status=200)
        self.app.get('/languages.geojson', status=200)

    def test_parameters(self):
        self.app.get('/parameters', status=200)
        self.app.get('/parameters?sEcho=1', xhr=True, status=200)
        self.app.get('/parameters/1', status=200)
        self.app.get('/parameters/1.geojson', status=200)
        self.app.get('/values?sEcho=1&parameter=1', xhr=True, status=200)

    def test_sources(self):
        self.app.get('/sources', status=200)
        self.app.get('/sources/apics', status=200)
