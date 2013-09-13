from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import cast
from sqlalchemy.types import Integer

from clld.db.util import get_distinct_values
from clld.db.meta import DBSession
from clld.web import datatables
from clld.web.datatables.base import Col, LinkCol, filter_number, IdCol, LinkToMapCol
from clld.web.datatables.contribution import ContributorsCol, CitationCol
from clld.web.util.helpers import map_marker_img

from ewave.models import Region, VarietyType, Variety, Feature, FeatureCategory


def choices(col, order=None):
    order = order or col.pk
    return list((o.pk, o.name) for o in DBSession.query(col).order_by(order))


#
# contributions:
#
class _LinkToMapCol(LinkToMapCol):
    def get_obj(self, item):
        return item.variety


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
            TypeCol(self, 'type', choices=choices(VarietyType)),
            RegionCol(self, 'region', choices=choices(Region)),
            _LinkToMapCol(self),
            CitationCol(self, 'cite', bSearchable=False, bSortable=False),
        ]


#
# features:
#
class FeatureNumberCol(IdCol):
    def __init__(self, dt, name='id', **kw):
        kw.setdefault('input_size', 'mini')
        kw.setdefault('sClass', 'right')
        kw.setdefault('sTitle', 'No.')
        super(FeatureNumberCol, self).__init__(dt, name, **kw)

    def search(self, qs):
        return filter_number(cast(self.dt.model.id, Integer), qs, type_=int)

    def order(self):
        return cast(self.dt.model.id, Integer)


class CategoryCol(Col):
    def __init__(self, dt, name='category', **kw):
        kw['choices'] = choices(FeatureCategory)
        super(CategoryCol, self).__init__(dt, 'area', **kw)

    def format(self, item):
        return item.category.name

    def search(self, qs):
        return Feature.category_pk == int(qs)

    def order(self):
        return Feature.category_pk


class PercentCol(Col):
    def __init__(self, dt, **kw):
        kw['sClass'] = 'right'
        kw.setdefault('input_size', 'small')
        super(PercentCol, self).__init__(dt, **kw)

    def search(self, qs):
        return filter_number(self.model_col, qs, qs_weight=0.01)

    def format(self, item):
        return '%.0f%%' % (100 * getattr(item, self.model_col.name),)


class Features(datatables.Parameters):
    def base_query(self, query):
        return query.join(Feature.category)

    def col_defs(self):
        return [
            FeatureNumberCol(self),
            LinkCol(self, 'name', sTitle='Feature name'),
            PercentCol(self, name='attestation', model_col=Feature.attestation),
            PercentCol(self, name='pervasiveness', model_col=Feature.pervasiveness),
            CategoryCol(self),
        ]
