from clld.web.maps import LanguageMap as BaseLanguageMap
from clld.web.maps import ParameterMap, Map, FilterLegend


class LanguageMap(BaseLanguageMap):
    """small map on contribution detail page
    """
    def __init__(self, ctx, req, eid='map'):
        super(LanguageMap, self).__init__(ctx.variety, req, eid=eid)


class FeatureMap(ParameterMap):
    def __init__(self, ctx, req, eid='map', col=None, dt=None):
        self.col, self.dt = col, dt
        ParameterMap.__init__(self, ctx, req, eid=eid)

    def get_legends(self):
        for legend in super(FeatureMap, self).get_legends():
            yield legend
        yield FilterLegend(self, 'EWAVE.getType', col=self.col, dt=self.dt)


class VarietiesMap(Map):
    def __init__(self, ctx, req, eid='map', col=None, dt=None):
        self.col, self.dt = col, dt
        Map.__init__(self, ctx, req, eid=eid)

    def get_legends(self):
        for legend in super(VarietiesMap, self).get_legends():
            yield legend
        yield FilterLegend(self, 'EWAVE.getType', col=self.col, dt=self.dt)


def includeme(config):
    config.register_map('contribution', LanguageMap)
    config.register_map('parameter', FeatureMap)
    config.register_map('contributions', VarietiesMap)
