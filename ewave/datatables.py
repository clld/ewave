from sqlalchemy.orm import aliased

from clld.db.util import get_distinct_values
from clld.db.meta import DBSession
from clld.web import datatables
from clld.web.datatables.base import Col, LinkCol
from clld.web.datatables.contribution import ContributorsCol, CitationCol
from clld.web.util.helpers import map_marker_img

from ewave.models import Region, VarietyType, Variety


class RegionCol(Col):
    def format(self, item):
        return item.variety.region.name

    def search(self, qs):
        return Variety.region_pk == int(qs)

    def order(self):
        return Variety.region_pk


class TypeCol(Col):
    def format(self, item):
        return map_marker_img(self.dt.req, item.variety) + item.variety.type.name

    def search(self, qs):
        return self.dt.aliased_variety.type_pk == int(qs)

    def order(self):
        return self.dt.aliased_variety.type_pk


class WaveContributions(datatables.Contributions):
    def __init__(self, *args, **kw):
        super(WaveContributions, self).__init__(*args, **kw)
        self.aliased_variety = aliased(Variety)

    def base_query(self, query):
        return super(WaveContributions, self).base_query(query)\
            .join(Variety)\
            .join(self.aliased_variety)\
            .distinct()

    def col_defs(self):
        return [
            #OrderNumberCol(self),
            LinkCol(self, 'name', sTitle='Variety'),
            ContributorsCol(self, 'contributors', bSearchable=False, bSortable=False),
            TypeCol(self, 'type', choices=list((o.pk, o.name) for o in DBSession.query(VarietyType))),
            RegionCol(self, 'region', choices=list((o.pk, o.name) for o in DBSession.query(Region))),
            CitationCol(self, 'cite', bSearchable=False, bSortable=False),
        ]
