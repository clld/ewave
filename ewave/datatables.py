from sqlalchemy.orm import aliased, joinedload

from clld.db.models import common
from clld.db.meta import DBSession
from clld.web import datatables
from clld.web.datatables.base import Col, LinkCol, LinkToMapCol, PercentCol, IntegerIdCol
from clld.web.datatables.value import ValueNameCol
from clld.web.datatables.contribution import ContributorsCol, CitationCol
from clld.web.datatables.contributor import Contributors
from clld.web.datatables.sentence import Sentences as BaseSentences
from clld.web.util.helpers import map_marker_img
from clld.web.util.htmllib import HTML
from clld.web.util import glottolog

from ewave.models import Region, VarietyType, Variety, Feature, FeatureCategory, WaveContributor


def choices(col, order=None):
    order = order or col.pk
    return list((o.pk, o.name) for o in DBSession.query(col).order_by(order))


class AltTypeCol(Col):
    def __init__(self, dt, name, **kw):
        kw['choices'] = choices(VarietyType)
        kw['sTitle'] = 'Variety Type'
        super(AltTypeCol, self).__init__(dt, name, **kw)

    def format(self, item):
        return map_marker_img(self.dt.req, item.language) + item.language.type.name

    def search(self, qs):
        return Variety.type_pk == int(qs)

    def order(self):
        return Variety.type_pk


class Sentences(BaseSentences):
    def col_defs(self):
        return list(filter(
            lambda col: col.name not in ['type', 'd', 'analyzed', 'gloss', 'description'],
            super(Sentences, self).col_defs())) + [AltTypeCol(self, 'type')]


#
# contributions:
#
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
        kw['sTitle'] = 'Type'
        super(TypeCol, self).__init__(dt, name, **kw)

    def format(self, item):
        return map_marker_img(self.dt.req, item.variety) + item.variety.type.name

    def search(self, qs):
        return self.dt.aliased_variety.type_pk == int(qs)

    def order(self):
        return self.dt.aliased_variety.type_pk


class GlottocodeCol(Col):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        if item.variety.glottocode:
            return HTML.a(
                item.variety.glottocode,
                title='visit {0} in Glottolog'.format(item.variety.name),
                href=glottolog.url(item.variety.glottocode))
        return ''


class WaveContributions(datatables.Contributions):
    def __init__(self, *args, **kw):
        super(WaveContributions, self).__init__(*args, eid='Values', **kw)
        self.aliased_variety = aliased(Variety)

    def base_query(self, query):
        return super(WaveContributions, self).base_query(query)\
            .join(Variety)\
            .join(self.aliased_variety)\
            .distinct()

    def col_defs(self):
        return [
            IntegerIdCol(self, 'id'),
            LinkCol(self, 'name', sTitle='Variety'),
            ContributorsCol(self, 'contributors', bSearchable=False, bSortable=False),
            TypeCol(self, 'type'),
            RegionCol(self, 'region'),
            GlottocodeCol(self, 'glottocode'),
            LinkToMapCol(self, 'm', get_object=lambda i: i.variety),
            CitationCol(self, 'cite', bSearchable=False, bSortable=False),
        ]


#
# features:
#
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
            IntegerIdCol(self, 'id'),
            LinkCol(self, 'name', sTitle='Feature name'),
            PercentCol(
                self, 'attestation', 
                sDescription="Percentage of varieties in which the feature was rated A, B or C.", 
                model_col=Feature.attestation),
            PercentCol(
                self, 'pervasiveness', 
                sDescription="Average pervasiveness of the feature in the varieties in which it is attested. Values range between 100% (feature received only A-ratings) and 30% (feature received only C-ratings).", 
                model_col=Feature.pervasiveness),
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
        return item.valueset.language.type.name

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
                LinkCol(self, 'variety',
                        model_col=common.Language.name,
                        get_obj=lambda i: i.valueset.language),
                _RegionCol(self, 'region'),
                _TypeCol(self, 'type'),
                _ValueNameCol(self, 'value'),
                LinkToMapCol(self, 'm', get_obj=lambda i: i.valueset.language),
            ]
        if self.language:
            return [
                IntegerIdCol(
                    self, 'fid',
                    get_object=lambda i: i.valueset.parameter,
                    model_col=common.Parameter.id),
                LinkCol(
                    self, 'feature',
                    model_col=common.Parameter.name,
                    get_obj=lambda i: i.valueset.parameter),
                _ValueNameCol(self, 'value'),
                # TODO: feature category
            ]
        return [_ValueNameCol(self, 'name')]


class NameCol(LinkCol):
    def order(self):
        return WaveContributor.sortkey


class Informants(Contributors):
    def col_defs(self):
        return [NameCol(self, 'name')] + Contributors.col_defs(self)[1:]


def includeme(config):
    config.register_datatable('contributions', WaveContributions)
    config.register_datatable('contributors', Informants)
    config.register_datatable('parameters', Features)
    config.register_datatable('values', Values)
    config.register_datatable('sentences', Sentences)
