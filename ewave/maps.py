from clld.web.maps import LanguageMap as BaseLanguageMap
from clld.web.maps import Legend, ParameterMap, Map
from clld.web.util.helpers import JS
from clld.web.util.htmllib import HTML
from clld.db.meta import DBSession

from ewave.models import VarietyType


class LanguageMap(BaseLanguageMap):
    """small map on contribution detail page
    """
    def __init__(self, ctx, req, eid='map'):
        super(LanguageMap, self).__init__(ctx.variety, req, eid=eid)


def type_legend(map_):
    def li(value, label, checked=False):
        input_attrs = dict(
            type='radio',
            class_='stay-open vtype inline',
            name='vtype',
            value=value,
            onclick=JS("EWAVE.toggle_languages")(map_.eid))
        if checked:
            input_attrs['checked'] = 'checked'
        return HTML.label(
            HTML.input(**input_attrs),
            ' ',
            label,
            class_="stay-open",
            style="margin-left:5px; margin-right:5px;",
        )

    items = [li('--any--', '--any--', checked=True)]
    items.extend([li(vt.pk, vt.name) for vt in DBSession.query(VarietyType)])
    return Legend(map_, 'Type', items, stay_open=True)


class FeatureMap(ParameterMap):
    def get_legends(self):
        for legend in super(FeatureMap, self).get_legends():
            yield legend
        yield type_legend(self)


class VarietiesMap(Map):
    def get_legends(self):
        for legend in super(VarietiesMap, self).get_legends():
            yield legend
        yield type_legend(self)


def includeme(config):
    config.register_map('contribution', LanguageMap)
    config.register_map('parameter', FeatureMap)
    config.register_map('contributions', VarietiesMap)
