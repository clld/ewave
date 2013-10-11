from clld.web.maps import LanguageMap as BaseLanguageMap
from clld.web.maps import Legend, ParameterMap
from clld.web.util.helpers import JS
from clld.web.util.htmllib import HTML
from clld.db.meta import DBSession

from ewave.models import VarietyType


class LanguageMap(BaseLanguageMap):
    """small map on contribution detail page
    """
    def __init__(self, ctx, req, eid='map'):
        super(LanguageMap, self).__init__(ctx.variety, req, eid=eid)


class FeatureMap(ParameterMap):
    def get_legends(self):
        for legend in super(FeatureMap, self).get_legends():
            yield legend

        def li(value, label, label_class, input_class, onclick, type_='checkbox', name='', checked=False):
            input_attrs = dict(
                type=type_,
                class_=input_class + ' inline',
                name=name,
                value=value,
                onclick=onclick)
            if checked:
                input_attrs['checked'] = 'checked'
            return HTML.label(
                HTML.input(**input_attrs),
                ' ',
                label,
                class_="%s" % label_class,
                style="margin-left:5px; margin-right:5px;",
            )

        def type_li(vt):
            return li(
                vt.pk,
                vt.name,
                'stay-open',
                'stay-open vtype',
                JS("EWAVE.toggle_languages")(self.eid),
                type_='radio',
                name='vtype')

        items = [li(
            '--any--',
            '--any--',
            'stay-open',
            'stay-open vtype',
            JS("EWAVE.toggle_languages")(self.eid),
            type_="radio",
            name='vtype',
            checked=True)]
        for vt in DBSession.query(VarietyType):
            items.append(type_li(vt))

        yield Legend(self, 'Type', items, stay_open=True)
