from clld.db.models import common
from clld.db.meta import DBSession


def parameter_detail_html(context=None, request=None, **kw):
    res = []
    values = DBSession.query(common.Value.pk)\
        .join(common.ValueSet).filter(common.ValueSet.parameter_pk == context.pk)\
        .subquery()
    return {
        'examples': DBSession.query(common.Sentence).join(common.ValueSentence)
        .filter(common.ValueSentence.value_pk.in_(values))}


def dataset_detail_html(context=None, request=None, **kw):
    return {
        'varieties': {o.id: o for o in DBSession.query(common.Language)},
        'features': {o.id: o for o in DBSession.query(common.Parameter)},
    }
