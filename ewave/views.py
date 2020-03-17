from clld.db.meta import DBSession
from clld.db.models import common


def introduction(req):
    return {'vcount': DBSession.query(common.Language).count()}
