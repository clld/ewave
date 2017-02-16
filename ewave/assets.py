from clld.web.assets import environment
from clldutils.path import Path

import ewave


environment.append_path(
    Path(ewave.__file__).parent.joinpath('static').as_posix(), url='/ewave:static/')
environment.load_path = list(reversed(environment.load_path))
