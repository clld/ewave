from clld.db.models import common
from clld.db.meta import DBSession


def changes(request):
    return {
        'varieties': {o.id: o for o in DBSession.query(common.Language)},
        'features': {o.id: o for o in DBSession.query(common.Parameter)},
    }
