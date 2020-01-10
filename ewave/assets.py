import pathlib

from clld.web.assets import environment

import ewave


environment.append_path(
    str(pathlib.Path(ewave.__file__).parent.joinpath('static')), url='/ewave:static/')
environment.load_path = list(reversed(environment.load_path))
