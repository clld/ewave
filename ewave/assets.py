from clld.web.assets import environment
from path import path

import ewave


environment.append_path(
    path(ewave.__file__).dirname().joinpath('static'), url='/ewave:static/')
environment.load_path = list(reversed(environment.load_path))
