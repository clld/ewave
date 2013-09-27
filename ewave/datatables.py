from sqlalchemy.orm import aliased, joinedload
from sqlalchemy.sql.expression import cast
from sqlalchemy.types import Integer

from clld.db.util import get_distinct_values
from clld.db.models import common
from clld.db.meta import DBSession
from clld.web import datatables
from clld.web.datatables.base import (
    Col, LinkCol, filter_number, IdCol, LinkToMapCol, PercentCol,
)
from clld.web.datatables.value import ValueNameCol, ValueLanguageCol, ParameterCol
from clld.web.datatables.value import _LinkToMapCol as ValueLinkToMapCol
from clld.web.datatables.contribution import ContributorsCol, CitationCol
from clld.web.datatables.sentence import Sentences as BaseSentences
from clld.web.util.helpers import map_marker_img

from ewave.models import Region, VarietyType, Variety, Feature, FeatureCategory


def choices(col, order=None):
    order = order or col.pk
    return list((o.pk, o.name) for o in DBSession.query(col).order_by(order))


class Sentences(BaseSentences):
    def col_defs(self):
        return filter(
            lambda col: col.name not in ['type', 'd', 'analyzed', 'gloss', 'description'],
            super(Sentences, self).col_defs())


#
# contributions:
#
class _LinkToMapCol(LinkToMapCol):
    def get_obj(self, item):
        return item.variety


class RegionCol(Col):
    def __init__(self, dt, name, **kw):
        kw['choices'] = choices(Region)
        kw['sTitle'] = 'World Region'
        super(RegionCol, self).__init__(dt, name, **kw)

    def format(self, item):
        return item.variety.region.name

    def search(self, qs):
        return Variety.region_pk == int(qs)

    def order(self):
        return Variety.region_pk


class TypeCol(Col):
    def __init__(self, dt, name, **kw):
        kw['choices'] = choices(VarietyType)
        kw['sTitle'] = 'Variety Type'
        super(TypeCol, self).__init__(dt, name, **kw)

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
            TypeCol(self, 'type'),
            RegionCol(self, 'region'),
            _LinkToMapCol(self, 'm'),
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
    def __init__(self, dt, name, **kw):
        kw['choices'] = choices(FeatureCategory)
        super(CategoryCol, self).__init__(dt, name, **kw)

    def format(self, item):
        return item.category.name

    def search(self, qs):
        return Feature.category_pk == int(qs)

    def order(self):
        return Feature.category_pk


class Features(datatables.Parameters):
    def base_query(self, query):
        return query.join(Feature.category)

    def col_defs(self):
        return [
            FeatureNumberCol(self),
            LinkCol(self, 'name', sTitle='Feature name'),
            PercentCol(self, 'attestation', model_col=Feature.attestation),
            PercentCol(self, 'pervasiveness', model_col=Feature.pervasiveness),
            CategoryCol(self, 'area'),
        ]


#
# Values
#
class _RegionCol(RegionCol):
    def format(self, item):
        return item.valueset.language.region.name


class _TypeCol(TypeCol):
    def format(self, item):
        return map_marker_img(self.dt.req, item.valueset.language) + item.valueset.language.type.name

    def search(self, qs):
        return Variety.type_pk == int(qs)

    def order(self):
        return Variety.type_pk


class _ValueNameCol(ValueNameCol):
    def __init__(self, dt, name, **kw):
        if dt.parameter:
            kw['choices'] = [
                (de.name, '%s %s' % (de.name, de.description))
                for de in dt.parameter.domain]
        super(_ValueNameCol, self).__init__(dt, name, **kw)

    def order(self):
        return common.DomainElement.number

    def search(self, qs):
        return common.DomainElement.name.__eq__(qs)


class Values(datatables.Values):
    def base_query(self, query):
        query = DBSession.query(self.model)\
            .join(common.ValueSet)\
            .join(common.DomainElement)\
            .options(joinedload(common.Value.valueset), joinedload(common.Value.domainelement))\
            .distinct()

        if self.language:
            return query.join(common.ValueSet.parameter)\
                .filter(common.ValueSet.language_pk == self.language.pk)

        if self.parameter:
            return query.join(common.ValueSet.language)\
                .filter(common.ValueSet.parameter_pk == self.parameter.pk)

        return query

    def col_defs(self):
        if self.parameter:
            return [
                ValueLanguageCol(self, 'variety'),
                _RegionCol(self, 'region'),
                _TypeCol(self, 'type'),
                _ValueNameCol(self, 'name'),
                ValueLinkToMapCol(self, 'm'),
            ]
        if self.language:
            return [
                ParameterCol(self, 'feature'),
                _ValueNameCol(self, 'name'),
                # TODO: feature category
            ]
        return [
            _ValueNameCol(self, 'name'),
            ValueLanguageCol(self, 'variety'),
            ParameterCol(self, 'feature'),
        ]
