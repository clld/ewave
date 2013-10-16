from clld.db.models import common
from clld.db.meta import DBSession
from clld.web.util.helpers import get_referents, map_marker_img, get_adapter
from clld.web.util.htmllib import HTML, literal
from clld.interfaces import IRepresentation

from ewave import models


def source_detail_html(context=None, request=None, **kw):
    return dict(referents=get_referents(context, exclude=['valueset']))


def dataset_detail_html(context=None, request=None, **kw):
    def vnum(*ids):
        return DBSession.query(models.Variety).join(models.VarietyType)\
            .filter(models.VarietyType.id.in_(ids)).count()
    stats = {
        'vl': vnum('L1t', 'L1c', 'L2'),
        'vpc': vnum('P', 'Cr'),
        'features': DBSession.query(models.Feature).count(),
        'informants': DBSession.query(common.Contributor)
        .filter(common.Contributor.contribution_assocs.any()).count(),
    }
    return {
        'stats': stats,
        'citation': get_adapter(IRepresentation, context, request, ext='md.txt')}


def parameter_detail_html(context=None, request=None, **kw):
    res = []
    values = DBSession.query(common.Value.pk)\
        .join(common.ValueSet).filter(common.ValueSet.parameter_pk == context.pk)\
        .subquery()
    return {
        'examples': DBSession.query(common.Sentence).join(common.ValueSentence)
        .filter(common.ValueSentence.value_pk.in_(values))}


def value_table(ctx, req):
    rows = [HTML.tr(
        HTML.td(map_marker_img(req, de)),
        HTML.td(literal(de.name + ' - ' + de.description)),
        HTML.td(str(len(de.values)), class_='right')) for de in ctx.domain]
    return HTML.table(HTML.tbody(*rows), class_='table table-condensed')
