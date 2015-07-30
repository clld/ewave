from sqlalchemy.orm import joinedload

from clld.web.adapters.geojson import GeoJsonLanguages
from clld.web.adapters.download import CsvDump, Download
from clld.db.meta import DBSession
from clld.db.models.common import Parameter, Language, Source, ValueSet
from clld.interfaces import IContribution, IIndex


class GeoJsonContributions(GeoJsonLanguages):
    def feature_iterator(self, ctx, req):
        return ctx.get_query(limit=5000)

    def get_language(self, ctx, req, item):
        return item.variety


class Matrix(CsvDump):
    md_fields = [
        ('Variety URL', lambda p: None),
        ('Variety number', lambda p: int(p.id)),
        ('Abbreviation', lambda p: p.abbr),
        ('Variety', lambda p: p.name),
        ('Contributor(s)', lambda p: ' and '.join(c.name for c in p.contribution.primary_contributors)),
        ('Variety type (narrow)', lambda p: p.type.id),
        ('Variety type (broad)', lambda p: p.type.jsondata['broad']),
        ('World Region', lambda p: p.region.name),
    ]

    def get_fields(self, req):  # pragma: no cover
        res = [f[0] for f in self.md_fields]
        res.extend(['feature %s' % p.id for p in DBSession.query(Parameter).order_by(Parameter.pk)])
        return res

    def row(self, req, fp, item, index):  # pragma: no cover
        valuesets = DBSession.query(ValueSet)\
            .filter(ValueSet.language_pk == item.pk)\
            .options(joinedload(ValueSet.parameter), joinedload(ValueSet.values))
        values = {'feature %s' % vs.parameter.id: vs.values[0].domainelement.name for vs in valuesets}
        for name, getter in self.md_fields:
            values[name] = getter(item) or ''
        values['Variety URL'] = req.resource_url(item)
        return [values.get(p, '') for p in self.get_fields(req)]


def includeme(config):
    config.register_download(Matrix(Language, 'ewave', description='eWAVE value matrix as csv'))
    config.register_adapter(
        GeoJsonContributions, IContribution, IIndex, name=GeoJsonContributions.mimetype)
    config.register_download(Download(
        Source, 'ewave', ext='bib', description="Sources as BibTeX"))
