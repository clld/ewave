from pyramid.view import view_config

from clld.db.models import common
from clld.db.meta import DBSession


@view_config(route_name="changes", renderer="changes.mako")
def changes(request):
    return {
        'varieties': {o.id: o for o in DBSession.query(common.Language)},
        'features': {o.id: o for o in DBSession.query(common.Parameter)},
    }
