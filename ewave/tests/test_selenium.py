from clld.tests.util import TestWithSelenium

import ewave


class Tests(TestWithSelenium):
    app = ewave.main({}, **{'sqlalchemy.url': 'postgres://robert@/ewave'})
