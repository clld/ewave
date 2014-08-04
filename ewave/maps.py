from clld.web.maps import LanguageMap as BaseLanguageMap
from clld.web.maps import ParameterMap, Map, FilterLegend


class LanguageMap(BaseLanguageMap):
    """small map on contribution detail page
    """
    def __init__(self, ctx, req, eid='map'):
        super(LanguageMap, self).__init__(ctx.variety, req, eid=eid)


class FeatureMap(ParameterMap):
    def __init__(self, ctx, req, eid='map', col=None):
        self.col = col
        ParameterMap.__init__(self, ctx, req, eid=eid)

    def get_legends(self):
        for legend in super(FeatureMap, self).get_legends():
            yield legend
        yield FilterLegend(self, 'EWAVE.getType', self.col)


class VarietiesMap(Map):
    def __init__(self, ctx, req, eid='map', col=None):
        self.col = col
        Map.__init__(self, ctx, req, eid=eid)

    def get_legends(self):
        for legend in super(VarietiesMap, self).get_legends():
            yield legend
        yield FilterLegend(self, 'EWAVE.getType', self.col)


def includeme(config):
    config.register_map('contribution', LanguageMap)
    config.register_map('parameter', FeatureMap)
    config.register_map('contributions', VarietiesMap)
