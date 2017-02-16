from clldutils.path import Path
from clld.tests.util import TestWithApp

import ewave


class Tests(TestWithApp):
    __cfg__ = Path(ewave.__file__).parent.joinpath('..', 'development.ini').resolve()

    def test_home(self):
        self.app.get_html('/')
        self.app.get_html('/changes')

    def test_contributions(self):
        self.app.get_html('/languages')
        self.app.get_dt('/languages')
        self.app.get_dt('/languages?iSortingCols=1&iSortCol_0=3&sSearch_3=a')
        self.app.get_dt('/languages?iSortingCols=1&iSortCol_0=4&sSearch_4=a')
        self.app.get_html('/languages/1')
        self.app.get_json('/languages.geojson')

    def test_sentences(self):
        self.app.get_dt('/sentences?iSortingCols=1&iSortCol_0=3&sSearch_3=a')

    def test_parameters(self):
        self.app.get_html('/parameters')
        self.app.get_dt('/parameters?iSortingCols=1&iSortCol_0=4&sSearch_4=a')
        self.app.get_html('/parameters/1')
        self.app.get_json('/parameters/1.geojson')

    def test_values(self):
        self.app.get_dt('/values')
        self.app.get_dt('/values?language=1')
        self.app.get_dt('/values?parameter=1&iSortingCols=1&iSortCol_0=2&sSearch_2=a')
        self.app.get_dt('/values?parameter=1&iSortingCols=1&iSortCol_0=3&sSearch_3=a')

    def test_sources(self):
        self.app.get_html('/sources')
        self.app.get_html('/sources/apics')
